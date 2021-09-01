from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    AccountVerification,
    ForgotPassword,
    Login,
    Registration,
    ResetPassword,
    VerifySession,
)

urlpatterns = [
    path("login/", Login.as_view(), name="user_login"),
    path("session/", VerifySession.as_view(), name="user_verify_session"),
    path("register/", Registration.as_view(), name="user_register"),
    path("verify/", AccountVerification.as_view(), name="user-verify"),
    path(
        "forgot-password/",
        ForgotPassword.as_view(),
        name="user-forgot-password",
    ),
    path(
        "reset-password/", ResetPassword.as_view(), name="user-reset-password"
    ),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
