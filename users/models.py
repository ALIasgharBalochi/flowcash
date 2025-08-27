from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from datetime import timedelta

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
            if not email:
                raise ValueError('The Email field must be set')
            email = self.normalize_email(email)
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True,null=False,blank=False)
    is_verified = models.BooleanField(default=False)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class OTPToken(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6) 
    create_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    @classmethod
    def create_token(cls,user,minuts=2):
        from django.utils import timezone
        import random

        otp = str(random.randint(100000,999999))
        expires = timezone.now() + timedelta(minutes=minuts)
        return cls.objects.create(user=user,otp_code=otp,expires_at=expires)

    def __str__(self):
         return self.otp_code

