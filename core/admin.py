from django.contrib import admin

from .models import (
    Genre,
    Person,
    Principal,
    Profession,
    Title,
    TitleName,
    TitleType,
)

admin.site.register(
    [Title, TitleName, TitleType, Person, Principal, Profession, Genre]
)
