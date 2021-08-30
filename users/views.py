from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .helpers import response_http_400
from .models import User
from .serializers import UserSerializer


class LoginAPI(APIView):
    def post(self, request):
        print(request.data)
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
        return Response({"user": serializer.data, "message": "Logging in..."})
