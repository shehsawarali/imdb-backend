from django.contrib import admin

from .forms import OptimizeForeignKeyForm
from .models import (
    Action,
    ActivityLog,
    Genre,
    Person,
    Principal,
    Profession,
    Rating,
    Review,
    Title,
    TitleName,
    TitleType,
)


class OptimizeForeignKeyAdmin(admin.ModelAdmin):
    form = OptimizeForeignKeyForm


admin.site.register(
    [Title, TitleName, TitleType, Person, Profession, Genre, Action]
)

admin.site.register(
    [Principal, Rating, Review, ActivityLog], OptimizeForeignKeyAdmin
)
