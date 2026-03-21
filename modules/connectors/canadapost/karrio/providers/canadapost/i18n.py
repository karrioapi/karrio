"""Translation catalog for Canadapost service and option names."""

from django.utils.translation import gettext_lazy as _

SERVICE_NAME_TRANSLATIONS = {}

OPTION_NAME_TRANSLATIONS = {
    "canadapost_signature": _("Canada Post Signature"),
    "canadapost_coverage": _("Canada Post Coverage"),
    "canadapost_collect_on_delivery": _("Canada Post Collect On Delivery"),
    "canadapost_proof_of_age_required_18": _("Canada Post Proof Of Age Required 18"),
    "canadapost_proof_of_age_required_19": _("Canada Post Proof Of Age Required 19"),
    "canadapost_card_for_pickup": _("Canada Post Card For Pickup"),
    "canadapost_do_not_safe_drop": _("Canada Post Do Not Safe Drop"),
    "canadapost_leave_at_door": _("Canada Post Leave At Door"),
    "canadapost_deliver_to_post_office": _("Canada Post Deliver To Post Office"),
    "canadapost_return_at_senders_expense": _("Canada Post Return At Senders Expense"),
    "canadapost_return_to_sender": _("Canada Post Return To Sender"),
    "canadapost_abandon": _("Canada Post Abandon"),
    "canadapost_cost_center": _("Canada Post Cost Center"),
    "canadapost_submit_shipment": _("Canada Post Submit Shipment"),
    "insurance": _("Insurance"),
    "cash_on_delivery": _("Cash On Delivery"),
    "signature_confirmation": _("Signature Confirmation"),
}
