from django.contrib import admin

from .model_admins import (
    ActivityLogAdmin,
    CrewAdmin,
    PersonAdmin,
    PrincipalAdmin,
    RatingAdmin,
    RatingReviewAdmin,
    TitleAdmin,
)
from .models import (
    ActivityLog,
    Crew,
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

admin.site.register([TitleName, TitleType, Profession, Genre])

admin.site.register(ActivityLog, ActivityLogAdmin)
admin.site.register(Crew, CrewAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Principal, PrincipalAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Review, RatingReviewAdmin)
admin.site.register(Title, TitleAdmin)
