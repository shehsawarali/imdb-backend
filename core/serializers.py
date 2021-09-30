from rest_framework import serializers

from common.utils import SimpleNameAndIdSerializer, SimpleNameSerializer
from users.serializers import FollowSerializer

from .models import ActivityLog, Crew, Person, Principal, Rating, Review, Title


class BasicTitleSerializer(serializers.ModelSerializer):
    """
    Serializer, for Title model, to only include the basic, minimal
    information.
    """

    rating = serializers.DecimalField(
        max_digits=3, decimal_places=1, required=False
    )

    class Meta:
        model = Title
        fields = [
            "id",
            "name",
            "start_year",
            "end_year",
            "image",
            "rating",
        ]


class BasicPersonSerializer(serializers.ModelSerializer):
    """
    Serializer, for Person model, to only include the basic, minimal
    information.
    """

    class Meta:
        model = Person
        fields = [
            "id",
            "name",
            "image",
        ]


class TitlePrincipalsSerializer(serializers.ModelSerializer):
    """
    Serializer, for Principal model belonging to a specific Title instance.
    Does not include the redundant `Title` object in the serialized data.
    """

    person = BasicPersonSerializer()

    class Meta:
        model = Principal
        fields = ["person", "category", "characters"]


class PersonPrincipalsSerializer(serializers.ModelSerializer):
    """
    Serializer, for Principal model belonging to a specific Person instance.
    Does not include the redundant `Person` object in the serialized data.
    """

    title = BasicTitleSerializer()

    class Meta:
        model = Principal
        fields = ["category", "characters", "title"]


class CrewSerializer(serializers.ModelSerializer):
    """
    Serializer, for Crew model belonging to a specific Title instance. Does
    not include the redundant `Title` object in the serialized data.
    """

    writers = SimpleNameAndIdSerializer(many=True)
    directors = SimpleNameAndIdSerializer(many=True)

    class Meta:
        model = Crew
        fields = ["writers", "directors"]


class TitleSerializer(serializers.ModelSerializer):
    """
    Serializer for Title model, in TitleDetail view.
    """

    genres = SimpleNameSerializer(many=True)
    principals = TitlePrincipalsSerializer(many=True)
    crew = CrewSerializer()
    rating = serializers.DecimalField(max_digits=3, decimal_places=1)
    rating_count = serializers.IntegerField()
    type = SimpleNameAndIdSerializer()

    class Meta:
        model = Title
        fields = [
            "id",
            "name",
            "is_adult",
            "start_year",
            "end_year",
            "runtime_minutes",
            "type",
            "genres",
            "principals",
            "crew",
            "rating",
            "rating_count",
            "image",
            "description",
        ]


class PersonSerializer(serializers.ModelSerializer):
    """
    Serializer for Person model, in PersonDetail view.
    """

    known_for_titles = BasicTitleSerializer(many=True)
    professions = SimpleNameSerializer(many=True)
    filmography = PersonPrincipalsSerializer(many=True)

    class Meta:
        model = Person
        fields = [
            "id",
            "name",
            "birth_year",
            "death_year",
            "known_for_titles",
            "professions",
            "filmography",
            "image",
            "description",
        ]


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving instance of Review model.
    """

    title = SimpleNameAndIdSerializer()
    user = FollowSerializer()

    class Meta:
        model = Review
        fields = ["title", "review", "user"]


class CreateReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for creating instances of Review model.
    """

    class Meta:
        model = Review
        fields = ["title", "user", "review"]


class RatingSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and retrieving instances of Rating model.
    """

    rating = serializers.IntegerField(max_value=10, min_value=1)

    class Meta:
        model = Rating
        fields = ["title", "user", "rating"]


class ActivitySerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving instances of ActivityLog model.
    """

    rating = RatingSerializer(required=False)
    review = ReviewSerializer(required=False)
    title = BasicTitleSerializer()
    user = FollowSerializer()

    class Meta:
        model = ActivityLog
        fields = [
            "user",
            "title",
            "action",
            "rating",
            "review",
            "created_at",
        ]
