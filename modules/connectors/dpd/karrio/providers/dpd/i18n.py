"""Translation catalog for Dpd service and option names."""

from django.utils.translation import gettext_lazy as _

SERVICE_NAME_TRANSLATIONS = {
    "dpd_cl": _("DPD Cl"),
    "dpd_express_10h": _("DPD Express 10h"),
    "dpd_express_12h": _("DPD Express 12h"),
    "dpd_express_18h_guarantee": _("DPD Express 18h Guarantee"),
    "dpd_express_b2b_predict": _("DPD Express B2b Predict"),
    "dpd_home_europe": _("DPD Home Europe"),
    "dpd_shop_europe": _("DPD Shop Europe"),
    "dpd_express_europe": _("DPD Express Europe"),
    "dpd_express_guarantee": _("DPD Express Guarantee"),
    "dpd_express_international": _("DPD Express International"),
}

OPTION_NAME_TRANSLATIONS = {
    "dpd_order_type": _("DPD Order Type"),
    "dpd_saturday_delivery": _("DPD Saturday Delivery"),
    "dpd_ex_works_delivery": _("DPD Ex Works Delivery"),
    "dpd_tyres": _("DPD Tyres"),
    "dpd_parcel_shop_delivery": _("DPD Parcel Shop Delivery"),
    "saturday_delivery": _("Saturday Delivery"),
}
