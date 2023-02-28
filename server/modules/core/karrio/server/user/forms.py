from django import forms
from django.db import transaction
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from karrio.server.conf import settings
from karrio.server.user.utils import send_email


class SignUpForm(UserCreationForm):
    redirect_url = forms.URLField(required=True)

    class Meta:
        model = get_user_model()
        fields = ("email", "full_name")

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
