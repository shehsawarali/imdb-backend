from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import Login, Registration, VerifySession

urlpatterns = [
    path("login/", Login.as_view()),
    path("session/", VerifySession.as_view()),
    path("register/", Registration.as_view()),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
