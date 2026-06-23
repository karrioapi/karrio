import karrio.references as ref
import karrio.server.core.dynamic as core_dynamic
import karrio.server.core.utils as utils
import karrio.server.providers.models as models
from django.db.models import signals
from karrio.server.core.logging import logger


def register_signals():
    signals.post_save.connect(carrier_changed, sender=models.CarrierConnection)
    signals.post_save.connect(carrier_dynamic_cache_bust, sender=models.CarrierConnection)
    signals.post_delete.connect(carrier_dynamic_cache_bust_on_delete, sender=models.CarrierConnection)

    # Brokered connections: per-brokered cache keyed by brokered id.
    signals.post_save.connect(brokered_dynamic_cache_bust, sender=models.BrokeredConnection)
    signals.post_delete.connect(brokered_dynamic_cache_bust_on_delete, sender=models.BrokeredConnection)

    # System connections: changes flow through to every linked brokered.
    signals.post_save.connect(system_dynamic_cache_bust, sender=models.SystemConnection)
    signals.post_delete.connect(system_dynamic_cache_bust_on_delete, sender=models.SystemConnection)

    logger.info("Karrio providers signals registered")


@utils.disable_for_loaddata
def carrier_changed(sender, instance, created, raw, using, update_fields, *args, **kwargs):
    """Setup default capabilities when carrier are created."""
    if not created:
        return

    if len(instance.capabilities or []) == 0:
        instance.capabilities = ref.get_carrier_capabilities(instance.carrier_code)
        instance.save()


@utils.disable_for_loaddata
def carrier_dynamic_cache_bust(sender, instance, *args, **kwargs):
    """Drop cached dynamic metadata when the connection settings change.

    Credentials, config, or test_mode flipping all change the live catalog the
    vendor returns. Easier to bust than to track which field touched what.
    """
    core_dynamic.invalidate(str(instance.pk))


def carrier_dynamic_cache_bust_on_delete(sender, instance, *args, **kwargs):
    """Drop cached dynamic metadata when the connection is deleted."""
    core_dynamic.invalidate(str(instance.pk))


@utils.disable_for_loaddata
def brokered_dynamic_cache_bust(sender, instance, *args, **kwargs):
    """Drop cached dynamic metadata when a brokered override / enablement changes."""
    core_dynamic.invalidate(str(instance.pk))


def brokered_dynamic_cache_bust_on_delete(sender, instance, *args, **kwargs):
    """Drop cached dynamic metadata when a brokered connection is removed."""
    core_dynamic.invalidate(str(instance.pk))


@utils.disable_for_loaddata
def system_dynamic_cache_bust(sender, instance, *args, **kwargs):
    """Bust every linked brokered cache when the underlying system connection changes."""
    core_dynamic.invalidate_for_system_connection(str(instance.pk))


def system_dynamic_cache_bust_on_delete(sender, instance, *args, **kwargs):
    """Bust every linked brokered cache when the system connection is deleted.

    BrokeredConnection rows are CASCADE-deleted, but we bust the cache before
    that propagates so any in-flight reads don't repopulate from stale state.
    """
    core_dynamic.invalidate_for_system_connection(str(instance.pk))
