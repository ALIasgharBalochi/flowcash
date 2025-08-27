from django.shortcuts import render
from django.contrib.auth import update_session_auth_hash
from rest_framework import status,generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response 
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .models import OTPToken
from .serializers import UserRegisterSerializer,UserProfileSerializer,ChangePasswordSerializer,RequestResetPasswordSerializer,ResetPasswordSerializer,VerifiedEmail
from core.views import generate_reset_password_jwt
from django.core.mail import send_mail
from django.utils import timezone 

User = get_user_model()
class UserRegisterView(APIView):
    def post(self,request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered Successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self,request,*args,**kwargs):
        kwargs['partial']=True
        return super().update(request,*args,**kwargs)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer = ChangePasswordSerializer(data=request.data)

        user = request.user

        if serializer.is_valid():
            if not user.check_password(serializer.validated_data["old_password"]):
                return Response({"message":'the current password is incorrect'},status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(serializer.validated_data["new_password"])
            user.save()

            update_session_auth_hash(request,user)

            return Response({"message": "Password changed successfully."},status=status.HTTP_200_OK)
        return Response({"message": serializer.error},status=status.HTTP_400_BAD_REQUEST)

class RequestResetPasswordView(APIView):
    permission_classes = [AllowAny]
    
    def post(self,request):
        serializer = RequestResetPasswordSerializer(data=request.data)

        if serializer.is_valid():
            user = User.objects.get(email=serializer.validated_data["email"])
            token = generate_reset_password_jwt(user)

            send_mail(
                subject="FlowCash Password Reset Request",
                message=f"""
                    Hello {user.first_name},

                    We received a request to reset your password for your FlowCash account.
                    Click the link below to reset your password:

                    your token it is : {token}

                    If you did not request this, please ignore this email.

                    Thanks,
                    The FlowCash Team
                    """,
                from_email="alibalochi1910@gmail.com",
                recipient_list=[user.email]
                ) 
            return Response({"message": "Token successfully sent to email."}, status=status.HTTP_200_OK)
        return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswrodView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        serializer = ResetPasswordSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]

            user.set_password(serializer.validated_data["new_password"])
            user.save()

            update_session_auth_hash(request,user)

            return Response({'message':'Password changed successfully.'},status=status.HTTP_200_OK)
        return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class EmailVerifiedToken(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  
        OTPToken.objects.filter(user=user).delete()   
        otp_token = OTPToken.create_token(user)

        send_mail(
            subject="Your OTP code for email verification",
            message=f"Your OTP code is: {otp_token.otp_code}",
            from_email="alibalochi1910@gmail.com",
            recipient_list=[user.email]
        )
        return Response({"message": "OTP code sent successfully"}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = VerifiedEmail(data=request.data)
        user = request.user  

        if serializer.is_valid():
            otp_token = OTPToken.objects.filter(
                user=user,
                otp_code=serializer.validated_data['code'],
                expires_at__gte=timezone.now()
            ).first()

            if otp_token:
                user.is_verified = True
                user.save()
                otp_token.delete()
                return Response(
                    {"message": "Your email has been successfully verified."},
                    status=status.HTTP_200_OK
                )

            return Response({"message": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        

