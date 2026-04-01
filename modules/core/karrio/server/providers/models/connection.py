"""
SystemConnection and BrokeredConnection Models.

SystemConnection: Admin-managed platform-wide carrier connections.
BrokeredConnection: User's enabled instance of a SystemConnection with config overrides.

This enables a three-tier connection architecture:
1. Carrier: User/org-owned connections (full credential access)
2. SystemConnection: Platform-managed connections (admin only)
3. BrokeredConnection: User enablement of SystemConnection (config overrides only)
"""
import typing
import functools
import django.conf as conf
import django.forms as forms
import django.db.models as models
import django.core.cache as caching
from django.contrib.contenttypes.fields import GenericRelation

import karrio.lib as lib
import karrio.sdk as karrio
import karrio.api.gateway as gateway
import karrio.server.core.models as core
import karrio.server.core.fields as fields
import karrio.server.core.datatypes as datatypes


# ─────────────────────────────────────────────────────────────────────────────
# SYSTEM CONNECTION - Admin-managed platform-wide connections
# ─────────────────────────────────────────────────────────────────────────────


class SystemConnectionQuerySet(models.QuerySet):
    """QuerySet for SystemConnection with common filters."""

    def active(self):
        return self.filter(active=True)

    def for_carrier(self, carrier_code: str):
        return self.filter(carrier_code=carrier_code)


class SystemConnectionManager(models.Manager):
    """Manager for system connections."""

    def get_queryset(self):
        return (
            SystemConnectionQuerySet(self.model, using=self._db)
            .select_related("created_by", "rate_sheet")
        )

    def active(self):
        return self.get_queryset().active()


@core.register_model
class SystemConnection(models.Model):
    """
    Admin-managed platform-wide carrier connections.

    Key characteristics:
    - Created by platform admins (staff users)
    - Credentials stored but never exposed to end users
    - Users access via BrokeredConnection (enablement + config overrides)
    - Admin can disable globally, affecting all brokered connections
    """

    class Meta:
        db_table = "SystemConnection"
        verbose_name = "System Connection"
        verbose_name_plural = "System Connections"
        ordering = ["test_mode", "-created_at"]
        indexes = [
            models.Index(fields=["carrier_code", "active"]),
        ]

    objects = SystemConnectionManager()

    # ─────────────────────────────────────────────────────────────────
    # IDENTITY
    # ─────────────────────────────────────────────────────────────────
    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=functools.partial(core.uuid, prefix="car_"),
        editable=False,
    )
    carrier_code = models.CharField(
        max_length=100,
        db_index=True,
        help_text="Carrier identifier (e.g., 'dhl_express', 'fedex')",
    )
    carrier_id = models.CharField(
        max_length=150,
        db_index=True,
        help_text="Platform-defined connection identifier",
    )

    # ─────────────────────────────────────────────────────────────────
    # CREDENTIALS (Admin-managed, never exposed)
    # ─────────────────────────────────────────────────────────────────
    credentials = models.JSONField(
        default=core.field_default({}),
        help_text="Carrier API credentials (admin only)",
    )

    # ─────────────────────────────────────────────────────────────────
    # CONFIGURATION (Base config for brokered connections)
    # ─────────────────────────────────────────────────────────────────
    config = models.JSONField(
        default=core.field_default({}),
        blank=True,
        help_text="Base operational configuration",
    )

    # ─────────────────────────────────────────────────────────────────
    # CAPABILITIES & STATUS
    # ─────────────────────────────────────────────────────────────────
    capabilities = fields.MultiChoiceField(
        choices=datatypes.CAPABILITIES_CHOICES,
        default=core.field_default([]),
        help_text="Enabled carrier capabilities",
    )
    active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Enable/disable system connection (affects all brokered)",
    )
    test_mode = models.BooleanField(
        default=True,
        help_text="Toggle carrier connection mode",
    )

    # ─────────────────────────────────────────────────────────────────
    # OWNERSHIP (Track admin creator)
    # ─────────────────────────────────────────────────────────────────
    created_by = models.ForeignKey(
        conf.settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="system_connections_created",
        help_text="Admin who created this connection",
    )

    # ─────────────────────────────────────────────────────────────────
    # RATE SHEET
    # ─────────────────────────────────────────────────────────────────
    rate_sheet = models.ForeignKey(
        "SystemRateSheet",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="system_connections",
    )

    # ─────────────────────────────────────────────────────────────────
    # METADATA & TIMESTAMPS
    # ─────────────────────────────────────────────────────────────────
    metadata = models.JSONField(
        blank=True,
        null=True,
        default=core.field_default({}),
        help_text="Admin-defined metadata",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Metafields via GenericRelation
    metafields = GenericRelation(
        "core.Metafield",
        related_query_name="system_connection",
    )

    def __str__(self):
        return f"{self.carrier_code}:{self.carrier_id}"

    # ─────────────────────────────────────────────────────────────────
    # COMPUTED PROPERTIES
    # ─────────────────────────────────────────────────────────────────

    @property
    def object_type(self):
        return "system-connection"

    @property
    def ext(self) -> str:
        """Get carrier extension name for SDK lookup."""
        return (
            "generic"
            if "custom_carrier_name" in self.credentials
            else lib.failsafe(lambda: self.carrier_code) or "generic"
        )

    @property
    def carrier_name(self) -> str:
        """Alias for ext - the carrier type name."""
        return self.ext

    @property
    def display_name(self) -> str:
        """Get human-readable display name."""
        import karrio.references as references

        return (
            (self.metadata or {}).get("display_name")
            or self.credentials.get("display_name")
            or references.REFERENCES.get("carriers", {}).get(self.ext)
            or self.carrier_id
        )

    @property
    def services(self) -> typing.Optional[typing.List]:
        """Get services from linked rate sheet."""
        if self.rate_sheet is None:
            return None
        return self.rate_sheet.services.all()

    # ─────────────────────────────────────────────────────────────────
    # CREDENTIAL MANAGEMENT (Encrypted Storage)
    # ─────────────────────────────────────────────────────────────────

    def get_sensitive_fields(self) -> typing.Set[str]:
        """
        Dynamically get sensitive fields for THIS carrier.

        Uses carrier_code to look up field metadata from plugin registry.
        Each carrier plugin defines which fields are sensitive via attrs metadata.

        Returns:
            Set of sensitive field names (e.g., {'api_key', 'secret_key', 'password'})
        """
        import karrio.references as references

        # Get field metadata for this carrier's plugin
        connection_fields = references.REFERENCES.get("connection_fields", {})
        carrier_fields = connection_fields.get(self.ext, {})

        # Filter to only sensitive fields
        sensitive = {
            field_name
            for field_name, field_meta in carrier_fields.items()
            if field_meta.get("sensitive", False)
        }

        return sensitive

    def get_allowed_fields(self) -> typing.Set[str]:
        """
        Dynamically get all allowed fields for THIS carrier.

        Uses carrier_code to look up field metadata from plugin registry.

        Returns:
            Set of all allowed field names
        """
        import karrio.references as references

        connection_fields = references.REFERENCES.get("connection_fields", {})
        carrier_fields = connection_fields.get(self.ext, {})
        return set(carrier_fields.keys())

    def get_credentials(self, user_id: typing.Optional[typing.Any] = None) -> typing.Dict:
        """
        Get all credentials (transparently decrypts sensitive fields when enabled).

        When encryption is disabled, returns credentials directly from the JSON field.

        Args:
            user_id: Optional user ID for audit logging

        Returns:
            Complete credentials dict with all fields
        """
        if not getattr(conf.settings, 'SECRET_ENCRYPTION_ENABLED', False):
            return dict(self.credentials or {})

        from karrio.server.providers.credential_manager import get_credential_manager

        credential_manager = get_credential_manager()

        return credential_manager.get_system_credentials(
            system_connection_id=self.id,
            sensitive_fields=self.get_sensitive_fields(),
            user_id=user_id
        )

    def set_credentials(
        self,
        credentials_dict: typing.Dict,
        user_id: typing.Optional[typing.Any] = None
    ) -> None:
        """
        Store credentials (transparently encrypts sensitive fields when enabled).

        When encryption is disabled, stores all credentials in the JSON field.

        Args:
            credentials_dict: Raw credentials (plaintext values)
            user_id: Optional user ID for audit logging
        """
        if not getattr(conf.settings, 'SECRET_ENCRYPTION_ENABLED', False):
            self.credentials = credentials_dict
            self.save(update_fields=['credentials'])
            return

        from karrio.server.providers.credential_manager import get_credential_manager

        credential_manager = get_credential_manager()

        credential_manager.set_system_credentials(
            system_connection_id=self.id,
            credentials_dict=credentials_dict,
            sensitive_fields=self.get_sensitive_fields(),
            allowed_fields=self.get_allowed_fields(),
            user_id=user_id
        )

    # ─────────────────────────────────────────────────────────────────
    # SDK INTEGRATION
    # ─────────────────────────────────────────────────────────────────

    def _get_credentials(self) -> dict:
        """Get credentials for internal gateway use only (transparently decrypts)."""
        return self.get_credentials()

    @property
    def data(self) -> datatypes.CarrierSettings:
        """Build CarrierSettings for SDK gateway creation."""
        _computed_data: typing.Dict = dict(
            id=self.id,
            config=self.config or {},
            test_mode=self.test_mode,
            metadata=self.metadata or {},
            carrier_id=self.carrier_id,
            carrier_name=self.ext,
            display_name=self.display_name,
        )

        # Include services from rate sheet
        # Pass pre-loaded rate_sheet to get_zones/get_surcharges to avoid
        # N+1 queries (each service would otherwise query rate_sheet separately)
        _services = self.services
        if any(_services or []):
            _rate_sheet = self.rate_sheet  # Already select_related via manager
            _computed_data.update(
                services=[
                    {
                        **forms.model_to_dict(s),
                        "zones": s.get_zones(_rate_sheet=_rate_sheet),
                        "surcharges": s.get_surcharges(_rate_sheet=_rate_sheet),
                        "pricing_config": s.effective_pricing_config,
                    }
                    for s in _services
                ]
            )

        return datatypes.CarrierSettings.create(
            {**self._get_credentials(), **_computed_data}
        )

    @property
    def gateway(self) -> gateway.Gateway:
        """Create SDK gateway instance for this connection."""
        import karrio.server.core.middleware as middleware
        import karrio.server.core.config as system_config

        _context = middleware.SessionContext.get_current_request()
        _tracer = getattr(_context, "tracer", lib.Tracer())
        _cache = lib.Cache(
            caching.cache,
            version=str(self.updated_at.timestamp()),
        )
        _config = lib.SystemConfig(system_config.config)

        return karrio.gateway[self.ext].create(
            self.data.to_dict(),
            _tracer,
            _cache,
            _config,
        )


# ─────────────────────────────────────────────────────────────────────────────
# BROKERED CONNECTION - User's enabled instance of SystemConnection
# ─────────────────────────────────────────────────────────────────────────────


class BrokeredConnectionQuerySet(models.QuerySet):
    """QuerySet for BrokeredConnection with common filters."""

    def enabled(self):
        return self.filter(is_enabled=True, system_connection__active=True)

    def for_carrier(self, carrier_code: str):
        return self.filter(system_connection__carrier_code=carrier_code)

    def with_system(self):
        """Prefetch system connection and rate sheet for efficient access."""
        return self.select_related(
            "system_connection",
            "system_connection__rate_sheet",
            "created_by",
        )


class BrokeredConnectionManager(models.Manager):
    """Manager for brokered connections."""

    def get_queryset(self):
        return (
            BrokeredConnectionQuerySet(self.model, using=self._db)
            .with_system()
        )

    def enabled(self):
        return self.get_queryset().enabled()


@core.register_model
class BrokeredConnection(models.Model):
    """
    User's enabled instance of a SystemConnection.

    Key characteristics:
    - References a SystemConnection (admin-managed)
    - Can override config and carrier_id for customization
    - Never exposes credentials (uses system connection's credentials internally)
    - is_enabled controls user-level visibility
    - Effective active state = is_enabled AND system_connection.active

    Visibility:
    - OSS: Linked to created_by user
    - Insiders: Linked to organization via BrokeredConnectionLink
    """

    class Meta:
        db_table = "BrokeredConnection"
        verbose_name = "Brokered Connection"
        verbose_name_plural = "Brokered Connections"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["is_enabled"]),
        ]

    objects = BrokeredConnectionManager()

    # ─────────────────────────────────────────────────────────────────
    # IDENTITY
    # ─────────────────────────────────────────────────────────────────
    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=functools.partial(core.uuid, prefix="car_"),
        editable=False,
    )

    # ─────────────────────────────────────────────────────────────────
    # SYSTEM CONNECTION REFERENCE
    # ─────────────────────────────────────────────────────────────────
    system_connection = models.ForeignKey(
        SystemConnection,
        on_delete=models.CASCADE,
        related_name="brokered_connections",
        help_text="The system connection this is based on",
    )

    # ─────────────────────────────────────────────────────────────────
    # USER OVERRIDES
    # ─────────────────────────────────────────────────────────────────
    carrier_id = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        help_text="User-defined carrier identifier (overrides system)",
    )
    config_overrides = models.JSONField(
        default=core.field_default({}),
        blank=True,
        help_text="User-specific config overrides (merged with system config)",
    )
    capabilities_overrides = fields.MultiChoiceField(
        choices=datatypes.CAPABILITIES_CHOICES,
        default=core.field_default([]),
        blank=True,
        help_text="Override capabilities (if empty, uses system capabilities)",
    )

    # ─────────────────────────────────────────────────────────────────
    # STATUS
    # ─────────────────────────────────────────────────────────────────
    is_enabled = models.BooleanField(
        default=True,
        db_index=True,
        help_text="User-level enable/disable",
    )

    # ─────────────────────────────────────────────────────────────────
    # OWNERSHIP (OSS mode)
    # ─────────────────────────────────────────────────────────────────
    created_by = models.ForeignKey(
        conf.settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="brokered_connections",
        help_text="User who enabled this connection (OSS mode)",
    )

    # NOTE: Org linking is handled via BrokeredConnectionLink in orgs package (Insiders only)

    # ─────────────────────────────────────────────────────────────────
    # METADATA & TIMESTAMPS
    # ─────────────────────────────────────────────────────────────────
    metadata = models.JSONField(
        blank=True,
        null=True,
        default=core.field_default({}),
        help_text="User-defined metadata",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Metafields via GenericRelation
    metafields = GenericRelation(
        "core.Metafield",
        related_query_name="brokered_connection",
    )

    def __str__(self):
        return f"{self.effective_carrier_id} (via {self.system_connection_id})"

    # ─────────────────────────────────────────────────────────────────
    # COMPUTED PROPERTIES - Identity
    # ─────────────────────────────────────────────────────────────────

    @property
    def object_type(self):
        return "brokered-connection"

    @property
    def carrier_code(self) -> str:
        """Carrier code from system connection."""
        return self.system_connection.carrier_code

    @property
    def effective_carrier_id(self) -> str:
        """Get effective carrier_id (user override or system)."""
        return self.carrier_id or self.system_connection.carrier_id

    @property
    def ext(self) -> str:
        """Get carrier extension name for SDK lookup."""
        return self.system_connection.ext

    @property
    def carrier_name(self) -> str:
        """Alias for ext - the carrier type name."""
        return self.ext

    @property
    def display_name(self) -> str:
        """Get human-readable display name from system connection."""
        return self.system_connection.display_name

    @property
    def test_mode(self) -> bool:
        """Test mode from system connection."""
        return self.system_connection.test_mode

    # ─────────────────────────────────────────────────────────────────
    # COMPUTED PROPERTIES - Config & Capabilities
    # ─────────────────────────────────────────────────────────────────

    @property
    def config(self) -> dict:
        """
        Get merged config (system base + user overrides).

        Override semantics: User overrides win.
        """
        base = dict(self.system_connection.config or {})
        overrides = dict(self.config_overrides or {})
        return {**base, **overrides}

    @property
    def capabilities(self) -> list:
        """
        Get effective capabilities.

        If user has overrides, use them entirely (replacement).
        Otherwise, inherit from system connection.
        """
        overrides = list(self.capabilities_overrides or [])
        return overrides if overrides else list(self.system_connection.capabilities or [])

    @property
    def active(self) -> bool:
        """
        Effective active state.

        Requires BOTH user-enabled AND system-active.
        """
        return self.is_enabled and self.system_connection.active

    # ─────────────────────────────────────────────────────────────────
    # COMPUTED PROPERTIES - Rate Sheet & Services
    # ─────────────────────────────────────────────────────────────────

    @property
    def rate_sheet(self):
        """Get rate sheet from system connection."""
        return self.system_connection.rate_sheet

    @property
    def services(self) -> typing.Optional[typing.List]:
        """Get services from system connection's rate sheet."""
        return self.system_connection.services

    # ─────────────────────────────────────────────────────────────────
    # CREDENTIALS - SECURITY
    # ─────────────────────────────────────────────────────────────────

    @property
    def credentials(self) -> None:
        """
        Credentials are NEVER exposed through brokered connections.

        This is a security feature - users with brokered connections
        should never see the underlying system credentials.
        """
        return None

    def _get_credentials(self) -> dict:
        """Get credentials for internal gateway use only."""
        return self.system_connection._get_credentials()

    # ─────────────────────────────────────────────────────────────────
    # SDK INTEGRATION
    # ─────────────────────────────────────────────────────────────────

    @property
    def data(self) -> datatypes.CarrierSettings:
        """Build CarrierSettings for SDK gateway creation."""
        _computed_data: typing.Dict = dict(
            id=self.id,
            config=self.config,
            test_mode=self.test_mode,
            metadata=self.metadata or {},
            carrier_id=self.effective_carrier_id,
            carrier_name=self.ext,
            display_name=self.display_name,
        )

        # Include services from rate sheet
        # Pass pre-loaded rate_sheet to get_zones/get_surcharges to avoid
        # N+1 queries (each service would otherwise query rate_sheet separately)
        _services = self.services
        if any(_services or []):
            _rate_sheet = self.rate_sheet  # Already select_related via manager
            _computed_data.update(
                services=[
                    {
                        **forms.model_to_dict(s),
                        "zones": s.get_zones(_rate_sheet=_rate_sheet),
                        "surcharges": s.get_surcharges(_rate_sheet=_rate_sheet),
                        "pricing_config": s.effective_pricing_config,
                    }
                    for s in _services
                ]
            )

        return datatypes.CarrierSettings.create(
            {**self._get_credentials(), **_computed_data}
        )

    @property
    def gateway(self) -> gateway.Gateway:
        """Create SDK gateway instance for this connection."""
        import karrio.server.core.middleware as middleware
        import karrio.server.core.config as system_config

        _context = middleware.SessionContext.get_current_request()
        _tracer = getattr(_context, "tracer", lib.Tracer())
        _cache = lib.Cache(
            caching.cache,
            version=str(self.system_connection.updated_at.timestamp()),
        )
        _config = lib.SystemConfig(system_config.config)

        return karrio.gateway[self.ext].create(
            self.data.to_dict(),
            _tracer,
            _cache,
            _config,
        )
