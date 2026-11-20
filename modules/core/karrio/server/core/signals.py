from django.conf import settings
from django.dispatch import receiver
from constance import config
from constance.signals import config_updated
from django.core.signals import request_started

from karrio.server.core.logging import logger


def register_signals():
    from django.apps import apps
    from django.contrib.auth import get_user_model
    from django.db.models.signals import post_delete, post_save

    config_updated.connect(constance_updated)
    request_started.connect(initialize_settings)
    post_delete.connect(token_changed, sender=apps.get_model("user", "Token"))
    post_save.connect(token_changed, sender=apps.get_model("user", "Token"))
    post_save.connect(user_saved, sender=get_user_model())

    logger.info("Signal registration complete", module="karrio.core")


def _forget_now_and_on_commit(keys) -> None:
    """Evict cached authentications for these token keys now, and again once the
    surrounding transaction commits. Each eviction leaves a revocation marker that
    authenticators never overwrite (they fill with cache.add), so a request that read
    the old row before the commit cannot write it back. Only a request still in flight
    TOKEN_REVOKED_TTL seconds after the commit could (core.authentication). The cache
    keys are built here, in the schema the change was made in, and reused at commit,
    so a schema switch before the commit cannot redirect the second eviction."""
    from django.db import transaction
    from karrio.server.core.authentication import revoke_cache_keys, token_cache_keys

    cache_keys = token_cache_keys(keys)
    revoke_cache_keys(cache_keys)
    transaction.on_commit(lambda: revoke_cache_keys(cache_keys))


def token_changed(sender, instance, created=False, **_kwargs):
    """A deleted or edited API token (its user or test_mode) must stop authenticating
    with the cached identity now. Also covers a deleted user: User.delete() and the
    cascade delete its tokens. A new key has nothing cached yet."""
    if created:
        return

    _forget_now_and_on_commit([instance.key])


def user_saved(sender, instance, created=False, update_fields=None, **_kwargs):
    """The cached pair carries the whole user (is_active, is_staff, is_superuser, ...),
    so any change to a user evicts their API tokens: a deactivated user must stop
    authenticating, and a demoted staff user must lose staff access, not keep it until
    the entry expires. A login-timestamp-only save changes nothing the pair carries."""
    if created or (update_fields is not None and set(update_fields) <= {"last_login"}):
        return

    _forget_now_and_on_commit(instance.tokens.values_list("key", flat=True))


def initialize_settings(_sender=None, **_kwargs):
    """Initialize Django settings from constance on first request."""
    if getattr(initialize_settings, "has_run", False):
        return

    try:
        update_settings(config)
        initialize_settings.has_run = True
    except Exception as e:
        logger.error("Failed to initialize settings", error=str(e))


@receiver(config_updated)
def constance_updated(sender, **_kwargs):
    update_settings(sender)


def _batch_fetch_constance(keys: list) -> dict:
    """Fetch all constance values in a single query.

    Returns a dict of {key: deserialized_value} for all keys found in the DB.
    Falls back to CONSTANCE_CONFIG defaults for missing keys.
    """
    try:
        from constance.models import Constance

        prefix = getattr(settings, "CONSTANCE_DATABASE_PREFIX", "")
        db_keys = [f"{prefix}{k}" for k in keys]

        rows = Constance.objects.filter(key__in=db_keys).values_list("key", "value")
        raw_map = {k.removeprefix(prefix): v for k, v in rows}

        # Deserialize using pickle (constance default) and fall back to config defaults
        import pickle  # nosec — mirrors constance's own pickle serialization for DB-stored values

        result = {}
        for key in keys:
            if key in raw_map and raw_map[key] is not None:
                try:
                    result[key] = pickle.loads(raw_map[key])  # nosec B301 — constance stores values as pickle, same pattern as constance internals
                except Exception:
                    result[key] = settings.CONSTANCE_CONFIG[key][0]
            else:
                result[key] = settings.CONSTANCE_CONFIG[key][0]

        return result
    except Exception:
        # Fallback: table doesn't exist yet (migrations not run)
        return {}


def update_settings(current):
    """Sync constance values to Django settings.

    Uses a single batch query instead of per-key lookups to avoid N+1.
    Falls back to individual getattr() if batch fetch fails.
    """
    keys = [k for k in settings.CONSTANCE_CONFIG.keys() if hasattr(settings, k)]
    email_keys = ["EMAIL_HOST", "EMAIL_HOST_USER"]
    all_keys = list(set(keys + email_keys))

    # Try batch fetch first (1 query instead of N)
    values = _batch_fetch_constance(all_keys)

    if values:
        for key in keys:
            if key in values:
                setattr(settings, key, values[key])

        settings.EMAIL_ENABLED = all(
            values.get(k) not in (None, "")
            for k in email_keys
        )
        return

    # Fallback: individual lookups (e.g., during tests or when table doesn't exist)
    for key in keys:
        try:
            setattr(settings, key, getattr(current, key))
        except Exception:
            pass

    try:
        settings.EMAIL_ENABLED = all(
            cfg not in (None, "")
            for cfg in [current.EMAIL_HOST, current.EMAIL_HOST_USER]
        )
    except Exception:
        settings.EMAIL_ENABLED = False
