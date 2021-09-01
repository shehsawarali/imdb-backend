from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .emails import send_verification_email
from .models import User
from .utils import (
    BaseUserTokenSerializer,
    password_reset_token,
    verification_token,
)


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer, for User model, to filter which attributes will be returned
    to client
    """

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "country",
            "age",
            "date_joined",
            "verified",
        ]


class RegistrationSerializer(serializers.ModelSerializer, CountryFieldMixin):
    """
    Serializer, for Registration view, to validate form data received from
    client, and create new User instance upon successful validation.
    """

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "password",
            "country",
            "age",
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class LoginSerializer(serializers.ModelSerializer):
    """
    Serializer, for Login view, to validate form data received from
    client. Returns user object and authentication tokens upon successful
    login. Otherwise, raises an error. If user is not verified, calls
    send_verification_email()
    """

    class Meta:
        model = User
        fields = ["email", "password"]
        extra_kwargs = {
            "email": {"validators": []},
            "password": {
                "write_only": True,
            },
        }

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Incorrect email or password")

        if not user.verified:
            email_error = send_verification_email(user)
            if email_error:
                raise serializers.ValidationError(email_error)

            raise serializers.ValidationError(
                "Please verify your account using the link sent to your "
                "email address."
            )

        refresh = RefreshToken.for_user(user)
        serialized_user = UserSerializer(user)
        update_last_login(None, user)

        return {
            "user": serialized_user.data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "message": "Successfully logged in",
        }


class VerificationSerializer(BaseUserTokenSerializer):
    """
    Serializer, for AccountVerification view, to validate data received
    from client. Verifies user and returns success message if the data is
    valid. Otherwise, raises an error.
    """

    def validate(self, data):

        try:
            user, token = self.parse_data(data)
        except (KeyError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError("Verification link is invalid")

        if verification_token.check_token(user, token):
            user.verified = True
            user.save()

            return {
                "message": "Your account has been verified.",
            }

        raise serializers.ValidationError(
            "Verification link is invalid or expired"
        )


class ResetLinkSerializer(BaseUserTokenSerializer):
    """
    Serializer, for POST method of ResetPassword view, to validate the
    password reset link used by the client. Returns success message if the
    link is valid. Otherwise, raises an error.
    """

    def validate(self, data):

        try:
            user, token = self.parse_data(data)
        except (KeyError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError("Reset link is invalid")

        if password_reset_token.check_token(user, token):
            user.verified = True
            user.save()

            return {
                "message": "Enter your new password",
            }

        raise serializers.ValidationError("Reset link is invalid or expired")


class ResetSerializer(serializers.ModelSerializer, BaseUserTokenSerializer):
    """
    Serializer, for PUT method of ResetPassword view, to validate the
    password reset link used by the client, and change the corresponding
    user's password. Returns success message if the password is successfully
    reset. Otherwise, raises an error.
    """

    confirm_password = serializers.CharField(required=True, allow_blank=False)

    class Meta:
        model = User
        fields = ["password", "confirm_password", "token", "id"]
        extra_kwargs = {
            "password": {"write_only": True},
            "confirm-password": {"write_only": True},
        }

    def validate(self, data):
        try:
            user, token = self.parse_data(data)
        except (KeyError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError("Reset link is invalid")

        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")

        user.set_password(password)
        user.save()

        return {
            "message": "Your password has been reset",
        }
