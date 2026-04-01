"""Translation catalog for Dhl Poland service and option names."""

from django.utils.translation import gettext_lazy as _

SERVICE_NAME_TRANSLATIONS = {}

OPTION_NAME_TRANSLATIONS = {
    "dhl_poland_delivery_in_18_22_hours": _("DHL Poland Delivery In 18 22 Hours"),
    "dhl_poland_delivery_on_saturday": _("DHL Poland Delivery On Saturday"),
    "dhl_poland_pickup_on_staturday": _("DHL Poland Pickup On Staturday"),
    "dhl_poland_insuration": _("DHL Poland Insuration"),
    "dhl_poland_collect_on_delivery": _("DHL Poland Collect On Delivery"),
    "dhl_poland_information_to_receiver": _("DHL Poland Information To Receiver"),
    "dhl_poland_return_of_document": _("DHL Poland Return Of Document"),
    "dhl_poland_proof_of_delivery": _("DHL Poland Proof Of Delivery"),
    "dhl_poland_delivery_to_neighbour": _("DHL Poland Delivery To Neighbour"),
    "dhl_poland_self_collect": _("DHL Poland Self Collect"),
    "insurance": _("Insurance"),
    "cash_on_delivery": _("Cash On Delivery"),
    "saturday_delivery": _("Saturday Delivery"),
}
