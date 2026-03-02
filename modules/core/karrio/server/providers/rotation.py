"""
Key Rotation Worker - Zero-downtime KEK rotation for encrypted secrets.

This module provides functions for rotating secrets from one KEK version to another
without downtime. Uses optimistic locking to prevent race conditions.
"""
import os
import logging
import typing
from django.db import transaction
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag

from karrio.server.providers.secret_manager import SecretManager, get_secret_manager

logger = logging.getLogger(__name__)


def rotate_batch(
    secret_manager: SecretManager,
    old_version: int,
    new_version: int,
    batch_size: int = 100,
) -> int:
    """
    Rotate a batch of secrets from old KEK to new KEK.

    Uses row-level locking (FOR UPDATE SKIP LOCKED) to allow parallel workers
    and optimistic locking (WHERE key_version = old_version) to prevent races.

    Args:
        secret_manager: SecretManager instance with KEK registry
        old_version: Current KEK version to rotate from
        new_version: Target KEK version to rotate to
        batch_size: Number of secrets to process per batch

    Returns:
        Number of secrets successfully rotated
    """
    from karrio.server.providers.models.secret import Secret
    from django.utils import timezone

    # Validate KEK versions exist
    if old_version not in secret_manager.kek_registry:
        raise ValueError(f"Old KEK version {old_version} not found in registry")
    if new_version not in secret_manager.kek_registry:
        raise ValueError(f"New KEK version {new_version} not found in registry")

    # Fetch batch with row-level locking (allows parallel workers)
    rows = list(
        Secret.objects.filter(key_version=old_version)
        .select_for_update(skip_locked=True)
        .values('id', 'dek_wrapped', 'name')[:batch_size]
    )

    if not rows:
        logger.info("No more secrets to rotate")
        return 0

    old_kek = secret_manager.kek_registry[old_version]
    new_kek = secret_manager.kek_registry[new_version]

    rotated_count = 0

    for row in rows:
        try:
            # Extract nonce and encrypted DEK
            wrapped_dek = row['dek_wrapped']
            nonce_old = wrapped_dek[:12]
            encrypted_dek = wrapped_dek[12:]

            # Unwrap DEK with old KEK
            aesgcm_old = AESGCM(old_kek)
            dek = aesgcm_old.decrypt(nonce_old, encrypted_dek, None)

            try:
                # Rewrap DEK with new KEK
                aesgcm_new = AESGCM(new_kek)
                nonce_new = os.urandom(12)
                encrypted_dek_new = aesgcm_new.encrypt(nonce_new, dek, None)

                # Prepend nonce to wrapped DEK
                new_wrapped = nonce_new + encrypted_dek_new

                # Update database with optimistic locking
                updated = Secret.objects.filter(
                    id=row['id'],
                    key_version=old_version  # Optimistic lock
                ).update(
                    dek_wrapped=new_wrapped,
                    key_version=new_version,
                    rotated_at=timezone.now()
                )

                if updated:
                    rotated_count += 1
                    logger.debug(f"Rotated secret: {row['name']}")
                else:
                    logger.warning(
                        f"Secret {row['name']} already rotated by another worker"
                    )

            finally:
                # Wipe DEK from memory
                del dek

        except InvalidTag as e:
            logger.error(
                f"Failed to decrypt secret {row['name']} with old KEK: {e}"
            )
            # Continue with next secret instead of failing entire batch
            continue
        except Exception as e:
            logger.error(f"Failed to rotate secret {row['name']}: {e}")
            # Continue with next secret instead of failing entire batch
            continue

    logger.info(f"Rotated {rotated_count}/{len(rows)} secrets in batch")
    return rotated_count


def rotate_all_secrets(
    secret_manager: typing.Optional[SecretManager] = None,
    old_version: int = None,
    new_version: int = None,
    batch_size: int = 100,
    max_iterations: int = None,
) -> dict:
    """
    Rotate all secrets from old KEK to new KEK.

    Processes secrets in batches until all are rotated or max_iterations reached.

    Args:
        secret_manager: Optional SecretManager instance (auto-created if None)
        old_version: Current KEK version to rotate from (required if secret_manager not provided)
        new_version: Target KEK version to rotate to (required if secret_manager not provided)
        batch_size: Number of secrets to process per batch
        max_iterations: Maximum number of batches to process (None = unlimited)

    Returns:
        Dict with rotation statistics:
        {
            'total_rotated': int,
            'total_failed': int,
            'batches_processed': int,
        }
    """
    if secret_manager is None:
        secret_manager = get_secret_manager()

    if secret_manager is None:
        raise ValueError(
            "Secret encryption is not enabled. "
            "Set ACTIVE_KEK_VERSIONS to enable encryption before rotating."
        )

    if old_version is None or new_version is None:
        raise ValueError("old_version and new_version must be provided")

    total_rotated = 0
    total_failed = 0
    batches_processed = 0

    while True:
        if max_iterations is not None and batches_processed >= max_iterations:
            logger.info(f"Reached max_iterations ({max_iterations}), stopping")
            break

        rotated = rotate_batch(
            secret_manager,
            old_version,
            new_version,
            batch_size
        )

        batches_processed += 1

        if rotated == 0:
            logger.info("All secrets rotated")
            break

        total_rotated += rotated

    return {
        'total_rotated': total_rotated,
        'total_failed': total_failed,
        'batches_processed': batches_processed,
    }

