from django.core.mail import send_mail
from apps.accounts.models import OTPToken
from django.utils import timezone
from .tasks import send_email_celery
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
def create_and_send_email_token(user):
    OTPToken.objects.filter(user=user).delete()   
    otp_token = OTPToken.create_token(user)

    send_email_celery.delay(
        subject="Your OTP code for email verification",
        message=f"Your OTP code is: {otp_token.otp_code}",
        from_email="alibalochi1910@gmail.com",
        recipient_list=[user.email]
    )
    return otp_token 

def verify_email_token(user,code):
    otp_token = OTPToken.objects.filter(
            user=user,
            otp_code=code,
            expires_at__gte=timezone.now()
    ).first()

    if otp_token:
        user.is_verified = True
        user.save()
        otp_token.delete()
        return True
    return False

def send_reset_password_email(user,token):
    send_email_celery.delay(
        subject="FlowCash Password Reset Request",
        message=f"""
            Hello {user.first_name},

            We received a request to reset your password for your FlowCash account.
            Click the link below to reset your password:

            your token it is : {token}

            If you did not request this, please ignore this email.

            Thanks,
            The FlowCash Team
            """,
        from_email="alibalochi1910@gmail.com",
        recipient_list=[user.email]
    )

def verify_google_id_token(token):
    try:
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            settings.GOOGLE_CLIENT_ID
        )
        return idinfo
    except ValueError: 
        return None
    
def get_or_created_user(idinfo):
    from django.contrib.auth import get_user_model
    User = get_user_model()

    user, created = User.objects.get_or_create(
        email=idinfo.get('email'),
        defaults={
        'first_name':idinfo.get('given_name',""),
        'last_name':idinfo.get('family_name',""),
        }
    )

    if created:
        user.set_unusable_password()
        user.save()

    return user


