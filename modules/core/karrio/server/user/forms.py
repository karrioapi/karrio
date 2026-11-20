from django import forms
from django.db import transaction
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from karrio.server.conf import settings
from karrio.server.core import links
from karrio.server.user.utils import send_email


class SignUpForm(UserCreationForm):
    # The page the confirmation email links to. Optional, and only accepted on
    # an allowed frontend (see karrio.server.core.links).
    redirect_url = forms.CharField(required=False, strip=False)

    class Meta:
        model = get_user_model()
        fields = ("email", "full_name")

    def clean_redirect_url(self):
        # No email is sent when email is disabled, so no link is needed.
        if not settings.EMAIL_ENABLED:
            return None

        return links.email_link(
            links.CONFIRM_EMAIL_ROUTE, self.cleaned_data.get("redirect_url")
        )

    @transaction.atomic
    def save(self, commit=True):
        if settings.ALLOW_SIGNUP == False:
            raise Exception(
                "Signup is not allowed. "
                "Please contact your administrator to create an account."
            )

        user = super().save(commit=commit)

        if commit and settings.EMAIL_ENABLED:
            user.is_active = False
            send_email(user, self.cleaned_data["redirect_url"])

        if commit and settings.ALLOW_ADMIN_APPROVED_SIGNUP:
            user.is_active = False

        return user
