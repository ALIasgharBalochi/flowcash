from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.accounts.serializers import GoogleAuthSerializer,UserRegisterSerializer,RequestResetPasswordSerializer,ResetPasswordSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from common.utils.jwtencode import generate_reset_password_jwt
from apps.accounts.services import send_reset_password_email
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
            user = User.objects.filter(email=serializer.validated_data["email"]).first()
            if not user:
                return Response({"message": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)
            token = generate_reset_password_jwt(user)
            send_reset_password_email(user,token)
            return Response({"message": "Token successfully sent to email."}, status=status.HTTP_200_OK)
        return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswrodView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        serializer = ResetPasswordSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Password changed successfully.'},status=status.HTTP_200_OK)
        return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class GoogleAuthView(APIView):
    def post(self,request):
        serializer = GoogleAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.save()
        return Response(token)