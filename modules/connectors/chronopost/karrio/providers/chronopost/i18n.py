"""Translation catalog for Chronopost service and option names."""

from django.utils.translation import gettext_lazy as _

SERVICE_NAME_TRANSLATIONS = {
    "chronopost_retrait_bureau": _("Chronopost Retrait Bureau"),
    "chronopost_13": _("Chronopost 13"),
    "chronopost_10": _("Chronopost 10"),
    "chronopost_18": _("Chronopost 18"),
    "chronopost_relais": _("Chronopost Relais"),
    "chronopost_express_international": _("Chronopost Express International"),
    "chronopost_premium_international": _("Chronopost Premium International"),
    "chronopost_classic_international": _("Chronopost Classic International"),
}

OPTION_NAME_TRANSLATIONS = {
    "chronopost_delivery_on_monday": _("Chronopost Delivery On Monday"),
    "chronopost_delivery_on_saturday": _("Chronopost Delivery On Saturday"),
    "chronopost_delivery_normal": _("Chronopost Delivery Normal"),
    "saturday_delivery": _("Saturday Delivery"),
}
