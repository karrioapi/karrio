from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from karrio.server.conf import settings
from karrio.server.user.utils import send_email


class SignUpForm(UserCreationForm):
    redirect_url = forms.URLField(required=True)

    class Meta:
        model = get_user_model()
        fields = ("email", "full_name")

    @transaction.atomic
    def save(self, commit=True):
        # Authorization for public signup is enforced at the mutation layer
        # (RegisterUserMutation) — not here, because this form is also used by
        # the admin staff-creation flow which must work even when
        # ALLOW_SIGNUP is False.
        user = super().save(commit=commit)

        if commit and settings.EMAIL_ENABLED:
            user.is_active = False
            send_email(user, self.cleaned_data["redirect_url"])

        if commit and settings.ALLOW_ADMIN_APPROVED_SIGNUP:
            user.is_active = False

        return user
