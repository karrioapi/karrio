"""Translation catalog for Sendle service and option names."""

from django.utils.translation import gettext_lazy as _

SERVICE_NAME_TRANSLATIONS = {
    "sendle_standard_pickup": _("Sendle Standard Pickup"),
    "sendle_standard_dropoff": _("Sendle Standard Dropoff"),
    "sendle_express_pickup": _("Sendle Express Pickup"),
}

OPTION_NAME_TRANSLATIONS = {
    "sendle_hide_pickup_address": _("Sendle Hide Pickup Address"),
    "sendle_first_mile_option": _("Sendle First Mile Option"),
}
