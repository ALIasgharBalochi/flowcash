from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from .views import UserRegisterView,UserProfileView,ChangePasswordView,RequestResetPasswordView,ResetPasswrodView
urlpatterns = [
    path('register/',UserRegisterView.as_view(), name='register'),
    path('login/token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('login/token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('profile/',UserProfileView.as_view(),name='profile'),
    path('ch_password/',ChangePasswordView().as_view(),name='ch_password'),
    path('re_password/request_token/', RequestResetPasswordView().as_view(),name="re_password_request_for_token"),
    path('re_password/reset_password/',ResetPasswrodView().as_view(),name='reset_password')
]