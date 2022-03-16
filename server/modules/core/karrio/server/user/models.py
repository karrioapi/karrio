import os
import binascii
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager as DefaultUserManager
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token as BaseToken

from karrio.server.core.models import ControlledAccessModel


class UserManager(DefaultUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    full_name = models.CharField(_("full name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    username = None
    first_name = None
    last_name = None

    def __str__(self):
        return self.email

    def delete(self, *args, **kwargs):
        self.tokens.all().delete()
        super().delete(*args, **kwargs)

    @property
    def object_type(self):
        return "user"


class Token(BaseToken, ControlledAccessModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tokens"
    )

    class Meta:
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")

    @property
    def pk(self):
        return self.key

    @classmethod
    def generate_key(cls):
        return f"key_{binascii.hexlify(os.urandom(16)).decode()}"

    @property
    def organization(self):
        return self.org.first() if hasattr(self, "org") else None

    @property
    def object_type(self):
        return "token"
