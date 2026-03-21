"""Translation catalog for Parcelone service and option names."""

from django.utils.translation import gettext_lazy as _

SERVICE_NAME_TRANSLATIONS = {
    "parcelone_pa1_basic": _("ParcelOne Pa1 Basic"),
    "parcelone_pa1_eco": _("ParcelOne Pa1 Eco"),
    "parcelone_pa1_premium": _("ParcelOne Pa1 Premium"),
    "parcelone_pa1_express": _("ParcelOne Pa1 Express"),
    "parcelone_dhl_paket": _("ParcelOne DHL Paket"),
    "parcelone_dhl_paket_international": _("ParcelOne DHL Paket International"),
    "parcelone_dhl_express": _("ParcelOne DHL Express"),
    "parcelone_dhl_retoure": _("ParcelOne DHL Retoure"),
    "parcelone_ups_standard": _("ParcelOne UPS Standard"),
    "parcelone_ups_express": _("ParcelOne UPS Express"),
    "parcelone_ups_express_saver": _("ParcelOne UPS Express Saver"),
}

OPTION_NAME_TRANSLATIONS = {
    "parcelone_saturday_delivery": _("ParcelOne Saturday Delivery"),
    "parcelone_return_label": _("ParcelOne Return Label"),
    "parcelone_cod": _("ParcelOne COD"),
    "parcelone_cod_currency": _("ParcelOne COD Currency"),
    "parcelone_insurance": _("ParcelOne Insurance"),
    "parcelone_insurance_currency": _("ParcelOne Insurance Currency"),
    "parcelone_notification_email": _("ParcelOne Notification Email"),
    "parcelone_notification_sms": _("ParcelOne Notification Sms"),
    "parcelone_signature": _("ParcelOne Signature"),
    "parcelone_ident_check": _("ParcelOne Ident Check"),
    "parcelone_age_check": _("ParcelOne Age Check"),
    "parcelone_personally": _("ParcelOne Personally"),
    "parcelone_neighbor_delivery": _("ParcelOne Neighbor Delivery"),
    "parcelone_no_neighbor": _("ParcelOne No Neighbor"),
    "parcelone_drop_off_point": _("ParcelOne Drop Off Point"),
    "parcelone_premium": _("ParcelOne Premium"),
    "parcelone_bulky_goods": _("ParcelOne Bulky Goods"),
    "cash_on_delivery": _("Cash On Delivery"),
    "insurance": _("Insurance"),
    "signature_required": _("Signature Required"),
    "saturday_delivery": _("Saturday Delivery"),
    "email_notification": _("Email Notification"),
}
