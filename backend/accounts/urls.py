from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    PasswordResetRequestView,
    RegisterView,
    me,
    password_change,
    password_reset_confirm,
)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("token/", TokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("me/", me),
    path("password/change/", password_change),
    path("password/reset/", PasswordResetRequestView.as_view()),
    path("password/reset/confirm/", password_reset_confirm),
]
