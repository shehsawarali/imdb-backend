from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MinValueValidator
from django.db import models
from django_countries.fields import CountryField

from common.utils import MAX_STRING_LENGTH
from core.models import Title


class UserManager(BaseUserManager):
    """
    Manager for custom user model, to create users and superusers using email
    """

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_active", False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom user model. Removes username, first_name, and last_name fields
    inherited form AbstractUser class.
    """

    username = None
    first_name = models.CharField(max_length=MAX_STRING_LENGTH)
    last_name = models.CharField(max_length=MAX_STRING_LENGTH)
    email = models.EmailField(unique=True)
    country = CountryField()
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(18)])
    updated_at = models.DateTimeField(auto_now=True)
    follows = models.ManyToManyField(
        "User", related_name="followers", blank=True
    )
    watchlist = models.ManyToManyField(
        Title, blank=True, related_name="watchlist_set"
    )
    favorites = models.ManyToManyField(
        Title, blank=True, related_name="favorites_set"
    )
    image = models.ImageField(upload_to="user", blank=True)
    timezone = models.CharField(max_length=MAX_STRING_LENGTH, blank=True)
    login_alert_preference = models.BooleanField(default=True)
    email_list_preference = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "country", "age"]

    objects = UserManager()

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email
