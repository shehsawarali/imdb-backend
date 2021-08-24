from django import forms

from .models import Tsv


class UploadTSVForm(forms.ModelForm):
    class Meta:
        model = Tsv
        fields = ("file_name",)
