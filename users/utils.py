from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers

from .models import User


class BaseUserTokenSerializer(serializers.Serializer):
    """
    Base serializer which receives a hashed `token` and a uidb64 as `id`.
    parse_data() decodes the users_id and returns a tuple containing the
    user_id and token
    """

    token = serializers.CharField(required=True, allow_blank=False)
    id = serializers.CharField(required=True, allow_blank=False)

    def parse_data(self, data):
        token = data.get("token")
        uidb64 = data.get("id")
        user_id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=user_id)

        return user, token


class VerificationTokenGenerator(PasswordResetTokenGenerator):
    """
    Token generator used to generate user verification links. The generated
    hash value is dependent on `user.id` `user.is_active` `login_timestamp`
    and `timestamp`

    The generated link becomes invalid if either of `user.id` `user.is_active`
    `login_timestamp` change, or if the timestamp expires.
    """

    def _make_hash_value(self, user, timestamp):
        login_timestamp = (
            ""
            if user.last_login is None
            else user.last_login.replace(microsecond=0, tzinfo=None)
        )

        return (
            str(user.pk)
            + str(user.is_active)
            + str(login_timestamp)
            + str(timestamp)
        )


verification_token = VerificationTokenGenerator()
password_reset_token = PasswordResetTokenGenerator()
