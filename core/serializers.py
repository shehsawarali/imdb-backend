from rest_framework import serializers

from common.utils import SimpleNameAndIdSerializer, SimpleNameSerializer

from .models import Crew, Person, Principal, Title


class BasicTitleSerializer(serializers.ModelSerializer):
    """
    Serializer, for Title model, to only include the basic, minimal
    information.
    """

    type = SimpleNameAndIdSerializer()

    class Meta:
        model = Title
        fields = ["id", "name", "start_year", "end_year", "image", "type"]


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


class PersonPrincipalsSerializers(serializers.ModelSerializer):
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
    principals = PersonPrincipalsSerializers(many=True)

    class Meta:
        model = Person
        fields = [
            "id",
            "name",
            "birth_year",
            "death_year",
            "known_for_titles",
            "professions",
            "principals",
            "image",
            "description",
        ]
