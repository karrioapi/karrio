"""Translation catalog for Teleship service and option names."""

from django.utils.translation import gettext_lazy as _

SERVICE_NAME_TRANSLATIONS = {
    "teleship_expedited_pickup": _("Teleship Expedited Pickup"),
    "teleship_expedited_dropoff": _("Teleship Expedited Dropoff"),
    "teleship_standard_dropoff": _("Teleship Standard Dropoff"),
    "teleship_standard_pickup": _("Teleship Standard Pickup"),
    "teleship_postal_dropoff": _("Teleship Postal Dropoff"),
    "teleship_postal_pickup": _("Teleship Postal Pickup"),
}

OPTION_NAME_TRANSLATIONS = {
    "teleship_signature_required": _("Teleship Signature Required"),
    "teleship_delivery_warranty": _("Teleship Delivery Warranty"),
    "teleship_delivery_PUDO": _("Teleship Delivery Pudo"),
    "teleship_low_carbon": _("Teleship Low Carbon"),
    "teleship_duty_tax_calculation": _("Teleship Duty Tax Calculation"),
    "teleship_customer_reference": _("Teleship Customer Reference"),
    "teleship_order_tracking_reference": _("Teleship Order Tracking Reference"),
    "teleship_commercial_invoice_reference": _("Teleship Commercial Invoice Reference"),
}
