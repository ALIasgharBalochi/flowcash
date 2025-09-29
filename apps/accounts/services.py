from django.core.mail import send_mail
from apps.accounts.models import OTPToken
from django.utils import timezone
from .tasks import send_verified_email

def create_and_send_email_token(user):
    OTPToken.objects.filter(user=user).delete()   
    otp_token = OTPToken.create_token(user)

    send_verified_email.delay(
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
        send_mail(
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

