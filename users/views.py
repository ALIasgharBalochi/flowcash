from django.shortcuts import render
from rest_framework import status,generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response 
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import UserRegisterSerializer,UserProfileSerializer

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

