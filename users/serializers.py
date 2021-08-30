from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers

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


class SignUpSerializer(serializers.ModelSerializer, CountryFieldMixin):
    """
    Serializer, for RegistrationAPI, to validate form data received from
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
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
