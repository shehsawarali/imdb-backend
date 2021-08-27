import csv
import logging
from distutils.util import strtobool

from django.db.utils import IntegrityError

from core.models import (
    Genre,
    Person,
    Principal,
    Profession,
    Title,
    TitleName,
    TitleType,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def open_file_and_call_parser(file):
    """
    Opens the file and reads the file name to invoke the corresponding
    parsing function. Logs file name if there is no corresponding function

    Args:
        file: Object containing FileField of the uploaded tsv file

    Returns:
        None
    """

    with open(file.path, "r") as tsv_file:
        file_name = file.name
        reader = csv.reader(tsv_file, delimiter="\t")
        next(reader)

        if "title.basics" in file_name:
            parse_basics(reader)
        elif "name.basics" in file_name:
            parse_name_basics(reader)
        elif "title.akas" in file_name:
            parse_akas(reader)
        elif "title.principals" in file_name:
            parse_principal(reader)
        else:
            logger.info("No method defined for parsing file %s", file_name)
            raise ValueError


def normalize_title(title_id):
    """
    Converts title_id `ttxxxxxxx` into an integer

    Args:
        title_id (): string variable containing title_id

    Returns:
        title_id: integer variable containing title_id
    """

    if title_id is None or title_id == "\\N":
        return 0

    if title_id.startswith("tt"):
        title_id = title_id.removeprefix("tt")

    return int(title_id)


def normalize_person(person_id):
    """
    Converts title_id `nmxxxxxxx` into an integer

    Args:
        person_id (): string variable containing person_id

    Returns:
        person_id: integer variable containing person_id
    """

    if person_id is None or person_id == "\\N":
        return 0

    if person_id.startswith("nm"):
        person_id = person_id.removeprefix("nm")

    return int(person_id)


def read_field_data(model_fields, row):
    """
    Matches data from .tsv row to its corresponding model field

    Args:
        model_fields (): list of strings containing names of a model's
        attributes.

        row (): list containing row data from a tsv file. Each column
        corresponds to one model attribute.

    Returns:
        instance: dictionary which matches each model attribute to
        corresponding data read from row
    """

    filtered_fields = [field for field in model_fields if field != "skip"]
    instance = dict.fromkeys(filtered_fields, None)

    for index, field in enumerate(model_fields):
        if row[index] != "\\N" and field != "skip":
            instance[field] = row[index]

    return instance


def parse_basics(tsv_rows):
    """
    Parses and saves title according to `title.basics.tsv`

    Args:
        tsv_rows (): List of rows in the uploaded tsv file

    Returns:
        None
    """

    model_fields = [
        "id",
        "type",
        "name",
        "skip",
        "is_adult",
        "start_year",
        "end_year",
        "runtime_minutes",
        "genres",
    ]

    genres = None

    for row in tsv_rows:
        instance = read_field_data(model_fields, row)
        instance["id"] = normalize_title(instance["id"])

        if Title.objects.filter(id=instance["id"]).exists():
            logger.info("Duplicate Title")
            continue

        if instance["is_adult"]:
            instance["is_adult"] = strtobool(instance["is_adult"])

        if instance["type"]:
            instance["type"], _ = TitleType.objects.get_or_create(
                name=instance["type"]
            )

        if instance["genres"]:
            genres = instance["genres"].split(",")
            for index, genre in enumerate(genres):
                genres[index], _ = Genre.objects.get_or_create(name=genre)
                genres[index] = genres[index].id

        instance.pop("genres", None)

        try:
            new_title = Title.objects.create(**instance)

            if genres is not None:
                new_title.genres.add(*genres)
                new_title.save()

            logger.info("Created Title %s", instance["id"])
        except (ValueError, TypeError, IntegrityError) as error:
            logger.error(
                "Error while creating Title %s", instance["id"], error
            )


def parse_akas(tsv_rows):
    """
    Parses and saves TitleType according to `title.akas.tsv`

    Args:
        tsv_rows (): List of rows in the uploaded tsv file

    Returns:
        None
    """

    model_fields = [
        "title",
        "skip",
        "name",
        "region",
        "language",
        "types",
        "attributes",
        "is_original_title",
    ]

    types = attributes = None

    for row in tsv_rows:
        instance = read_field_data(model_fields, row)
        instance["title"] = normalize_title(instance["title"])

        if TitleName.objects.filter(
            title=instance["title"], region=instance["region"]
        ).exists():
            logger.info("Duplicate Title Name")
            continue

        title_object = Title.objects.filter(id=instance["title"])
        if title_object.exists():
            instance["title"] = title_object.first()
        else:
            logger.info("TitleName Title %s does not exist", instance["title"])
            continue

        if instance["types"]:
            types = instance["types"].split(",")
            for index, title_type in enumerate(types):
                types[index], _ = TitleType.objects.get_or_create(
                    name=title_type
                )
                types[index] = types[index].id

        if instance["attributes"]:
            attributes = instance["attributes"].split(",")
            for index, attribute in enumerate(attributes):
                attributes[index], _ = TitleType.objects.get_or_create(
                    name=attribute
                )
                attributes[index] = attributes[index].id

        # Many to many fields must be added only after object creation
        del instance["types"]
        del instance["attributes"]

        try:
            new_title_name = TitleName.objects.create(**instance)

            if types is not None:
                new_title_name.types.add(*types)

            if attributes is not None:
                new_title_name.attributes.add(*attributes)

            new_title_name.save()
            logger.info("Created TitleName %s", instance["title"])
        except (ValueError, TypeError, IntegrityError) as error:
            logger.error(
                "Error while creating TitleName %s", instance["title"], error
            )


def parse_name_basics(tsv_rows):
    """
    Parses and saves Person according to `name.basics.tsv`

    Args:
        tsv_rows (): List of rows in the uploaded tsv file

    Returns:
        None
    """

    model_fields = [
        "id",
        "name",
        "birth_year",
        "death_year",
        "professions",
        "known_for_titles",
    ]

    professions = titles = None

    for row in tsv_rows:
        instance = read_field_data(model_fields, row)
        instance["id"] = normalize_person(instance["id"])

        if Person.objects.filter(id=instance["id"]).exists():
            logger.info("Duplicate Person")
            continue

        # 5th column of a row contains the list of professions
        if instance["professions"]:
            professions = instance["professions"].split(",")

            for index, profession in enumerate(professions):
                professions[index], _ = Profession.objects.get_or_create(
                    name=profession
                )
                professions[index] = professions[index].id

        # 6th column of a row contains the list of titles
        if instance["known_for_titles"]:
            titles = []
            temp_row = instance["known_for_titles"].split(",")

            for title in temp_row:
                normalized_id = normalize_title(title)
                if Title.objects.filter(id=normalized_id).exists():
                    titles.append(normalized_id)

        # Many to many fields must be added only after object creation
        del instance["professions"]
        del instance["known_for_titles"]

        try:
            new_person = Person.objects.create(**instance)
            if professions is not None:
                new_person.professions.add(*professions)

            if titles and len(titles):
                new_person.known_for_titles.add(*titles)

            new_person.save()
            logger.info("Created Person %s", instance["id"])
        except (ValueError, TypeError, IntegrityError) as error:
            logger.error(
                "Error while creating Person %s", instance["id"], error
            )


def parse_principal(tsv_rows):
    """
    Parses and saves Principal according to `title.principals.tsv`

    Args:
        tsv_rows (): List of rows in the uploaded tsv file

    Returns:
        None
    """

    model_fields = ["title", "skip", "person", "category", "job", "characters"]

    for row in tsv_rows:
        instance = read_field_data(model_fields, row)
        instance["title"] = normalize_title(instance["title"])
        instance["person"] = normalize_person(instance["person"])

        if Principal.objects.filter(
            title=instance["title"],
            person=instance["person"],
            category=instance["category"],
        ).exists():
            logger.info("Duplicate Principal")
            continue

        title_object = Title.objects.filter(id=instance["title"])
        if title_object.exists():
            instance["title"] = title_object.first()
        else:
            logger.info("Principal Title %s does not exist", instance["title"])
            continue

        person_object = Person.objects.filter(id=instance["person"])
        if person_object.exists():
            instance["person"] = person_object.first()
        else:
            logger.info(
                "Principal Person %s does not exist", instance["person"]
            )
            continue

        try:
            Principal.objects.create(**instance)
            logger.info(
                "Created Principal for %s %s",
                instance["title"],
                instance["person"],
            )
        except (ValueError, TypeError, IntegrityError) as error:
            logger.error(
                "Error while creating Principal for %s %s",
                instance["title"],
                instance["person"],
                error,
            )
