import logging

from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .emails import send_password_reset_email, send_verification_email
from .helpers import response_http_400
from .models import User
from .serializers import (
    LoginSerializer,
    RegistrationSerializer,
    ResetLinkSerializer,
    ResetSerializer,
    UserSerializer,
    VerificationSerializer,
)
from .utils import MISSING_REQUIRED_FIELDS, get_first_serializer_error

logger = logging.getLogger(__name__)


class Login(APIView):
    """
    View for authenticating login requests from client. Returns
    validated_data from LoginSerializer upon successful registration.
    Otherwise, returns the error raised by LoginSerializer
    """

    @method_decorator(sensitive_post_parameters("password"))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        if not request.user.is_anonymous:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data)

        message = get_first_serializer_error(serializer.errors)
        message = message.capitalize()
        return response_http_400(message)


class Registration(APIView):
    """
    View for authenticating registration requests from client. Returns
    success message upon successful registration. Otherwise, returns
    the error raised by RegistrationSerializer
    """

    @method_decorator(sensitive_post_parameters("password"))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        if not request.user.is_anonymous:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            if new_user:
                send_verification_email(new_user)
                return Response(
                    {
                        "message": "Successfully signed up! Please verify your"
                        " account using the link sent to your email "
                        "address."
                    },
                    status=status.HTTP_201_CREATED,
                )

        message = get_first_serializer_error(serializer.errors)
        message = message.capitalize()
        return response_http_400(message)


class VerifySession(APIView):
    """
    View for verifying a received authentication token. Returns the
    authenticated user's serialized User instance upon successful
    verification. If token is invalid, automatically returns `HTTP 401
    Unauthorized` error
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({"user": serializer.data})


class AccountVerification(APIView):
    """
    View for verifying a received authentication token. Returns the
    message returned by VerificationSerializer if the data is valid. If
    data is invalid, returns the error raised by VerificationSerializer.
    """

    def post(self, request):
        if not request.user.is_anonymous:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = VerificationSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data)

        message = get_first_serializer_error(serializer.errors)
        return response_http_400(message)


class ForgotPassword(APIView):
    """
    View for handling password reset request from client. Returns an error
    message if a user with given the email address does not exist, or if the
    send_password_reset_email function throws an error. Returns a success
    message otherwise.
    """

    def post(self, request):
        try:
            email = request.data.get("email")
            user = User.objects.get(email=email)
        except (KeyError, User.DoesNotExist):
            return Response(
                {
                    "message": "Please reset your password using the link sent to "
                    "your email address"
                }
            )

        email_error = send_password_reset_email(user)
        if email_error:
            return Response(
                {"message": email_error},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {
                "message": "Please reset your password using the link sent to "
                "your email address"
            }
        )


class ResetPassword(APIView):
    """
    View for resetting the user's password.
    """

    def post(self, request):
        """
        Requires `token` and `id` in the payload. Returns a success message
        if the token and id are valid. Returns and error message otherwise.
        """
        if not request.user.is_anonymous:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = ResetLinkSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data)

        message = get_first_serializer_error(serializer.errors)
        return response_http_400(message)

    def put(self, request):
        """
        Requires `token`, `id`, `password`, and `confirm_password` in the
        payload. Returns a success message upon successful password reset.
        Returns an error message otherwise.

        The token and id must be valid to change the password.
        """
        if not request.user.is_anonymous:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = ResetSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data)

        message = get_first_serializer_error(serializer.errors)
        return response_http_400(message)


class Logout(APIView):
    """
    View for blacklisting RefreshToken when user logs out
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                raise KeyError
        except KeyError:
            return response_http_400(MISSING_REQUIRED_FIELDS)

        token_object = RefreshToken(refresh_token)
        token_object.blacklist()

        return Response({"message": "Successfully signed out"})
