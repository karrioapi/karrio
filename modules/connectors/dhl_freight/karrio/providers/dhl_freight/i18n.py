"""DHL Freight translation catalog for service and option names.

Discovered at reference-response time by ``karrio.core.i18n.translate_references``
(via ``_load_carrier_i18n("dhl_freight")``). The strings are wrapped in
``gettext_lazy`` so the active-language (German) value resolves from the Django
catalog at ``karrio/apps/api/locale/de/LC_MESSAGES/django.po``.
"""

from django.utils.translation import gettext_lazy as _

SERVICE_NAME_TRANSLATIONS = {
    "dhl_freight_eurapid": _("DHL Freight Eurapid"),
    "dhl_freight_euroconnect": _("DHL Freight Euroconnect"),
    "dhl_freight_euroconnect_plus": _("DHL Freight Euroconnect Plus"),
    "dhl_freight_domestic": _("DHL Freight Domestic"),
    "dhl_freight_ftl": _("DHL Freight Full Truck Load"),
}

OPTION_NAME_TRANSLATIONS = {
    # Delivery timing
    "dhl_freight_after_12_delivery": _("Delivery After 12:00"),
    "dhl_freight_available_pickup_time": _("Available Pickup Time"),
    "dhl_freight_available_delivery_time": _("Available Delivery Time"),
    "dhl_freight_time_slot_booking_pickup": _("Pickup Time Slot Booking"),
    "dhl_freight_time_slot_booking_delivery": _("Delivery Time Slot Booking"),
    "dhl_freight_pre_advice": _("Pre-Advice"),
    # Loading services
    "dhl_freight_tail_lift_loading": _("Tail-Lift Loading"),
    "dhl_freight_tail_lift_unloading": _("Tail-Lift Unloading"),
    "dhl_freight_side_loading_pickup": _("Side Loading at Pickup"),
    "dhl_freight_side_unloading_delivery": _("Side Unloading at Delivery"),
    "dhl_freight_drop_off_by_consignor": _("Drop-Off by Consignor"),
    # Cargo conditioning
    "dhl_freight_temperature_controlled": _("Temperature Controlled"),
    "dhl_freight_dangerous_goods": _("Dangerous Goods"),
    # Financial
    "dhl_freight_insurance": _("Insurance"),
    "dhl_freight_cash_on_delivery": _("Cash on Delivery"),
    "dhl_freight_payer_code": _("Payer Code (Incoterms)"),
    "dhl_freight_payer_code_location": _("Payer Location"),
    # Accounts
    "dhl_freight_consignor_account": _("Consignor Account Number"),
    "dhl_freight_consignee_account": _("Consignee Account Number"),
    # References
    "dhl_freight_consignor_reference": _("Consignor Reference"),
    "dhl_freight_consignee_reference": _("Consignee Reference"),
    "dhl_freight_order_reference": _("Order Reference"),
    # Instructions
    "dhl_freight_pickup_instruction": _("Pickup Instruction"),
    "dhl_freight_delivery_instruction": _("Delivery Instruction"),
    # Country-specific tax references
    "dhl_freight_uit_number": _("UIT Number (Romania)"),
    "dhl_freight_ekaer_number": _("EKAER Number (Hungary)"),
    "dhl_freight_sent_number": _("SENT Number (Poland)"),
}
