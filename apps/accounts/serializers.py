from rest_framework import serializers
from django.contrib.auth import get_user_model
import jwt
from django.conf import settings

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uuid', "password","email","first_name","last_name")
        extra_kwargs = {'password': {'write_only':True}}

    def create(self,validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uuid',"email","is_verified","first_name","last_name") 

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate_new_password(self,value):
        if len(value) < 6:
            raise serializers.ValidationError('Password must be at least 6 characters long.')
        return value

class RequestResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self,value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError('This email is not registered')   
        return value

class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, attrs):
        token = attrs.get("token")

        try:
            payload = jwt.decode(
                jwt=token,
                key=settings.SECRET_KEY,
                algorithms=["HS256"]
            )
            user = User.objects.get(uuid=payload["user_id"])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError({"token": "Activation link expired"})
        except jwt.InvalidTokenError:
            raise serializers.ValidationError({"token": "Invalid token"})
        except User.DoesNotExist:
            raise serializers.ValidationError({"token": "User not found"})

        attrs["user"] = user  
        return attrs

    def validate_new_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("Password must be at least 6 characters long.")
        return value

class VerifiedEmail(serializers.Serializer):
    code = serializers.IntegerField()

    def validate_code(self,value):
        if len(str(value)) < 6:
             raise serializers.ValidationError('code must be at least 6 characters log.')
        return value
