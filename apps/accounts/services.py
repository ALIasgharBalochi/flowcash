from django.core.mail import send_mail
from apps.accounts.models import OTPToken
from django.utils import timezone

def create_and_send_email_token(user):
    OTPToken.objects.filter(user=user).delete()   
    otp_token = OTPToken.create_token(user)

    send_mail(
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