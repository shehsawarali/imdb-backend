from django.contrib.auth import authenticate
from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


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
    login. Otherwise, raises an error.
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

        serialized_user = UserSerializer(user)
        refresh = RefreshToken.for_user(user)

        return {
            "user": serialized_user.data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "message": "Successfully logged in",
        }
