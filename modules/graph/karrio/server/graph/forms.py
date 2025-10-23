import logging
import django.forms as forms
import django.contrib.auth.forms as auth
import django.core.exceptions as exceptions
import django.contrib.auth.tokens as tokens
import django_email_verification.confirm as confirm

import karrio.server.conf as conf
import karrio.server.user.forms as user_forms

logger = logging.getLogger(__name__)


class UserRegistrationForm(user_forms.SignUpForm):
    pass


class PasswordChangeForm(auth.PasswordChangeForm):
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(user, *args, **kwargs)


class ConfirmPasswordResetForm(auth.SetPasswordForm):
    uid = forms.CharField(required=True, max_length=100)
    token = forms.CharField(required=True, max_length=100)

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(user, *args, **kwargs)

    def clean_token(self):
        token = self.cleaned_data["token"]
        valid_link = tokens.default_token_generator.check_token(self.user, token)

        if not valid_link:
            raise exceptions.ValidationError("invalid or expired url token")


class ResetPasswordRequestForm(auth.PasswordResetForm):
    redirect_url = forms.URLField()
    from_email = confirm._get_validated_field("EMAIL_FROM_ADDRESS")

    def save(self, **kwargs):
        try:
            super().save(
                **{
                    **kwargs,
                    "extra_email_context": dict(
                        app_name=conf.settings.app_name,
                        redirect_url=self.cleaned_data["redirect_url"],
                    ),
                    "email_template_name": "karrio/password_reset_email.html",
                    "from_email": self.from_email,
                }
            )
        except Exception as e:
            logger.error(f"An error occurred while sending the email: {e}")
            raise exceptions.ValidationError(
                "An error occurred while sending the email"
            )
