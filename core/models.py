from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from common.utils import BaseTimestampsModel, SimpleNameModel

from .managers import TitleManager

YEAR_LENGTH = 4
CHAR_LENGTH = 255


class Genre(SimpleNameModel):
    """
    Genre model, for title genres e.g. Horror, Romance, etc. Stores
    the string attribute `name` as primary_key.
    """

    pass


class TitleType(SimpleNameModel):
    """
    TitleType model, for title types e.g. short, movie, tvSeries,
    reissue, title, etc. Stores the string attribute `name` as
    primary_key.
    """

    pass


class Profession(SimpleNameModel):
    """
    Profession model, for person professions e.g. writer, talent_agent,
    stunt, etc. Stores the string attribute `profession` as
    primary_key.
    """

    pass


class Title(BaseTimestampsModel):
    """
    Title model, for basic information of every title. Stores integer
    attribute `id` as primary_key. References TitleType and Genre as
    foreign_key.
    """

    class Meta:
        base_manager_name = "objects"

    id = models.PositiveBigIntegerField(primary_key=True)
    type = models.ForeignKey(TitleType, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=CHAR_LENGTH)
    is_adult = models.BooleanField(default=False)
    start_year = models.CharField(
        max_length=YEAR_LENGTH, null=True, blank=True
    )
    end_year = models.CharField(max_length=YEAR_LENGTH, null=True, blank=True)
    runtime_minutes = models.PositiveIntegerField(null=True, blank=True)
    genres = models.ManyToManyField(
        Genre, blank=True, related_name="genres", db_column="genre"
    )
    image = models.ImageField(upload_to="title", blank=True)
    description = models.TextField(blank=True)

    objects = TitleManager()

    def __str__(self):
        return f"{self.name}, id={self.id}"


class TitleName(BaseTimestampsModel):
    """
    TitleName model, for storing different names for a Title.
    Stores auto id as primary_key. References Title and TitleType as
    foreign_key.
    """

    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    name = models.CharField(max_length=CHAR_LENGTH)
    region = models.CharField(max_length=CHAR_LENGTH, null=True, blank=True)
    language = models.CharField(max_length=CHAR_LENGTH, null=True, blank=True)
    is_original_title = models.BooleanField(default=True)
    types = models.ManyToManyField(TitleType, blank=True, related_name="types")
    attributes = models.ManyToManyField(
        TitleType, blank=True, related_name="attributes"
    )


class Person(BaseTimestampsModel):
    """
    Person model, for information of people/performers. Stores integer
    attribute `id` as primary key. References Profession and
    Title as foreign_key.
    """

    id = models.PositiveBigIntegerField(primary_key=True)
    name = models.CharField(max_length=CHAR_LENGTH)
    birth_year = models.CharField(
        max_length=YEAR_LENGTH, null=True, blank=True
    )
    death_year = models.CharField(
        max_length=YEAR_LENGTH, null=True, blank=True
    )
    professions = models.ManyToManyField(
        Profession,
        blank=True,
        related_name="professions",
        db_column="profession",
    )
    known_for_titles = models.ManyToManyField(
        Title, blank=True, related_name="known_for_titles"
    )
    image = models.ImageField(upload_to="person", blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name}, id={self.id}"


class Principal(BaseTimestampsModel):
    """
    Person model, for information of a Person's contribution in a
    Title. Stores auto id as primary_key References Title and
    Person as foreign_key.
    """

    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="principals"
    )
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="filmography"
    )
    category = models.CharField(max_length=CHAR_LENGTH)
    job = models.CharField(max_length=CHAR_LENGTH, null=True, blank=True)
    characters = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["-title__start_year", "-title__end_year"]

    def __str__(self):
        person = f"{self.person.name} ({self.person.id})"
        title = f"{self.title.name} ({self.title.id})"
        return f"{person} in {title}"


class Rating(BaseTimestampsModel):
    """
    Rating model, specifying each rating submitted in the system by any user.
    Stores auto id as primary_key. References settings.AUTH_USER_MODEL and
    Title as foreign keys.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ratings",
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="ratings"
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    outdated = models.BooleanField(default=False)


class Review(BaseTimestampsModel):
    """
    Rating model, specifying each review submitted in the system by any user.
    Stores auto id as primary_key. References settings.AUTH_USER_MODEL and
    Title as foreign keys.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="reviews"
    )
    review = models.TextField()
    outdated = models.BooleanField(default=False)


class ActivityLog(BaseTimestampsModel):
    """
    ActivityLog model, to store every action performed by user on a title.
    Stores auto id as primary_key. References settings.AUTH_USER_MODEL,
    Title and Action as foreign keys.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    action = models.CharField(max_length=CHAR_LENGTH)
    rating = models.ForeignKey(
        Rating, on_delete=models.CASCADE, blank=True, null=True
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, blank=True, null=True
    )


class Crew(models.Model):
    """
    Crew model, for directors and writers of a Title object. Stores auto id
    as primary_key. References Title and Person as foreign keys.
    """

    title = models.OneToOneField(
        Title, on_delete=models.CASCADE, related_name="crew"
    )

    directors = models.ManyToManyField(
        Person, related_name="directors", blank=True
    )

    writers = models.ManyToManyField(
        Person, related_name="writers", blank=True
    )

    class Meta:
        verbose_name_plural = "crew"
