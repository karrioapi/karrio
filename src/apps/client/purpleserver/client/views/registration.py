from django.urls import reverse_lazy, path
from django import forms
from django.views import generic
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, ValidationError
from django.utils.translation import gettext_lazy as _


class SignUpForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ("email", "full_name")


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


class SignUp(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', LogIn.as_view(), name='login'),
]
