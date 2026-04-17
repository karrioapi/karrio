"""Translation catalog for Asendia service and option names."""

from django.utils.translation import gettext_lazy as _

SERVICE_NAME_TRANSLATIONS = {
    "asendia_epaq_standard": _("Asendia Epaq Standard"),
    "asendia_epaq_standard_cup": _("Asendia Epaq Standard Cup"),
    "asendia_epaq_plus": _("Asendia Epaq Plus"),
    "asendia_epaq_plus_cup": _("Asendia Epaq Plus Cup"),
    "asendia_epaq_elite": _("Asendia Epaq Elite"),
    "asendia_epaq_elite_cup": _("Asendia Epaq Elite Cup"),
    "asendia_epaq_returns": _("Asendia Epaq Returns"),
    "asendia_epaq_returns_domestic": _("Asendia Epaq Returns Domestic"),
    "asendia_country_road": _("Asendia Country Road"),
    "asendia_country_road_plus": _("Asendia Country Road Plus"),
    "asendia_priority": _("Asendia Priority"),
    "asendia_priority_tracked": _("Asendia Priority Tracked"),
}

OPTION_NAME_TRANSLATIONS = {
    "asendia_insurance": _("Asendia Insurance"),
    "asendia_return_label": _("Asendia Return Label"),
    "asendia_return_label_type": _("Asendia Return Label Type"),
    "asendia_return_label_payment": _("Asendia Return Label Payment"),
    "asendia_sender_eori": _("Asendia Sender Eori"),
    "asendia_seller_eori": _("Asendia Seller Eori"),
    "asendia_sender_tax_id": _("Asendia Sender Tax ID"),
    "asendia_receiver_tax_id": _("Asendia Receiver Tax ID"),
    "insurance": _("Insurance"),
}
