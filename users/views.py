from django.shortcuts import render
from django.contrib.auth import update_session_auth_hash
from rest_framework import status,generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response 
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import UserRegisterSerializer,UserProfileSerializer,ResetPasswordSerializer

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

class ResetPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer = ResetPasswordSerializer(data=request.data)

        user = request.user

        if serializer.is_valid():
            if not user.check_password(serializer.validated_data["old_password"]):
                return Response({"message":'the current password is incorrect'},status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(serializer.validated_data["new_password"])
            user.save()

            update_session_auth_hash(request,user)

            return Response({"message": "Password changed successfully."},status=status.HTTP_200_OK)
        return Response({"message": serializer.error},status=status.HTTP_400_BAD_REQUEST)
