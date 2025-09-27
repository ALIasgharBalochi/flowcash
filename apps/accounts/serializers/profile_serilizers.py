from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uuid',"email","is_verified","first_name","last_name") 


class VerifiedEmail(serializers.Serializer):
    code = serializers.IntegerField()

    def validate_code(self,value):
        if len(str(value)) < 6:
             raise serializers.ValidationError('code must be at least 6 characters log.')
        return value