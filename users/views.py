import logging

from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import status, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from common.utils import (
    MISSING_REQUIRED_FIELDS,
    get_first_serializer_error,
    response_http,
)

from .emails import (
    send_password_changed_email,
    send_password_reset_link,
    send_registration_email,
)
from .models import User
from .serializers import (
    ChangePasswordSerializer,
    FollowSerializer,
    LoginSerializer,
    PasswordResetSerializer,
    RegistrationSerializer,
    ResetLinkSerializer,
    UserSerializer,
    VerificationSerializer,
)

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
        return response_http(message, status.HTTP_400_BAD_REQUEST)


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
                send_registration_email(new_user)
                return response_http(
                    "Successfully signed up! Please verify "
                    "your account using the link sent to your "
                    "email address.",
                    status.HTTP_201_CREATED,
                )

        message = get_first_serializer_error(serializer.errors)
        message = message.capitalize()
        return response_http(message, status.HTTP_400_BAD_REQUEST)


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
        return response_http(message, status.HTTP_400_BAD_REQUEST)


class ForgotPassword(APIView):
    """
    View for handling password reset request from client. Returns an error
    message if a user with given the email address does not exist, or if the
    send_password_reset_email function throws an error. Returns a success
    message otherwise.
    """

    def post(self, request):
        try:
            email = request.data["email"]
            user = User.objects.get(email=email)
        except (KeyError, User.DoesNotExist):
            return response_http(
                "Please reset your password using the link sent"
                "to your email address",
                status.HTTP_200_OK,
            )

        email_error = send_password_reset_link(user)
        if email_error:
            return Response(
                {"message": email_error},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return response_http(
            "Please reset your password using the link sent "
            "to your email address",
            status.HTTP_200_OK,
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
        return response_http(message, status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """
        Requires `token`, `id`, `password`, and `confirm_password` in the
        payload. Returns a success message upon successful password reset.
        Returns an error message otherwise.

        The token and id must be valid to change the password.
        """
        if not request.user.is_anonymous:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data)

        message = get_first_serializer_error(serializer.errors)
        return response_http(message, status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    """
    View for blacklisting RefreshToken when user logs out
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
        except KeyError:
            return response_http(
                MISSING_REQUIRED_FIELDS, status.HTTP_400_BAD_REQUEST
            )

        token_object = RefreshToken(refresh_token)
        token_object.blacklist()

        return response_http("Successfully signed out", status.HTTP_200_OK)


class UserViewSet(viewsets.ViewSet):
    """
    ViewSet for retrieving and updating public user information.
    """

    queryset = User.objects.all().prefetch_related("follows", "followers")

    def retrieve(self, request, pk):
        user = get_object_or_404(self.queryset, id=pk)
        serializer = UserSerializer(user, context={"request": request})

        return Response({"profile": serializer.data})

    def update(self, request, pk):
        if not request.user.id == int(pk):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        user = get_object_or_404(self.queryset, id=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data})

        message = get_first_serializer_error(serializer.errors)
        return response_http(message, status.HTTP_400_BAD_REQUEST)


class Follow(APIView):
    """
    View for following/unfollowing other users. POST method receives follow
    requests, and DELETE method receives unfollow requests.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = get_object_or_404(User, id=pk)

        if not user.id == request.user.id:
            request.user.follows.add(user.id)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Followed"})

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = get_object_or_404(User, id=pk)

        if not user.id == request.user.id:
            request.user.follows.remove(user.id)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Unfollowed"})

        return Response(status=status.HTTP_400_BAD_REQUEST)


class ChangePassword(APIView):
    """
    View for changing a user's password. This view requires the user to be
    authenticated.
    """

    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = ChangePasswordSerializer(request.user, data=request.data)
        if serializer.is_valid():
            new_password = request.data.get("new_password")
            request.user.set_password(new_password)
            request.user.save()
            send_password_changed_email(request.user)
            return Response({"message": "Password Changed"})

        message = get_first_serializer_error(serializer.errors)
        return response_http(message, status.HTTP_400_BAD_REQUEST)


class UserFollowers(ListAPIView):
    """
    View for listing users who follow a particular user. This view will return
    the complete list, but can be paginated using query params.
    """

    serializer_class = FollowSerializer

    def get_queryset(self):
        pk = self.kwargs["pk"]
        user = User.objects.filter(id=pk).prefetch_related("followers").first()
        return user.followers.all()


class UserFollowing(ListAPIView):
    """
    View for listing users who are followed by a particular user. This view
    will return the complete list, but can be paginated using query params.
    """

    serializer_class = FollowSerializer

    def get_queryset(self):
        pk = self.kwargs["pk"]
        user = User.objects.filter(id=pk).prefetch_related("follows").first()
        return user.follows.all()


class AvatarUpload(APIView):
    """
    View for uploading User Avatar. Requires a single image file in a
    `multipart/form-data` http request.
    """

    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = UserSerializer(
            request.user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return response_http("Uploaded", status.HTTP_200_OK)

        message = get_first_serializer_error(serializer.errors)
        return response_http(message, status.HTTP_400_BAD_REQUEST)
