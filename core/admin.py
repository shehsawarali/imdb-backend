from django.contrib import admin

from .models import (
    Title,
    TitleName,
    TitleType,
    Person,
    Principal,
    Profession,
    Genre,
)

admin.site.register([
    Title,
    TitleName,
    TitleType,
    Person,
    Principal,
    Profession,
    Genre
])
