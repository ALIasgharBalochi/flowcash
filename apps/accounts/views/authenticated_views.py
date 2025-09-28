from apps.accounts.serializers import ChangePasswordSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer = ChangePasswordSerializer(data=request.data,context={'request':request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password changed successfully."},status=status.HTTP_200_OK)
        return Response({"message": serializer.error},status=status.HTTP_400_BAD_REQUEST)

