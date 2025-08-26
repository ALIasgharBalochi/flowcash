from django.shortcuts import render
import jwt
from datetime import datetime,timedelta
from django.conf import settings


def generate_reset_password_jwt(user):
    payload = {
        "user_id": user.id,
        "email": user.email,
        "type": "reset_password",
        "exp": datetime.utcnow() + timedelta(minutes=10),
        "iat": datetime.utcnow()
    }
    token = jwt.encode(payload,settings.SECRET_KEY,algorithm="HS256")
    return token 