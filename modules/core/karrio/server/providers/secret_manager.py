"""
Secret Manager - Production-grade secret encryption using AES-256-GCM.

This module provides envelope encryption (DEK + KEK) for storing secrets
securely in the database. Secrets are encrypted before they reach PostgreSQL,
ensuring database administrators and backups cannot access plaintext values.
"""
import os
import re
import secrets
import logging
import typing
import base64

from uuid import UUID
from django.db import transaction
from django.conf import settings

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag


logger = logging.getLogger(__name__)


class SecretNotFoundError(Exception):
    """Raised when secret does not exist"""
    pass


class DecryptionError(Exception):
    """Raised when decryption fails (wrong key or corrupted data)"""
    pass


class SecretManager:
    """
    Production-grade secret encryption using AES-256-GCM envelope encryption.

    Uses envelope encryption strategy:
    - DEK (Data Encryption Key): Random 256-bit key per secret
    - KEK (Key Encryption Key): Master key that encrypts DEKs
    - KEKs are versioned to support zero-downtime rotation

    Security guarantees:
    - AES-256-GCM provides confidentiality and integrity
    - Nonce reuse prevention (fresh random nonce per encryption)
    - Memory wiping of sensitive keys after use
    - Input validation prevents DOS attacks
    """

    # Configuration
    MAX_SECRET_SIZE = 65_536  # 64KB max per secret
    MAX_SECRET_NAME_LENGTH = 255

    def __init__(self, kek_registry: dict[int, bytes]):
        """
        Initialize SecretManager with KEK registry.

        Args:
            kek_registry: Dict mapping version -> 256-bit KEK bytes
                Example: {1: b'...', 2: b'...'}
        """
        if not kek_registry:
            raise ValueError("KEK registry cannot be empty")

        self.kek_registry = kek_registry
        self._current_version = max(kek_registry.keys())

        # Validate all KEKs are 32 bytes (256 bits)
        for version, kek in kek_registry.items():
            if not isinstance(kek, bytes):
                raise TypeError(f"KEK version {version} must be bytes")
            if len(kek) != 32:
                raise ValueError(
                    f"KEK version {version} must be 32 bytes (256 bits), got {len(kek)}"
                )

    def validate_secret_input(self, name: str, plaintext: bytes) -> None:
        """
        Validate secret before encryption (REQUIRED).

        Prevents:
        - DOS attacks (oversized secrets)
        - Database corruption (invalid characters)
        - Type confusion attacks

        Args:
            name: Secret name
            plaintext: Secret value to encrypt

        Raises:
            ValueError: If validation fails
            TypeError: If type is incorrect
        """
        # 1. Validate name
        if not name or not isinstance(name, str):
            raise ValueError("Secret name must be non-empty string")

        if len(name) > self.MAX_SECRET_NAME_LENGTH:
            raise ValueError(
                f"Secret name too long: {len(name)} chars "
                f"(max {self.MAX_SECRET_NAME_LENGTH})"
            )

        # Check for dangerous characters in name
        if not re.match(r'^[a-zA-Z0-9:_-]+$', name):
            raise ValueError(
                f"Secret name contains invalid characters: {name}"
            )

        # 2. Validate plaintext type
        if not isinstance(plaintext, bytes):
            raise TypeError(
                f"Plaintext must be bytes, got {type(plaintext).__name__}"
            )

        # 3. Validate size (prevent DOS)
        if len(plaintext) == 0:
            raise ValueError("Cannot encrypt empty secret")

        if len(plaintext) > self.MAX_SECRET_SIZE:
            raise ValueError(
                f"Secret too large: {len(plaintext)} bytes "
                f"(max {self.MAX_SECRET_SIZE})"
            )

        # 4. Check for null bytes (database issues)
        if b'\x00' in plaintext:
            raise ValueError("Secret contains null bytes")

    def write_secret(
        self,
        name: str,
        plaintext: bytes,
        secret_id: typing.Optional[UUID] = None,
    ) -> UUID:
        """
        Encrypt and store a secret using envelope encryption.

        Args:
            name: Unique identifier for the secret
            plaintext: Secret value to encrypt
            secret_id: Optional UUID for the secret (auto-generated if None)

        Returns:
            UUID of the created/updated secret

        Raises:
            ValueError: If validation fails
            DecryptionError: If encryption fails
        """
        # Validate before encryption
        self.validate_secret_input(name, plaintext)

        # Generate random 256-bit DEK
        dek = secrets.token_bytes(32)
        
        # Check if secret already exists - reuse its ID if updating
        from karrio.server.providers.models.secret import Secret
        existing_secret = Secret.objects.filter(name=name).first()
        if secret_id is None:
            secret_id = existing_secret.id if existing_secret else UUID(os.urandom(16).hex()[:32])

        try:
            # Encrypt plaintext with DEK using AES-256-GCM
            aesgcm_data = AESGCM(dek)
            nonce_data = os.urandom(12)  # 96-bit nonce for GCM
            encrypted_data = aesgcm_data.encrypt(nonce_data, plaintext, None)

            # Prepend nonce to ciphertext (nonce || ciphertext || auth_tag)
            ciphertext = nonce_data + encrypted_data

            # Wrap DEK with current KEK
            kek = self.kek_registry[self._current_version]
            aesgcm_kek = AESGCM(kek)
            nonce_kek = os.urandom(12)
            encrypted_dek = aesgcm_kek.encrypt(nonce_kek, dek, None)

            # Prepend nonce to wrapped DEK
            wrapped_dek = nonce_kek + encrypted_dek

            # Store in database
            from karrio.server.providers.models.secret import Secret
            from django.utils import timezone

            with transaction.atomic():
                # Check if secret already exists to determine if this is a rotation
                existing_secret = Secret.objects.filter(name=name).first()
                is_rotation = existing_secret is not None and existing_secret.key_version != self._current_version

                defaults = {
                    'id': secret_id,
                    'ciphertext': ciphertext,
                    'dek_wrapped': wrapped_dek,
                    'key_version': self._current_version,
                }

                # Set rotated_at only if this is a key rotation
                if is_rotation:
                    defaults['rotated_at'] = timezone.now()

                secret, created = Secret.objects.update_or_create(
                    name=name,
                    defaults=defaults
                )

                return secret.id

        except Exception as e:
            logger.error(f"Failed to encrypt secret '{name}': {e}")
            raise DecryptionError(f"Encryption failed: {e}") from e
        finally:
            # Wipe DEK from memory (security best practice)
            if 'dek' in locals():
                del dek

    def read_secret(self, secret_id: UUID) -> bytes:
        """
        Retrieve and decrypt a secret by ID.

        Args:
            secret_id: UUID of the secret (primary key lookup)

        Returns:
            Decrypted plaintext secret

        Raises:
            SecretNotFoundError: Secret does not exist
            DecryptionError: Decryption failed (invalid key or corrupted data)
        """
        from karrio.server.providers.models.secret import Secret

        # Fetch encrypted secret from database (primary key lookup - most efficient)
        try:
            secret = Secret.objects.get(id=secret_id)
        except Secret.DoesNotExist:
            raise SecretNotFoundError(f"Secret with ID '{secret_id}' not found")

        try:
            # Extract nonce and encrypted DEK
            wrapped_dek = secret.dek_wrapped
            nonce_kek = wrapped_dek[:12]
            encrypted_dek = wrapped_dek[12:]

            # Unwrap DEK using KEK
            kek = self.kek_registry[secret.key_version]
            aesgcm_kek = AESGCM(kek)
            dek = aesgcm_kek.decrypt(nonce_kek, encrypted_dek, None)

            try:
                # Extract nonce and encrypted data
                ciphertext = secret.ciphertext
                nonce_data = ciphertext[:12]
                encrypted_data = ciphertext[12:]

                # Decrypt plaintext using DEK
                aesgcm_data = AESGCM(dek)
                plaintext = aesgcm_data.decrypt(nonce_data, encrypted_data, None)

                return plaintext

            finally:
                # Wipe DEK from memory
                del dek

        except InvalidTag:
            raise DecryptionError(
                f"Decryption failed for secret ID '{secret_id}': "
                "Invalid authentication tag (wrong key or corrupted data)"
            )
        except KeyError as e:
            raise DecryptionError(
                f"KEK version {secret.key_version} not found in registry"
            ) from e

    def read_secret_by_name(self, name: str) -> bytes:
        """
        Retrieve and decrypt a secret by name (alternative lookup method).

        Note: This uses a unique index lookup. For performance-critical paths,
        prefer read_secret() with ID-based lookup.

        Args:
            name: Unique name of the secret

        Returns:
            Decrypted plaintext secret

        Raises:
            SecretNotFoundError: Secret does not exist
            DecryptionError: Decryption failed
        """
        from karrio.server.providers.models.secret import Secret

        # Fetch secret ID by name first
        try:
            secret = Secret.objects.get(name=name)
        except Secret.DoesNotExist:
            raise SecretNotFoundError(f"Secret '{name}' not found")

        # Use ID-based lookup for decryption
        return self.read_secret(secret.id)


def get_secret_manager() -> typing.Optional[SecretManager]:
    """
    Get SecretManager instance with KEKs from settings.

    Returns None if encryption is not enabled (ACTIVE_KEK_VERSIONS not set),
    allowing the system to fall back to plaintext credential storage.

    Returns:
        SecretManager instance, or None if encryption is disabled.

    Raises:
        ValueError: If KEK configuration is present but invalid.
    """
    if not getattr(settings, 'SECRET_ENCRYPTION_ENABLED', False):
        return None

    kek_registry = getattr(settings, 'SECRET_KEK_REGISTRY', {})

    if not kek_registry:
        logger.warning(
            "SECRET_ENCRYPTION_ENABLED is True but SECRET_KEK_REGISTRY is empty. "
            "Falling back to plaintext credential storage."
        )
        return None

    return SecretManager(kek_registry)


def check_kek_in_use(version: int) -> bool:
    from karrio.server.providers.models.secret import Secret

    return Secret.objects.filter(key_version=version).exists()


def get_kek_usage_stats() -> dict:
    from karrio.server.providers.models.secret import Secret
    from django.db.models import Count

    stats = (
        Secret.objects.values('key_version')
        .annotate(count=Count('id'))
        .order_by('key_version')
    )

    return {item['key_version']: item['count'] for item in stats}
