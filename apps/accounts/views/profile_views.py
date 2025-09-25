from rest_framework import generics,status
from rest_framework.permissions import IsAuthenticated
from apps.accounts.serializers import UserProfileSerializer,VerifiedEmail
from rest_framework.views import APIView
from apps.accounts.models import OTPToken
from django.core.mail import send_mail
from rest_framework.response import Response
from django.utils import timezone

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self,request,*args,**kwargs):
        kwargs['partial']=True
        return super().update(request,*args,**kwargs)

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