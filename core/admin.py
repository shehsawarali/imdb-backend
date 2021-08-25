from django.contrib import admin

from .model_admins import (
    ActivityLogAdmin,
    PrincipalAdmin,
    RatingAdmin,
    ReviewAdmin,
)
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

admin.site.register(
    [Title, TitleName, TitleType, Person, Profession, Genre, Action]
)

admin.site.register(Rating, RatingAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Principal, PrincipalAdmin)
admin.site.register(ActivityLog, ActivityLogAdmin)
