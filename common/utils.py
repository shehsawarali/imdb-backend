from django.db import models
from rest_framework import serializers
from rest_framework.response import Response

MAX_STRING_LENGTH = 255
YEAR_LENGTH = 4

REQUIRED_FIELDS_ERRORS = [
    "This field may not be blank.",
    "This field is required.",
    '"" is not a valid choice.',  # for CountryField in User model
]
MISSING_REQUIRED_FIELDS = "Missing required fields."


class BaseTimestampsModel(models.Model):
    """
    Abstract model for models which require creation and update timestamps
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SimpleNameModel(models.Model):
    """
    Abstract model for models which only need a unique string
    attribute `name`
    """

    name = models.CharField(max_length=MAX_STRING_LENGTH, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class SimpleNameSerializer(serializers.Serializer):
    """
    Reusable serializer for serializing only the `name` attribute.
    """

    name = serializers.CharField(required=True)


class SimpleNameAndIdSerializer(serializers.Serializer):
    """
    Reusable serializer for serializing only the `id` and `name` attributes
    """

    id = serializers.IntegerField(required=True)
    name = serializers.CharField(required=True)


def get_first_serializer_error(errors):
    """
    Receives serializer errors and returns the first error.
    """

    error_list = [errors[error][0] for error in errors]
    message = error_list[0]

    if message in REQUIRED_FIELDS_ERRORS:
        message = MISSING_REQUIRED_FIELDS

    return message


def response_http(message, status):
    """
    Takes a message and an HTTP status code, and returns an HTTP response
    which can be sent to the client.
    """

    return Response(
        {
            "message": message,
        },
        status=status,
    )


genres = [
  "Action",
  "Adult",
  "Adventure",
  "Animation",
  "Biography",
  "Comedy",
  "Crime",
  "Documentary",
  "Drama",
  "Family",
  "Fantasy",
  "Film-Noir",
  "Game-Show",
  "History",
  "Horror",
  "Mystery",
  "Music",
  "Musical",
  "News",
  "Romance",
  "Sci-Fi",
  "Short",
  "Sport",
  "Talk-Show",
  "Thriller",
  "War",
  "Western",
]