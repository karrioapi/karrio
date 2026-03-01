"""
Secret Storage Models - Encrypted at-rest secret storage.

This module provides database models for storing encrypted secrets using
envelope encryption (DEK + KEK) with AES-256-GCM.
"""
import uuid
import django.db.models as models
import karrio.server.core.models as core


@core.register_model
class Secret(core.Entity):
    """
    System-wide encrypted secret storage.

    Stores secrets encrypted with envelope encryption:
    - DEK (Data Encryption Key) encrypts the secret value
    - KEK (Key Encryption Key) encrypts the DEK
    - Only encrypted data is stored in the database

    Attributes:
        id: UUID primary key
        name: Unique logical identifier for the secret
        ciphertext: Encrypted secret value (nonce || encrypted_data || auth_tag)
        dek_wrapped: Encrypted DEK (nonce || encrypted_dek || auth_tag)
        key_version: KEK version used for encryption
        created_at: Timestamp when secret was created
        rotated_at: Timestamp when secret was last rotated (key version changed)
    """

    class Meta:
        db_table = "secrets"
        verbose_name = "Secret"
        verbose_name_plural = "Secrets"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["name"]),  # For unique name lookups
            models.Index(fields=["key_version"]),  # For rotation queries
        ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for the secret",
    )
    name = models.TextField(
        unique=True,
        db_index=True,
        help_text="Unique logical identifier for the secret (e.g., 'carrier:uuid:api_key')",
    )
    ciphertext = models.BinaryField(
        help_text="Encrypted secret value (nonce || encrypted_data || auth_tag)",
    )
    dek_wrapped = models.BinaryField(
        help_text="Encrypted DEK (nonce || encrypted_dek || auth_tag)",
    )
    key_version = models.IntegerField(
        db_index=True,
        help_text="KEK version used for encryption",
    )
    # created_at and updated_at inherited from Entity
    rotated_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp when secret was last rotated (key version changed)",
    )

    def __str__(self):
        return f"Secret({self.name})"


@core.register_model
class CarrierSecretRef(core.Entity):
    """
    Reference table linking CarrierConnection to encrypted secrets.

    Maps carrier credential field names to their encrypted secret storage.
    This allows multiple carriers to share the same secret storage infrastructure
    while maintaining logical separation.

    Attributes:
        carrier: Foreign key to CarrierConnection
        name: Credential field name (e.g., 'api_key', 'secret_key')
        secret: Foreign key to Secret (encrypted value)
    """

    class Meta:
        db_table = "carrier_secret_refs"
        verbose_name = "Carrier Secret Reference"
        verbose_name_plural = "Carrier Secret References"
        unique_together = [
            ("carrier", "name"),  # One secret per field per carrier
        ]
        indexes = [
            models.Index(fields=["carrier", "name"]),  # For credential lookups
        ]

    carrier = models.ForeignKey(
        "CarrierConnection",
        on_delete=models.CASCADE,
        related_name="secret_refs",
        help_text="Carrier connection owning this credential",
    )
    name = models.CharField(
        max_length=255,
        help_text="Credential field name (e.g., 'api_key', 'secret_key')",
    )
    secret = models.ForeignKey(
        Secret,
        on_delete=models.CASCADE,
        related_name="carrier_refs",
        help_text="Encrypted secret value",
    )

    def __str__(self):
        return f"CarrierSecretRef({self.carrier.carrier_id}:{self.name})"


@core.register_model
class SystemSecretRef(core.Entity):
    """
    Reference table linking SystemConnection to encrypted secrets.

    Maps system connection credential field names to their encrypted secret storage.
    This allows system connections to use the same secret storage infrastructure
    as carrier connections while maintaining logical separation.

    Attributes:
        system_connection: Foreign key to SystemConnection
        name: Credential field name (e.g., 'api_key', 'secret_key', 'password')
        secret: Foreign key to Secret (encrypted value)
    """

    class Meta:
        db_table = "system_secret_refs"
        verbose_name = "System Secret Reference"
        verbose_name_plural = "System Secret References"
        unique_together = [
            ("system_connection", "name"),  # One secret per field per system connection
        ]
        indexes = [
            models.Index(fields=["system_connection", "name"]),  # For credential lookups
        ]

    system_connection = models.ForeignKey(
        "SystemConnection",
        on_delete=models.CASCADE,
        related_name="secret_refs",
        help_text="System connection owning this credential",
    )
    name = models.CharField(
        max_length=255,
        help_text="Credential field name (e.g., 'api_key', 'secret_key', 'password')",
    )
    secret = models.ForeignKey(
        Secret,
        on_delete=models.CASCADE,
        related_name="system_refs",
        help_text="Encrypted secret value",
    )

    def __str__(self):
        return f"SystemSecretRef({self.system_connection.carrier_id}:{self.name})"

