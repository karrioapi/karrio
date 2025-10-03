from django.urls import path
from two_factor.views import LoginView as BaseLoginView


class LoginView(BaseLoginView):
    template_name = "registration/login.html"


urlpatterns = [path("login/", LoginView.as_view(), name="login")]
