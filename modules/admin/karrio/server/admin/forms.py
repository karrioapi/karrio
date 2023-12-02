import django.forms as forms
import django.db.transaction as transaction
import karrio.server.user.forms as user_forms


class CreateUserForm(user_forms.SignUpForm):
    is_staff = forms.NullBooleanField(required=False, initial=None)
    is_active = forms.NullBooleanField(required=False, initial=None)
    is_superuser = forms.NullBooleanField(required=False, initial=None)

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=commit)

        statuses = {
            k: v
            for k, v in self.cleaned_data.items()
            if k in ["is_staff", "is_active", "is_superuser"] and v is not None
        }

        for k, v in statuses.items():
            setattr(user, k, v)

        if any(statuses.keys()):
            user.save()

        user.save()

        return user
