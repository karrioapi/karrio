"""DHL Parcel DE translation catalog for service and option names."""

from django.utils.translation import gettext_lazy as _

SERVICE_NAME_TRANSLATIONS = {
    "dhl_parcel_de_paket": _("DHL Paket"),
    "dhl_parcel_de_kleinpaket": _("DHL Kleinpaket"),
    "dhl_parcel_de_europaket": _("DHL Europaket"),
    "dhl_parcel_de_paket_international": _("DHL Paket International"),
    "dhl_parcel_de_warenpost_international": _("DHL Warenpost International"),
    "dhl_parcel_de_warenpost": _("DHL Warenpost"),
}

OPTION_NAME_TRANSLATIONS = {
    # Reference
    "dhl_parcel_de_reference": _("Shipment Reference"),
    # Delivery Options
    "dhl_parcel_de_preferred_neighbour": _("Preferred Neighbour"),
    "dhl_parcel_de_preferred_location": _("Preferred Location"),
    "dhl_parcel_de_named_person_only": _("Named Person Only"),
    "dhl_parcel_de_preferred_day": _("Preferred Day"),
    "dhl_parcel_de_no_neighbour_delivery": _("No Neighbour Delivery"),
    "dhl_parcel_de_bulky_goods": _("Bulky Goods"),
    "dhl_parcel_de_premium": _("Premium"),
    "dhl_parcel_de_economy": _("Economy"),
    "dhl_parcel_de_endorsement": _("Endorsement"),
    "dhl_parcel_de_visual_check_of_age": _("Visual Check of Age"),
    "dhl_parcel_de_gogreen_plus": _("GoGreen Plus"),
    # Signature
    "dhl_parcel_de_signed_for_by_recipient": _("Signed for by Recipient"),
    # Instructions
    "dhl_parcel_de_individual_sender_requirement": _("Individual Sender Requirement"),
    # Insurance
    "dhl_parcel_de_additional_insurance": _("Additional Insurance"),
    # COD
    "dhl_parcel_de_cash_on_delivery": _("Cash on Delivery"),
    # PUDO
    "dhl_parcel_de_closest_drop_point": _("Closest Drop Point"),
    "dhl_parcel_de_parcel_outlet_routing": _("Parcel Outlet Routing"),
    "dhl_parcel_de_post_number": _("Post Number"),
    "dhl_parcel_de_retail_id": _("Retail ID"),
    "dhl_parcel_de_po_box_id": _("PO Box ID"),
    # Locker
    "dhl_parcel_de_locker_id": _("Locker ID"),
    # Customs / Invoice
    "dhl_parcel_de_shipper_customs_ref": _("Shipper Customs Reference"),
    "dhl_parcel_de_consignee_customs_ref": _("Consignee Customs Reference"),
    "dhl_parcel_de_permit_no": _("Permit Number"),
    "dhl_parcel_de_attestation_no": _("Attestation Number"),
    "dhl_parcel_de_MRN": _("Movement Reference Number (MRN)"),
    "dhl_parcel_de_cost_center": _("Cost Center"),
    # Paperless
    "dhl_parcel_de_postal_delivery_duty_paid": _("Postal Delivery Duty Paid"),
    "dhl_parcel_de_has_electronic_export_notification": _("Electronic Export Notification"),
    # Return
    "dhl_parcel_de_return_enabled": _("Return Enabled"),
    "dhl_parcel_de_return_receiver_id": _("Return Receiver ID"),
    "dhl_parcel_de_return_billing_number": _("Return Billing Number"),
    "dhl_parcel_de_return_reference": _("Return Reference"),
    "dhl_parcel_de_return_service_code": _("Return Service Code"),
    # Method-level config
    "dhl_parcel_de_label_type": _("Label Type"),
    "dhl_parcel_de_profile": _("Profile"),
}
