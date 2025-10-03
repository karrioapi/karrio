from functools import partial
from django.db import models
from oauth2_provider.models import Application
from django.contrib.auth import get_user_model

import karrio.server.core.utils as utils
import karrio.server.core.models as core

User = get_user_model()


@core.register_model
class OAuthApp(core.OwnedEntity):
    """
    OAuth applications created by developers for API access.
    These are NOT physical apps - they're for API integrations only.
    """
    class Meta:
        db_table = "oauth-app"
        verbose_name = "OAuth App"
        verbose_name_plural = "OAuth Apps"
        ordering = ["-created_at"]

    id = models.CharField(
        max_length=50,
        editable=False,
        primary_key=True,
        default=partial(core.uuid, prefix="app_"),
    )

    display_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    # OAuth2 application reference
    registration = models.OneToOneField(
        Application,
        on_delete=models.CASCADE,
        related_name="oauth_app"
    )

    # App configuration
    launch_url = models.URLField(max_length=500)
    redirect_uris = models.TextField()  # Stored as text, can contain multiple URIs

    # Features and metadata
    features = models.JSONField(
        blank=True,
        null=True,
        default=partial(utils.identity, value=[]),
        help_text="List of features this OAuth app supports"
    )
    metadata = models.JSONField(
        blank=True,
        null=True,
        default=partial(utils.identity, value={}),
        help_text="Additional metadata for the OAuth app"
    )

    def delete(self, *args, **kwargs):
        """Ensure OAuth2 application is deleted when app is deleted"""
        if self.registration:
            self.registration.delete()
        return super().delete(*args, **kwargs)

    @property
    def object_type(self):
        return "oauth_app"

    @property
    def client_id(self):
        return self.registration.client_id if self.registration else None

    @property
    def client_secret(self):
        return self.registration.client_secret if self.registration else None

    def __str__(self):
        return f"{self.display_name}"

    @classmethod
    def create_with_oauth_application(
        cls,
        display_name,
        launch_url,
        redirect_uris,
        user,
        description="",
        features=None,
        metadata=None,
        grant_type=None
    ):
        """
        Create an OAuth app with proper OAuth2 application configuration.

        Args:
            display_name: The app's display name
            launch_url: The app's launch URL
            redirect_uris: Newline-separated redirect URIs
            user: The user creating the app
            description: Optional app description
            features: Optional list of features
            metadata: Optional metadata dict
            grant_type: OAuth grant type (defaults to authorization_code for OAuth apps)

        Returns:
            tuple: (oauth_app, raw_client_secret)
        """
        from oauth2_provider.models import Application

        # Default to Authorization Code Flow for OAuth apps
        if grant_type is None:
            grant_type = Application.GRANT_AUTHORIZATION_CODE

        # Create OAuth2 application
        registration = Application(
            user=user,
            name=display_name,
            redirect_uris=redirect_uris,
            algorithm=Application.RS256_ALGORITHM,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=grant_type,
            skip_authorization=False,  # Require user consent
        )

        # Capture the raw client secret before saving
        raw_client_secret = registration.client_secret
        registration.save()

        # Create OAuth app
        oauth_app = cls.objects.create(
            display_name=display_name,
            description=description,
            launch_url=launch_url,
            redirect_uris=redirect_uris,
            features=features or [],
            metadata=metadata or {},
            registration=registration,
            created_by=user,
        )

        return oauth_app, raw_client_secret


@core.register_model
class AppInstallation(core.OwnedEntity):
    """
    Installation records for physical apps (from app store).
    These reference app manifests by ID, not database records.
    """
    class Meta:
        db_table = "app-installation"
        verbose_name = "App Installation"
        verbose_name_plural = "App Installations"
        ordering = ["-created_at"]
        unique_together = [["created_by", "app_id"]]  # One installation per user per app

    id = models.CharField(
        max_length=50,
        editable=False,
        primary_key=True,
        default=partial(core.uuid, prefix="ins_"),
    )

    # Physical app reference (by manifest ID, not FK)
    app_id = models.CharField(
        max_length=100,
        help_text="ID of the physical app from the app store manifest"
    )

    # App type classification
    APP_TYPE_CHOICES = [
        ('builtin', 'Built-in App'),
        ('marketplace', 'Marketplace App'),
        ('private', 'Private App'),
    ]
    app_type = models.CharField(
        max_length=20,
        choices=APP_TYPE_CHOICES,
        default='marketplace',
        help_text="Type of the installed app"
    )

    # Installation configuration
    access_scopes = models.JSONField(
        blank=True,
        null=True,
        default=partial(utils.identity, value=[]),
        help_text="Scopes granted to this app installation"
    )

    # API key for app authentication
    api_key = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True,
        help_text="Auto-generated API key for this app installation"
    )

    metadata = models.JSONField(
        blank=True,
        null=True,
        default=partial(utils.identity, value={}),
        help_text="Installation-specific metadata and settings"
    )

    # Optional OAuth app reference (only for private apps that need OAuth)
    oauth_app = models.ForeignKey(
        OAuthApp,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="installations",
        help_text="Associated OAuth app if this installation requires OAuth"
    )

    # Installation status
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this app installation is currently active"
    )

    metafields = models.ManyToManyField(
        core.Metafield,
        related_name="metafield_app_installation",
        through="AppInstallationMetafieldLink",
    )

    def save(self, *args, **kwargs):
        """Auto-generate API key if not present"""
        if not self.api_key:
            self.api_key = self.generate_api_key()
        super().save(*args, **kwargs)

    def generate_api_key(self):
        """Generate a unique API key for this installation."""
        import secrets
        prefix = f"karrio_app_{self.app_id}"
        suffix = secrets.token_urlsafe(32)
        api_key = f"{prefix}_{suffix}"

        # Ensure uniqueness
        while AppInstallation.objects.filter(api_key=api_key).exists():
            suffix = secrets.token_urlsafe(32)
            api_key = f"{prefix}_{suffix}"

        return api_key

    def rotate_api_key(self):
        """Generate a new API key for this installation."""
        self.api_key = self.generate_api_key()
        self.save(update_fields=['api_key'])
        return self.api_key

    def ensure_api_key(self):
        """Ensure this installation has an API key, creating one if missing."""
        if not self.api_key:
            self.api_key = self.generate_api_key()
            self.save(update_fields=['api_key'])
        return self.api_key

    @property
    def object_type(self):
        return "app_installation"

    @property
    def requires_oauth(self):
        """Check if this installation has an associated OAuth app"""
        return self.oauth_app is not None

    def __str__(self):
        return f"{self.app_id} installed by {self.created_by}"


"""Models automation linking (for reverse OneToMany relations)"""


class AppInstallationMetafieldLink(models.Model):
    app_installation = models.ForeignKey(
        AppInstallation, on_delete=models.CASCADE, related_name="metafields_links"
    )
    metafield = models.OneToOneField(
        core.Metafield, on_delete=models.CASCADE, related_name="app_installation_link"
    )

