from django import forms
from django.views import generic
from django.conf import settings
from django.db import transaction
from django.urls import reverse_lazy, path, include
from django.views.generic.base import TemplateView
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, ValidationError
from django.utils.translation import gettext_lazy as _
from django_email_verification import send_email, urls as mail_urls


class SignUpForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ("email", "full_name")

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=commit)

        if commit and settings.EMAIL_ENABLED:
            user.is_active = False
            send_email(user)

        if commit and settings.MULTI_ORGANIZATIONS:
            from purpleserver.orgs.models import Organization
            org = Organization.objects.create(
                name=user.full_name,
                slug=user.full_name.replace(" ", "").lower(),
                is_active=not settings.EMAIL_ENABLED
            )
            # Set as organization user
            owner = org.add_user(user, is_admin=True)
            # Set as organization owner
            org.change_owner(owner)
            org.save()

        return user


class SignUp(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('registration_done')
    template_name = 'registration/signup.html'


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label=_("Email"),
        widget=forms.PasswordInput(attrs={'autofocus': True}),
    )

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'username': self.username_field.verbose_name},
        )


class LogIn(LoginView):
    form_class = LoginForm


class RegistrationDoneView(TemplateView):
    template_name = 'registration/registration_done.html'
    title = _('Successfully signed up')


class AccountDeactivateView(TemplateView):
    template_name = 'registration/account_deactivate_done.html'
    title = _('Successfully signed up')


urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', LogIn.as_view(), name='login'),

    path('registration/done/', RegistrationDoneView.as_view(), name='registration_done'),
    path('account/deactivated/', AccountDeactivateView.as_view(), name='account_deactivated'),

    path('email/', include(mail_urls)),
]
