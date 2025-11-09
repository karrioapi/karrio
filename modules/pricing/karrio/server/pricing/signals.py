import functools
import importlib
from django.db.models import Q

from karrio.server.serializers import Context
from karrio.server.core.gateway import Rates
from karrio.server.core.logging import logger
import karrio.server.pricing.models as models


def register_rate_post_processing(*args, **kwargs):
    Rates.post_process_functions += [apply_custom_surcharges]
    logger.info("Signal registration complete", module="karrio.pricing")


def apply_custom_surcharges(context: Context, result):
    _filters = tuple()

    if importlib.util.find_spec("karrio.server.orgs") is not None:
        _filters += (
            Q(active=True, org__id=getattr(context.org, "id", None))
            | Q(active=True, org=None),
        )
    else:
        _filters += (Q(active=True),)

    charges = models.Surcharge.objects.filter(*_filters)

    return functools.reduce(
        lambda cummulated_result, charge: charge.apply_charge(cummulated_result),
        charges,
        result,
    )
