from django.db import models

CHAR_LENGTH = 255


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

    name = models.CharField(max_length=CHAR_LENGTH, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
