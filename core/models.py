from django.db import models

YEAR_LENGTH = 4
CHAR_LENGTH = 255


class SimpleNameModel(models.Model):
    """
    Abstract DRY class for models which only need a primary_key name
    attribute
    """
    name = models.CharField(max_length=CHAR_LENGTH, primary_key=True)

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

    type = models.ForeignKey(
        TitleType,
        null=True,
        on_delete=models.SET_NULL,
        db_column="type"
    )

    primary_title = models.CharField(max_length=CHAR_LENGTH)
    original_title = models.CharField(max_length=CHAR_LENGTH)
    is_adult = models.BooleanField(default=False)

    start_year = models.CharField(
        max_length=YEAR_LENGTH,
        null=True,
        blank=True
    )

    end_year = models.CharField(
        max_length=YEAR_LENGTH,
        null=True,
        blank=True
    )

    runtime_minutes = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    genres = models.ManyToManyField(
        Genre,
        blank=True,
        related_name="genres",
        db_column="genre"
    )

    def __str__(self):
        return str(self.primary_title) + ', id=' + str(self.id)


class TitleName(models.Model):
    """
    TitleName model, for storing different names for a Title.
    Stores auto id as primary_key. References Title and TitleType as
    foreign_key.
    """

    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    name = models.CharField(max_length=CHAR_LENGTH)

    region = models.CharField(
        max_length=CHAR_LENGTH,
        null=True,
        blank=True
    )
    language = models.CharField(
        max_length=CHAR_LENGTH,
        null=True,
        blank=True
    )

    types = models.ManyToManyField(
        TitleType, blank=True,
        related_name="types",
        db_column="titletype"
    )
    attributes = models.ManyToManyField(
        TitleType, blank=True,
        related_name="attributes",
        db_column="attribute"
    )

    attributes = models.ManyToManyField(
        TitleType,
        blank=True,
        related_name="attributes",
        db_column="attribute"
    )
    is_original_title = models.BooleanField(default=True)


class Person(models.Model):
    """
    Person model, for information of people/performers. Stores integer
    attribute 'person_id' as primary key. References Profession and
    Title as foreign_key.
    """

    id = models.PositiveBigIntegerField(primary_key=True)
    name = models.CharField(max_length=CHAR_LENGTH)
    birth_year = models.CharField(
        max_length=YEAR_LENGTH,
        null=True,
        blank=True
    )
    death_year = models.CharField(
        max_length=YEAR_LENGTH,
        null=True,
        blank=True
    )
    professions = models.ManyToManyField(
        Profession,
        blank=True,
        related_name="professions",
        db_column="profession"
    )
    known_for_titles = models.ManyToManyField(
        Title,
        blank=True,
        related_name="known_for_titles"
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

    job = models.CharField(
        max_length=CHAR_LENGTH,
        null=True,
        blank=True
    )

    characters = models.TextField(null=True, blank=True)

    def __str__(self):
        person = self.person.name + " (" + str(self.person.id) + ")"
        title = self.title.primary_title + " (" + \
            str(self.title.id) + ")"
        return person + " in " + title
