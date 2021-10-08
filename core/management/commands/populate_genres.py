from django.core.management.base import BaseCommand

from common.utils import genres
from core.models import Genre

class Command(BaseCommand):
    help = "Populate genres"

    def handle(self, *args, **options):

        for genre in genres:
            obj, created = Genre.objects.get_or_create(
                name=genre
            )
