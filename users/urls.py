from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from .views import UserRegisterView,UserProfileView,ResetPasswordView

urlpatterns = [
    path('register/',UserRegisterView.as_view(), name='register'),
    path('login/token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('login/token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('profile/',UserProfileView.as_view(),name='profile'),
    path('re_password/',ResetPasswordView().as_view(),name='re_password'),
]