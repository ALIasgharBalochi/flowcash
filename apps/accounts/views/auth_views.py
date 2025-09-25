from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.accounts.serializers import UserRegisterSerializer,RequestResetPasswordSerializer,ResetPasswordSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from common.utils.jwtencode import generate_reset_password_jwt
from django.core.mail import send_mail

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

            return Response({'message':'Password changed successfully.'},status=status.HTTP_200_OK)
        return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)