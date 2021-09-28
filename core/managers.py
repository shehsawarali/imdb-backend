from django.db import models
from django.db.models import Avg, F, Q


class TitleManager(models.Manager):
    """
    Manager for Title model to automatically annotate average rating
    """

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                rating=Avg(
                    F("ratings__rating"),
                    filter=Q(ratings__outdated=False),
                )
            )
        )
