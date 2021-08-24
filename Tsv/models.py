from django.core.validators import FileExtensionValidator
from django.db import models


class Tsv(models.Model):
    """
    Tsv model, for uploaded .tsv files.
    Stores auto id as primary_key.
    """

    file_name = models.FileField(
        upload_to="tsvs",
        validators=[FileExtensionValidator(allowed_extensions=["tsv"])],
    )

    uploaded = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)

    def __str__(self):
        return f"File id: {self.id}"
