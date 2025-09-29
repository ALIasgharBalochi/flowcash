from celery import shared_task
from django.core.mail import send_mail

@shared_task(bind=True)
def send_email_celery(self, subject, message, from_email, recipient_list):
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False
        )
        return "Email sent successfully"
    except Exception as e:
        self.retry(exc=e, countdown=10, max_retries=3)