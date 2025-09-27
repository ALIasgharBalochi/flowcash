from rest_framework import generics,status
from rest_framework.permissions import IsAuthenticated
from apps.accounts.serializers import UserProfileSerializer,VerifiedEmail
from rest_framework.views import APIView
from apps.accounts.services import create_and_send_email_token,verify_email_token
from rest_framework.response import Response

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
        create_and_send_email_token(request.user)
        return Response({"message": "OTP code sent successfully"}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = VerifiedEmail(data=request.data)

        if serializer.is_valid():
            success = verify_email_token(request.user, serializer.validated_data['code'])
            if success:
                return Response({"message": "Your email has been successfully verified."}, status=status.HTTP_200_OK)
            return Response({"message": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)