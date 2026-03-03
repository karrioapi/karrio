"""
Carrier Credential Manager - Generic credential encryption for carrier connections.

This module provides a generic credential manager that works with any carrier type
by dynamically determining which fields are sensitive based on carrier plugin metadata.
"""
import logging
import typing
from uuid import UUID
from django.db import transaction
from karrio.server.providers.models.carrier import CarrierConnection
from karrio.server.providers.models.connection import SystemConnection

from karrio.server.providers.secret_manager import (
    SecretManager,
    get_secret_manager,
)
from karrio.server.providers.models.secret import CarrierSecretRef, SystemSecretRef

logger = logging.getLogger(__name__)


class CarrierCredentialManager:
    """
    Generic credential manager - works with any carrier type.

    Receives field sets as parameters. No hardcoded knowledge
    of specific carrier field names. Uses plugin metadata to determine
    which fields are sensitive.

    When encryption is disabled (no KEK configured), all credentials
    are stored in the plaintext JSON field for backward compatibility.
    """

    # Generic limits (apply to all credential types)
    MAX_CREDENTIAL_LENGTH = 10_000  # 10KB per field

    def __init__(self, secret_manager: typing.Optional[SecretManager] = None):
        """
        Initialize credential manager.

        Args:
            secret_manager: Optional SecretManager instance.
                If not provided, auto-created from settings.
                If encryption is disabled, will be None.
        """
        self.secret_manager = (
            secret_manager if secret_manager is not None
            else get_secret_manager()
        )
        self.encryption_enabled = self.secret_manager is not None

    def validate_credential(
        self,
        name: str,
        value: typing.Any,
        allowed_fields: set,
    ) -> None:
        """
        Validate credential before encryption.

        Args:
            name: Credential field name
            value: Credential value
            allowed_fields: Set of allowed field names (from calling model)

        Raises:
            ValueError: If validation fails
            TypeError: If value has wrong type
        """
        # 1. Check field name is in model's allowed list
        if name not in allowed_fields:
            raise ValueError(
                f"Unknown credential type: '{name}'. "
                f"Allowed: {', '.join(sorted(allowed_fields))}"
            )

        # 2. Validate value type
        if not isinstance(value, (str, int, bool, type(None))):
            raise TypeError(
                f"Invalid type for credential '{name}': {type(value).__name__}. "
                f"Must be str, int, bool, or None"
            )

        # 3. Skip validation for non-string values
        if not isinstance(value, str):
            return

        # 4. Check string length (prevent DOS)
        if len(value) > self.MAX_CREDENTIAL_LENGTH:
            raise ValueError(
                f"Credential '{name}' too long: {len(value)} bytes "
                f"(max {self.MAX_CREDENTIAL_LENGTH})"
            )

        # 5. Check for null bytes (database issues)
        if '\x00' in value:
            raise ValueError(f"Credential '{name}' contains null bytes")

    def get_carrier_credentials(
        self,
        carrier_id: str,
        sensitive_fields: set,
        user_id: typing.Optional[UUID] = None,
    ) -> dict:
        """
        Get all credentials (transparently decrypts sensitive fields).

        When encryption is disabled, returns credentials directly from the JSON field.

        Args:
            carrier_id: Carrier connection ID
            sensitive_fields: Set of sensitive field names (from model via plugin metadata)
            user_id: Optional user ID for audit logging

        Returns:
            Complete credentials dict with all fields
        """
        # Fallback: return plaintext credentials from JSON field
        if not self.encryption_enabled:
            try:
                carrier = CarrierConnection.objects.get(id=carrier_id)
                return dict(carrier.credentials or {})
            except CarrierConnection.DoesNotExist:
                return {}

        credentials = {}

        # Fetch encrypted credentials
        secret_refs = CarrierSecretRef.objects.filter(
            carrier_id=carrier_id,
            name__in=sensitive_fields
        ).select_related('secret')

        for ref in secret_refs:
            try:
                plaintext = self.secret_manager.read_secret(ref.secret_id)
                credentials[ref.name] = plaintext.decode('utf-8')
            except Exception as e:
                logger.error(
                    f"Failed to decrypt credential '{ref.name}' for carrier {carrier_id}: {e}"
                )
                raise

        # Fetch non-sensitive from JSONField
        try:
            carrier = CarrierConnection.objects.get(id=carrier_id)
            credentials.update(carrier.credentials or {})
        except CarrierConnection.DoesNotExist:
            logger.warning(f"Carrier {carrier_id} not found")

        return credentials

    def set_carrier_credentials(
        self,
        carrier_id: str,
        credentials_dict: dict,
        sensitive_fields: set,
        allowed_fields: set,
        user_id: typing.Optional[UUID] = None,
    ) -> None:
        """
        Store credentials (transparently encrypts sensitive fields).

        When encryption is disabled, stores all credentials in the JSON field.

        Args:
            carrier_id: Carrier connection ID
            credentials_dict: Raw credentials (plaintext values)
            sensitive_fields: Set of sensitive field names (from model via plugin metadata)
            allowed_fields: Set of allowed field names (from model via plugin metadata)
            user_id: Optional user ID for audit logging
        """
        # Fallback: store everything in JSON field
        if not self.encryption_enabled:
            CarrierConnection.objects.filter(id=carrier_id).update(
                credentials=credentials_dict
            )
            return

        non_sensitive_fields = {}

        with transaction.atomic():
            for key, value in credentials_dict.items():
                if key in sensitive_fields and value:
                    # Encrypt sensitive field
                    secret_name = f"carrier:{carrier_id}:{key}"
                    secret_id = self.secret_manager.write_secret(
                        secret_name,
                        str(value).encode('utf-8')
                    )

                    CarrierSecretRef.objects.update_or_create(
                        carrier_id=carrier_id,
                        name=key,
                        defaults={'secret_id': secret_id}
                    )
                else:
                    # Store non-sensitive
                    non_sensitive_fields[key] = value

            # Update JSONField
            CarrierConnection.objects.filter(id=carrier_id).update(
                credentials=non_sensitive_fields
            )

    def get_system_credentials(
        self,
        system_connection_id: str,
        sensitive_fields: set,
        user_id: typing.Optional[UUID] = None,
    ) -> dict:
        """
        Get all credentials for SystemConnection (transparently decrypts sensitive fields).

        When encryption is disabled, returns credentials directly from the JSON field.

        Args:
            system_connection_id: System connection ID
            sensitive_fields: Set of sensitive field names (from model via plugin metadata)
            user_id: Optional user ID for audit logging

        Returns:
            Complete credentials dict with all fields
        """
        # Fallback: return plaintext credentials from JSON field
        if not self.encryption_enabled:
            try:
                system_conn = SystemConnection.objects.values('credentials').get(id=system_connection_id)
                return dict(system_conn.get('credentials') or {})
            except SystemConnection.DoesNotExist:
                return {}

        credentials = {}

        # Fetch encrypted credentials
        secret_refs = SystemSecretRef.objects.filter(
            system_connection_id=system_connection_id,
            name__in=sensitive_fields
        ).select_related('secret')

        for ref in secret_refs:
            try:
                plaintext = self.secret_manager.read_secret(ref.secret_id)
                credentials[ref.name] = plaintext.decode('utf-8')
            except Exception as e:
                logger.error(
                    f"Failed to decrypt credential '{ref.name}' for system connection {system_connection_id}: {e}"
                )
                raise

        # Fetch non-sensitive from JSONField
        try:
            system_conn = SystemConnection.objects.values('credentials').get(id=system_connection_id)
            credentials.update(system_conn.get('credentials') or {})
        except SystemConnection.DoesNotExist:
            logger.warning(f"System connection {system_connection_id} not found")

        return credentials

    def set_system_credentials(
        self,
        system_connection_id: str,
        credentials_dict: dict,
        sensitive_fields: set,
        allowed_fields: set,
        user_id: typing.Optional[UUID] = None,
    ) -> None:
        """
        Store credentials for SystemConnection (transparently encrypts sensitive fields).

        When encryption is disabled, stores all credentials in the JSON field.

        Args:
            system_connection_id: System connection ID
            credentials_dict: Raw credentials (plaintext values)
            sensitive_fields: Set of sensitive field names (from model via plugin metadata)
            allowed_fields: Set of allowed field names (from model via plugin metadata)
            user_id: Optional user ID for audit logging
        """
        # Fallback: store everything in JSON field
        if not self.encryption_enabled:
            SystemConnection.objects.filter(id=system_connection_id).update(
                credentials=credentials_dict
            )
            return

        non_sensitive_fields = {}

        with transaction.atomic():
            for key, value in credentials_dict.items():
                if key in sensitive_fields and value:
                    # Encrypt sensitive field
                    secret_name = f"system:{system_connection_id}:{key}"
                    secret_id = self.secret_manager.write_secret(
                        secret_name,
                        str(value).encode('utf-8')
                    )

                    SystemSecretRef.objects.update_or_create(
                        system_connection_id=system_connection_id,
                        name=key,
                        defaults={'secret_id': secret_id}
                    )
                else:
                    # Store non-sensitive
                    non_sensitive_fields[key] = value

            # Update JSONField
            SystemConnection.objects.filter(id=system_connection_id).update(
                credentials=non_sensitive_fields
            )


def get_credential_manager() -> CarrierCredentialManager:
    """
    Get CarrierCredentialManager instance.

    Returns:
        CarrierCredentialManager instance
    """
    return CarrierCredentialManager()

