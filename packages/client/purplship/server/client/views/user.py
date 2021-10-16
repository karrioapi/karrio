from django.views import generic
from django.urls import reverse_lazy, path, include
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView
from django.utils.translation import gettext_lazy as _

from purplship.server.user.forms import SignUpForm, LoginForm


class SignUp(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("registration_done")
    template_name = "registration/signup.html"


class LogIn(LoginView):
    form_class = LoginForm


class RegistrationDoneView(TemplateView):
    template_name = "registration/registration_done.html"
    title = _("Successfully signed up")


class AccountDeactivateView(TemplateView):
    template_name = "registration/account_deactivate_done.html"
    title = _("Successfully signed up")


urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("signup/", SignUp.as_view(), name="signup"),
    path("login/", LogIn.as_view(), name="login"),
    path(
        "registration/done/", RegistrationDoneView.as_view(), name="registration_done"
    ),
    path(
        "account/deactivated/",
        AccountDeactivateView.as_view(),
        name="account_deactivated",
    ),
]
