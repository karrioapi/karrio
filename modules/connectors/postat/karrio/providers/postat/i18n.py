"""Translation catalog for Postat service and option names."""

from django.utils.translation import gettext_lazy as _

SERVICE_NAME_TRANSLATIONS = {
    "postat_standard_domestic": _("PostAT Standard Domestic"),
    "postat_express_domestic": _("PostAT Express Domestic"),
    "postat_international_standard": _("PostAT International Standard"),
    "postat_international_express": _("PostAT International Express"),
}

OPTION_NAME_TRANSLATIONS = {
    "postat_label_size": _("PostAT Label Size"),
    "postat_paper_layout": _("PostAT Paper Layout"),
    "postat_cod": _("PostAT COD"),
    "postat_cod_currency": _("PostAT COD Currency"),
    "postat_insurance": _("PostAT Insurance"),
    "postat_insurance_currency": _("PostAT Insurance Currency"),
    "postat_signature": _("PostAT Signature"),
    "postat_saturday_delivery": _("PostAT Saturday Delivery"),
    "postat_email_notification": _("PostAT Email Notification"),
    "postat_sms_notification": _("PostAT Sms Notification"),
    "postat_age_verification": _("PostAT Age Verification"),
    "cash_on_delivery": _("Cash On Delivery"),
    "insurance": _("Insurance"),
    "signature_required": _("Signature Required"),
    "saturday_delivery": _("Saturday Delivery"),
    "email_notification": _("Email Notification"),
}
