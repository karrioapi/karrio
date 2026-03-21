"""Translation catalog for Australiapost service and option names."""

from django.utils.translation import gettext_lazy as _

SERVICE_NAME_TRANSLATIONS = {
    "australiapost_parcel_post": _("Australia Post Parcel Post"),
    "australiapost_express_post": _("Australia Post Express Post"),
    "australiapost_parcel_post_signature": _("Australia Post Parcel Post Signature"),
    "australiapost_express_post_signature": _("Australia Post Express Post Signature"),
    "australiapost_intl_standard_pack_track": _("Australia Post INTL Standard Pack Track"),
    "australiapost_intl_standard_with_signature": _("Australia Post INTL Standard With Signature"),
    "australiapost_intl_express_merch": _("Australia Post INTL Express Merch"),
    "australiapost_intl_express_docs": _("Australia Post INTL Express Docs"),
    "australiapost_eparcel_post_returns": _("Australia Post Eparcel Post Returns"),
    "australiapost_express_eparcel_post_returns": _("Australia Post Express Eparcel Post Returns"),
}

OPTION_NAME_TRANSLATIONS = {
    "australiapost_delivery_date": _("Australia Post Delivery Date"),
    "australiapost_delivery_time_start": _("Australia Post Delivery Time Start"),
    "australiapost_delivery_time_end": _("Australia Post Delivery Time End"),
    "australiapost_pickup_date": _("Australia Post Pickup Date"),
    "australiapost_pickup_time": _("Australia Post Pickup Time"),
    "australiapost_identity_on_delivery": _("Australia Post Identity On Delivery"),
    "australiapost_print_at_depot": _("Australia Post Print At Depot"),
    "australiapost_transit_cover": _("Australia Post Transit Cover"),
    "australiapost_sameday_identity_on_delivery": _("Australia Post Sameday Identity On Delivery"),
    "australiapost_authority_to_leave": _("Australia Post Authority To Leave"),
    "australiapost_allow_partial_delivery": _("Australia Post Allow Partial Delivery"),
    "australiapost_contains_dangerous_goods": _("Australia Post Contains Dangerous Goods"),
    "insurance": _("Insurance"),
}
