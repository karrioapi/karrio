from django import forms
from django.contrib.auth import forms as auth
from django.core.exceptions import ValidationError
from django.contrib.auth.tokens import default_token_generator

from karrio.server.conf import settings
from karrio.server.user.forms import SignUpForm


class UserRegistrationForm(SignUpForm):
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
        valid_link = default_token_generator.check_token(self.user, token)

        if not valid_link:
            raise ValidationError("invalid or expired url token")


class ResetPasswordRequestForm(auth.PasswordResetForm):
    redirect_url = forms.URLField()

    def save(self, **kwargs):
        super().save(
            **{
                **kwargs,
                "extra_email_context": dict(
                    app_name=settings.app_name,
                    redirect_url=self.cleaned_data["redirect_url"],
                ),
                "email_template_name": "karrio/password_reset_email.html",
            }
        )
