import logging

from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .emails import send_verification_email
from .helpers import response_http_400
from .serializers import (
    LoginSerializer,
    RegistrationSerializer,
    UserSerializer,
    VerificationSerializer,
)

logger = logging.getLogger(__name__)

REQUIRED_FIELDS_ERRORS = [
    "This field may not be blank.",
    "This field is required.",
    '"" is not a valid choice.',  # for CountryField in User model
]
MISSING_REQUIRED_FIELDS = "Missing required fields."


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

        error_list = [
            serializer.errors[error][0] for error in serializer.errors
        ]
        message = error_list[0].capitalize()
        if message in REQUIRED_FIELDS_ERRORS:
            message = MISSING_REQUIRED_FIELDS

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
                        "message": "Successfully signed up! Please verify your "
                        "account using the link sent to your email "
                        "address."
                    },
                    status=status.HTTP_201_CREATED,
                )

        error_list = [
            serializer.errors[error][0] for error in serializer.errors
        ]
        message = error_list[0].capitalize()
        if message in REQUIRED_FIELDS_ERRORS:
            message = MISSING_REQUIRED_FIELDS

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

        error_list = [
            serializer.errors[error][0] for error in serializer.errors
        ]
        message = error_list[0]
        if message in REQUIRED_FIELDS_ERRORS:
            message = MISSING_REQUIRED_FIELDS

        return response_http_400(message)
