from django.contrib import admin


class RatingReviewAdmin(admin.ModelAdmin):
    """
    Admin site settings for Rating and Review models.
    """

    raw_id_fields = (
        "user",
        "title",
    )
    list_display = ("id", "title", "user", "current")
    search_fields = ("user", "title")
    ordering = ("-id",)
    list_filter = ("outdated",)

    def current(self, instance):
        return not instance.outdated

    current.boolean = True

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class RatingAdmin(RatingReviewAdmin):
    """
    Admin site settings for Rating model. Inherits RatingReviewAdmin and appends the
    'rating' attribute in list_display.
    """

    list_display = RatingReviewAdmin.list_display + ("rating",)


class ActivityLogAdmin(admin.ModelAdmin):
    """
    Admin site settings for Activity Log model.
    """

    list_display = ("user", "title", "action", "created_at")
    search_fields = ("action", "title__name", "user__email")
    ordering = ("-created_at",)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class PrincipalAdmin(admin.ModelAdmin):
    """
    Admin site settings for Principal model.
    """

    raw_id_fields = (
        "title",
        "person",
    )
    list_display = (
        "id",
        "title",
        "person",
        "category",
    )
    search_fields = ("title__name", "person__name")
    ordering = ("-id",)


class CrewAdmin(admin.ModelAdmin):
    """
    Admin site settings for Crew model.
    """

    raw_id_fields = (
        "title",
        "writers",
        "directors",
    )
    list_display = ("title",)
    search_fields = ("title__name", "writers__name", "directors__name")
    ordering = ("-id",)


class PersonAdmin(admin.ModelAdmin):
    """
    Admin site settings for Person model.
    """

    fields = [
        "id",
        "image",
        "name",
        ("birth_year", "death_year"),
        "description",
        "professions",
        "known_for_titles",
    ]
    filter_horizontal = ("professions",)
    raw_id_fields = ("known_for_titles",)
    list_display = ("id", "name")
    search_fields = (
        "id",
        "name",
    )
    ordering = ("-id",)


class TitleAdmin(admin.ModelAdmin):
    """
    ModelAdmin for Title model.
    """

    fields = [
        "id",
        "image",
        "name",
        "type",
        ("runtime_minutes", "is_adult"),
        ("start_year", "end_year"),
        "description",
        "genres",
    ]
    filter_horizontal = ("genres",)
    list_display = ("id", "name", "start_year", "end_year", "is_adult")
    list_filter = ("is_adult",)
    search_fields = (
        "id",
        "name",
    )
    ordering = ("-id",)
