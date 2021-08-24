from django import forms

from .models import Rating


class OptimizeForeignKeyForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = "__all__"
        widgets = {
            "user": forms.NumberInput(),
            "title": forms.NumberInput(),
            "person": forms.NumberInput(),
        }
