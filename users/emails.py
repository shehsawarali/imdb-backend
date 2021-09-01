import logging
from smtplib import SMTPException

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .utils import verification_token

logger = logging.getLogger(__name__)


def send_verification_email(user):
    try:
        token = verification_token.make_token(user)
        encoded_id = urlsafe_base64_encode(force_bytes(user.id))
        link = f"{settings.FRONTEND_URL}verify/#id={encoded_id}&link={token}"
        body = render_to_string("user-verification-email.html", {"link": link})

        email = EmailMessage(
            "Account Verification Link",
            body,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        )

        email.content_subtype = "html"
        email.send(fail_silently=False)
        return None
    except (
        AttributeError,
        TypeError,
        SMTPException,
        ConnectionRefusedError,
        TemplateDoesNotExist,
    ) as e:
        logger.error("ERROR: SEND ACTIVATION EMAIL", e)
        return "The server has encountered an error, please try again."
