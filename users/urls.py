from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    AccountVerification,
    AvatarUpload,
    ChangePassword,
    Follow,
    ForgotPassword,
    Login,
    Logout,
    Registration,
    ResetPassword,
    UserFollowers,
    UserFollowing,
    UserViewSet,
    VerifySession,
)

urlpatterns = [
    path("login/", Login.as_view(), name="login"),
    path("session/", VerifySession.as_view(), name="session"),
    path("register/", Registration.as_view(), name="register"),
    path("verify/", AccountVerification.as_view(), name="verify"),
    path("forgot-password/", ForgotPassword.as_view(), name="forgot-password"),
    path("reset-password/", ResetPassword.as_view(), name="reset-password"),
    path("change-email/", ChangePassword.as_view(), name="change-password"),
    path("<int:pk>/followers/", UserFollowers.as_view(), name="followers"),
    path("<int:pk>/following/", UserFollowing.as_view(), name="following"),
    path("logout/", Logout.as_view(), name="logout"),
    path("follow/<int:pk>/", Follow.as_view(), name="follow"),
    path("upload-image/", AvatarUpload.as_view(), name="upload-avatar"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

router = DefaultRouter()
router.register("", UserViewSet, basename="user")
urlpatterns += router.urls
