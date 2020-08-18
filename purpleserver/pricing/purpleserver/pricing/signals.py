from django.db.models.signals import post_save, post_delete

from purpleserver.core.gateway import Rates
from purpleserver.pricing.models import Charge


def register_rate_post_processing(*_, **__):
    Rates.post_process_functions = [
        charge.apply_charge for charge in Charge.objects.all()
    ]


post_save.connect(register_rate_post_processing, sender=Charge)
post_delete.connect(register_rate_post_processing, sender=Charge)
