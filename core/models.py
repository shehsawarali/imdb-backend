from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

YEAR_LENGTH = 4
CHAR_LENGTH = 255


class SimpleNameModel(models.Model):
    """
    Abstract DRY class for models which only need a unique string
    attribute 'name'
    """

    name = models.CharField(max_length=CHAR_LENGTH, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Genre(SimpleNameModel):
    """
    Genre model, for title genres e.g. Horror, Romance, etc. Stores
    the string attribute `name` as primary_key.
    """


class TitleType(SimpleNameModel):
    """
    TitleType model, for title types e.g. short, movie, tvSeries,
    reissue, title, etc. Stores the string attribute 'name' as
    primary_key.
    """


class Profession(SimpleNameModel):
    """
    Profession model, for person professions e.g. writer, talent_agent
    , stunt, etc. Stores the string attribute 'profession' as
    primary_key.
    """


class Title(models.Model):
    """
    Title model, for basic information of every title. Stores integer
    attribute 'id' as primary_key. References TitleType and Genre as
    foreign_key.
    """

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

    def __str__(self):
        return str(self.name) + ", id=" + str(self.id)


class TitleName(models.Model):
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


class Person(models.Model):
    """
    Person model, for information of people/performers. Stores integer
    attribute 'id' as primary key. References Profession and
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

    def __str__(self):
        return str(self.name) + ", id=" + str(self.id)


class Principal(models.Model):
    """
    Person model, for information of a Person's contribution in a
    Title. Stores auto id as primary_key References Title and
    Person as foreign_key.
    """

    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    category = models.CharField(max_length=CHAR_LENGTH)

    job = models.CharField(max_length=CHAR_LENGTH, null=True, blank=True)

    characters = models.TextField(null=True, blank=True)

    def __str__(self):
        person = self.person.name + " (" + str(self.person.id) + ")"
        title = self.title.name + " (" + str(self.title.id) + ")"
        return person + " in " + title


class Rating(models.Model):
    """
    Rating model, specifying each rating submitted in the system by any user.
    Stores auto id as primary_key. References settings.AUTH_USER_MODEL and
    Title as foreign keys.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )


class Review(models.Model):
    """
    Rating model, specifying each review submitted in the system by any user.
    Stores auto id as primary_key. References settings.AUTH_USER_MODEL and
    Title as foreign keys.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    review = models.TextField()


class Action(SimpleNameModel):
    """
    Specfies an action performed by a user
    """


class ActivityLog(models.Model):
    """
    ActivityLog model, to store every action performed by user on a title.
    Stores auto id as primary_key. References settings.AUTH_USER_MODEL,
    Title and Action as foreign keys.
    """

    user = user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    action = models.ForeignKey(Action, on_delete=models.RESTRICT)
