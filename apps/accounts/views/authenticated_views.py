from apps.accounts.serializers import ChangePasswordSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

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

            return Response({"message": "Password changed successfully."},status=status.HTTP_200_OK)
        return Response({"message": serializer.error},status=status.HTTP_400_BAD_REQUEST)

