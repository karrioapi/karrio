"""Translation catalog for Asendia service and option names."""

from django.utils.translation import gettext_lazy as _

SERVICE_NAME_TRANSLATIONS = {
    "asendia_epaq_standard": _("Asendia e-PAQ Standard"),
    "asendia_epaq_standard_cup": _("Asendia e-PAQ Standard Cup"),
    "asendia_epaq_plus": _("Asendia e-PAQ Plus"),
    "asendia_epaq_plus_cup": _("Asendia e-PAQ Plus Cup"),
    "asendia_epaq_select": _("Asendia e-PAQ Select"),
    "asendia_epaq_elite": _("Asendia e-PAQ Elite"),
    "asendia_epaq_elite_cup": _("Asendia e-PAQ Elite Cup"),
    "asendia_epaq_go": _("Asendia e-PAQ GO"),
    "asendia_epaq_returns": _("Asendia e-PAQ Returns"),
    "asendia_epaq_returns_domestic": _("Asendia e-PAQ Returns Domestic"),
    "asendia_epaq_returns_international": _("Asendia e-PAQ International Returns"),
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
    "asendia_service_type": _("Asendia Service Type"),
    "insurance": _("Insurance"),
}
