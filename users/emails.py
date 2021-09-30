import logging
from smtplib import SMTPException

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .utils import password_reset_token, verification_token

logger = logging.getLogger(__name__)


def send_email(user_list, params):
    """
    Generic function to send email to users. Requires a list of user objects
    and a params dictionary containing `template` and `subject`. Params can
    optionally contain a nested `context` dictionary.
    """

    try:
        subject = params.get("subject")
        template = params.get("template")
        context = params.get("context", None)
        email_list = [user.email for user in user_list]

        email = EmailMessage(
            subject,
            render_to_string(template, context),
            settings.DEFAULT_FROM_EMAIL,
            email_list,
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
        logger.error("ERROR: SEND EMAIL TO USER", e)
        return "The server has encountered an error, please try again."


def send_verification_link(user):
    """
    Generates a verifcation link and sends and email to the user
    """

    token = verification_token.make_token(user)
    encoded_id = urlsafe_base64_encode(force_bytes(user.id))
    link = f"{settings.FRONTEND_URL}verify/#id={encoded_id}&link={token}"

    return send_email(
        [user],
        {
            "template": "user-verification-email.html",
            "subject": "Account Verification Link",
            "context": {"link": link},
        },
    )


def send_password_reset_link(user):
    """
    Generates a password reset link and sends and email to the user
    """

    token = password_reset_token.make_token(user)
    encoded_id = urlsafe_base64_encode(force_bytes(user.id))
    link = f"{settings.FRONTEND_URL}reset/#id={encoded_id}&link={token}"

    send_email(
        [user],
        {
            "template": "password-reset-email.html",
            "subject": "Password Reset Link",
            "context": {"link": link},
        },
    )


def send_login_email(user):
    """
    Sends an email to the user, alerting them of their last login. The email is
    only sent if the user's login_alert_preference is set to True.
    """

    if user.login_alert_preference:
        return send_email(
            [user],
            {
                "template": "recent-login-email.html",
                "subject": "Recent Login",
                "context": {"timestamp": user.last_login},
            },
        )


def send_registration_email(user):
    """
    Sends an email to the user, upon successful registration, containing an
    account verification link
    """

    token = verification_token.make_token(user)
    encoded_id = urlsafe_base64_encode(force_bytes(user.id))
    link = f"{settings.FRONTEND_URL}verify/#id={encoded_id}&link={token}"

    return send_email(
        [user],
        {
            "template": "user-registration-email.html",
            "subject": "Welcome to IMDb!",
            "context": {"link": link},
        },
    )


def send_password_changed_email(user):
    """
    Sends an email to the user upon a successful password change
    """

    return send_email(
        [user],
        {
            "template": "password-changed-email.html",
            "subject": "Password Changed",
        },
    )
