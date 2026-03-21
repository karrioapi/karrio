"""Translation catalog for Usps International service and option names."""

from django.utils.translation import gettext_lazy as _

SERVICE_NAME_TRANSLATIONS = {
    "usps_first_class_package_international_service": _("USPS First Class Package International Service"),
    "usps_priority_mail_international": _("USPS Priority Mail International"),
    "usps_priority_mail_express_international": _("USPS Priority Mail Express International"),
    "usps_global_express_guaranteed": _("USPS Global Express Guaranteed"),
    "usps_all": _("USPS All"),
    "product_code": _("Product Code"),
    "product_name": _("Product Name"),
}

OPTION_NAME_TRANSLATIONS = {
    "usps_hazardous_materials_class_7_radioactive_materials": _("USPS Hazardous Materials Class 7 Radioactive Materials"),
    "usps_hazardous_materials_class_9_unmarked_lithium_batteries": _("USPS Hazardous Materials Class 9 Unmarked Lithium Batteries"),
    "usps_hazardous_materials_division_6_2_biological_materials": _("USPS Hazardous Materials Division 6 2 Biological Materials"),
    "usps_hazardous_materials": _("USPS Hazardous Materials"),
    "usps_insurance_below_500": _("USPS Insurance Below 500"),
    "usps_insurance_above_500": _("USPS Insurance Above 500"),
    "usps_return_receipt": _("USPS Return Receipt"),
}
