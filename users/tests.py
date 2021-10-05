import copy
import json
import logging

from django.contrib.auth import get_user_model
from django.urls import reverse
from parameterized import parameterized
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

logging.disable(logging.CRITICAL)
User = get_user_model()
client_user_data = {
    "first_name": "Test",
    "last_name": "Case",
    "email": "client@test.com",
    "password": "1234",
    "age": 18,
    "country": "PK",
}


class UserRegistrationTest(APITestCase):
    """
    Tests user registration with valid and invalid inputs.
    """

    invalid_password_form = {
        "first_name": "Test",
        "last_name": "Case",
        "email": "test@case.com",
        "password": "123",
        "age": 18,
        "country": "PK",
    }

    invalid_age_form = {
        "first_name": "Test",
        "last_name": "Case",
        "email": "test@case.com",
        "password": "1234",
        "age": 17,
        "country": "PK",
    }

    url = reverse("register")

    @parameterized.expand(
        ["first_name", "last_name", "email", "password", "age", "country"]
    )
    def test_missing_parameters(self, field):
        missing_parameter_form = copy.deepcopy(client_user_data)
        missing_parameter_form.pop(field)
        response = self.client.post(self.url, missing_parameter_form)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @parameterized.expand(
        [
            (invalid_password_form, status.HTTP_400_BAD_REQUEST),
            (invalid_age_form, status.HTTP_400_BAD_REQUEST),
        ]
    )
    def test_invalid_data(self, data, expected):
        response = self.client.post(self.url, data)
        assert response.status_code == expected
        assert User.objects.count() == 0

    def test_valid_data(self):
        response = self.client.post(self.url, client_user_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.count() == 1


class UserLogin(APITestCase):
    """
    Tests user login for active users with valid and invalid credentials.
    """

    url = reverse("login")

    def setUp(self):
        user = User.objects.create_user(**client_user_data)
        user.is_active = True
        user.save()

    @parameterized.expand(
        [
            (
                {
                    "email": "fail@test.com",
                    "password": client_user_data.get("password"),
                },
                status.HTTP_400_BAD_REQUEST,
            ),
            (
                {
                    "email": client_user_data.get("email"),
                    "password": "wrong_password",
                },
                status.HTTP_400_BAD_REQUEST,
            ),
        ]
    )
    def test_invalid_credentials(self, data, expected):
        response = self.client.post(self.url, data)
        assert response.status_code == expected

    def test_valid_credentials(self):
        data = {
            "email": client_user_data.get("email"),
            "password": client_user_data.get("password"),
        }

        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_200_OK


class UnverifiedUserLogin(APITestCase):
    """
    Tests user login for inactive users.
    """

    url = reverse("login")

    def setUp(self):
        User.objects.create_user(**client_user_data)

    def test_inactive_login(self):
        data = {
            "email": client_user_data.get("email"),
            "password": client_user_data.get("password"),
        }

        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class Follow(APITestCase):
    """
    Tests following other active or inactive users.
    """

    user2_data = {
        "first_name": "User",
        "last_name": "Two",
        "email": "user2@test.com",
        "password": "1234",
        "age": 18,
        "country": "PK",
    }

    def setUp(self):
        user = User.objects.create_user(**client_user_data)
        user.is_active = True
        user.save()

        refresh = RefreshToken.for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + str(refresh.access_token)
        )

        self.user2 = User.objects.create_user(**self.user2_data)
        self.url = reverse("follow", args=[self.user2.id])

    def test_follow_unverified_user(self):
        response = self.client.post(self.url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_verified_profile(self):
        self.user2.is_active = True
        self.user2.save()

        response = self.client.post(self.url)
        assert response.status_code == status.HTTP_200_OK
        client_email = client_user_data.get("email")
        assert self.user2.followers.filter(email=client_email).exists()


class Profile(APITestCase):
    """
    Tests retrieving active and inactive profiles.
    """

    def setUp(self):
        self.user = User.objects.create_user(**client_user_data)
        self.url = reverse("user-detail", args=[self.user.id])

    def test_unverified_profile(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_verified_profile(self):
        self.user.is_active = True
        self.user.save()

        response = self.client.get(self.url)
        profile = json.loads(response.content)["profile"]

        assert response.status_code == status.HTTP_200_OK
        assert profile.get("id") is not None
        assert profile.get("email_list_preference") is None
