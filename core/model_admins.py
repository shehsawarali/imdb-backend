from django import forms
from django.contrib import admin

from .models import ActivityLog, Principal, Rating, Review


class OptimizeForeignFields(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OptimizeForeignFields, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field in ["user", "title", "person"]:
                self.fields[field].widget = forms.NumberInput()


class PrincipalForm(OptimizeForeignFields):
    """
    ModelForm for Principal model. Sets widgets for Person and Title to
    NumberInput, to optimize form performance in Django Admin
    """

    class Meta:
        model = Principal
        fields = "__all__"


class RatingForm(OptimizeForeignFields):
    """
    ModelForm for Rating model. Sets widgets for User and Title to
    NumberInput, to optimize form performance in Django Admin
    """

    class Meta:
        model = Rating
        fields = "__all__"


class ReviewForm(OptimizeForeignFields):
    """
    ModelForm for Review model. Sets widgets for User and Title to
    NumberInput, to optimize form performance in Django Admin
    """

    class Meta:
        model = Review
        fields = "__all__"


class ActivityLogForm(OptimizeForeignFields):
    """
    ModelForm for ActivityLog model. Sets widgets for User and Title to
    NumberInput, to optimize form performance in Django Admin
    """

    class Meta:
        model = ActivityLog
        fields = "__all__"


class RatingAdmin(admin.ModelAdmin):
    form = RatingForm


class ReviewAdmin(admin.ModelAdmin):
    form = ReviewForm


class ActivityLogAdmin(admin.ModelAdmin):
    form = ActivityLogForm


class PrincipalAdmin(admin.ModelAdmin):
    form = PrincipalForm
