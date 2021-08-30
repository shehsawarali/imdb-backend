from django.contrib.auth.models import update_last_login
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .helpers import response_http_400
from .models import User
from .serializers import UserSerializer


class LoginAPI(APIView):
    """
    View for authenticating login requests from client. Requires `email` and
    `password` attributes in request payload. Returns user object and
    authentication tokens upon successful login. Otherwise, returns
    appropriate error message.
    """

    def post(self, request):
        if not request.user.is_anonymous:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            email = request.data["email"]
            password = request.data["password"]
        except KeyError:
            return response_http_400("Missing email or password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return response_http_400("Account does not exist")

        if not user.check_password(password):
            return response_http_400("Incorrect email or password")

        serializer = UserSerializer(user)
        refresh = RefreshToken.for_user(user)
        update_last_login(None, user)

        return Response(
            {
                "user": serializer.data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "message": "Successfully logged in",
            }
        )


class VerifySession(APIView):
    """
    View for verifying a received authentication token. Returns the
    authenticated user's User object upon successful verification. If token
    is invalid, automatically returns `HTTP 401 Unauthorized` error
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({"user": serializer.data})
