from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MinValueValidator
from django.db import models
from django_countries.fields import CountryField

CHAR_LENGTH = 255


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
        extra_fields.setdefault("is_active", True)
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
    first_name = models.CharField(max_length=CHAR_LENGTH)
    last_name = models.CharField(max_length=CHAR_LENGTH)
    email = models.EmailField(unique=True)
    country = CountryField()
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(18)])
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "country", "age"]

    objects = UserManager()

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email
