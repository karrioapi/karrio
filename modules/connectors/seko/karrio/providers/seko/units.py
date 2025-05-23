import karrio.lib as lib
import karrio.core.units as units


class LabelType(lib.Enum):
    LABEL_PDF = ("PDF", "LABEL_PDF")
    LABEL_PNG_100X150 = ("PNG", "LABEL_PNG_100X150")
    LABEL_PNG_100X175 = ("PNG", "LABEL_PNG_100X175")
    LABEL_PDF_100X175 = ("PDF", "LABEL_PDF_100X175")
    LABEL_PDF_100X150 = ("PDF", "LABEL_PDF_100X150")
    LABEL_ZPL_100X175 = ("ZPL", "LABEL_ZPL_100X175")
    LABEL_ZPL_100X150 = ("ZPL", "LABEL_ZPL_100X150")

    """ Unified Label type mapping """
    PDF = LABEL_PDF_100X150
    ZPL = LABEL_ZPL_100X150
    PNG = LABEL_PNG_100X150


class PackagingType(lib.StrEnum):
    """Carrier specific packaging type"""

    Bag = "Bag"
    Box = "Box"
    Carton = "Carton"
    Container = "Container"
    Crate = "Crate"
    Envelope = "Envelope"
    Pail = "Pail"
    Pallet = "Pallet"
    Satchel = "Satchel"
    Tube = "Tube"
    Custom = "Custom"

    """ Unified Packaging type mapping """
    envelope = Envelope
    pak = Satchel
    tube = Tube
    pallet = Pallet
    small_box = Box
    medium_box = Carton
    your_packaging = Custom


class ShippingService(lib.StrEnum):
    """Carrier specific services"""

    seko_ecommerce_standard_tracked = "eCommerce Standard Tracked"
    seko_ecommerce_express_tracked = "eCommerce Express Tracked"
    seko_domestic_express = "Domestic Express"
    seko_domestic_standard = "Domestic Standard"
    seko_domestic_large_parcel = "Domestic Large Parcel"


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    seko_carrier = lib.OptionEnum("Carrier")
    seko_ship_type = lib.OptionEnum("ShipType")
    seko_package_id = lib.OptionEnum("PackageId")
    seko_destination_id = lib.OptionEnum("DestinationId")
    seko_product_category = lib.OptionEnum("ProductCategory")
    origin_instructions = lib.OptionEnum("OriginInstructions")
    destination_instructions = lib.OptionEnum("DestinationInstructions")
    seko_is_saturday_delivery = lib.OptionEnum("IsSaturdayDelivery", bool)
    seko_is_signature_required = lib.OptionEnum("IsSignatureRequired", bool)
    seko_send_tracking_email = lib.OptionEnum("SendTrackingEmail", bool)
    seko_amount_collected = lib.OptionEnum("AmountCollected", float)
    seko_tax_collected = lib.OptionEnum("TaxCollected", bool)
    seko_cod_amount = lib.OptionEnum("CODAmount", float)
    seko_reference_2 = lib.OptionEnum("Reference2")
    seko_reference_3 = lib.OptionEnum("Reference3")
    seko_invoice_data = lib.OptionEnum("InvoiceData")
    seko_origin_id = lib.OptionEnum("OriginId", int)
    seko_print_to_printer = lib.OptionEnum("PrintToPrinter", bool)
    seko_cif_value = lib.OptionEnum("CIFValue", float)
    seko_freight_value = lib.OptionEnum("FreightValue", float)
    seko_send_label = lib.OptionEnum("SendLabel", bool)

    """ Unified Option type mapping """
    saturday_delivery = seko_is_saturday_delivery
    signature_required = seko_is_signature_required
    email_notification = seko_send_tracking_email
    doc_files = lib.OptionEnum("doc_files", lib.to_dict)
    doc_references = lib.OptionEnum("doc_references", lib.to_dict)


def shipping_options_initializer(
    options: dict,
    package_options: units.ShippingOptions = None,
) -> units.ShippingOptions:
    """
    Apply default values to the given options.
    """

    if package_options is not None:
        options.update(package_options.content)

    def items_filter(key: str) -> bool:
        return key in ShippingOption  # type: ignore

    return units.ShippingOptions(options, ShippingOption, items_filter=items_filter)


class CustomsOption(lib.Enum):
    XIEORINumber = lib.OptionEnum("XIEORINumber")
    IOSSNUMBER = lib.OptionEnum("IOSSNUMBER")
    GBEORINUMBER = lib.OptionEnum("GBEORINUMBER")
    VOECNUMBER = lib.OptionEnum("VOECNUMBER")
    VATNUMBER = lib.OptionEnum("VATNUMBER")
    VENDORID = lib.OptionEnum("VENDORID")
    NZIRDNUMBER = lib.OptionEnum("NZIRDNUMBER")
    SWISS_VAT = lib.OptionEnum("SWISS VAT")
    OVRNUMBER = lib.OptionEnum("OVRNUMBER")
    EUEORINumber = lib.OptionEnum("EUEORINumber")
    EUVATNumber = lib.OptionEnum("EUVATNumber")
    LVGRegistrationNumber = lib.OptionEnum("LVGRegistrationNumber")

    """ Unified Customs Identifier type mapping """

    ioss = IOSSNUMBER
    nip_number = VATNUMBER
    eori_number = EUEORINumber


class TrackingStatus(lib.Enum):
    pending = [
        "OP-1",  # Pending
        "OP-8",  # Manifest Received by Carrier
        "OP-9",  # Not yet received by carrier
        "OP-11",  # Received by carrier – no manifest sent
        "OP-12",  # Collection request received by carrier
    ]
    on_hold = [
        "OP-26",  # Held by carrier
        "OP-2",  # Held at Export Hub
        "OP-6",  # Customs held for inspection and clearance
        "OP-49",  # Held by Delivery Courier
        "OP-70",  # Parcel Blocked
        "OP-87",  # Aged Parcel - High Value Unpaid
        "OP-88",  # Held at Export Hub - Additional Payment Required
        "OP-41",  # Incorrect details declared by sender
        "OP-36",  # Delivery arranged with receiver
        "OP-39",  # Package repacked
        "OP-44",  # Selected for redelivery
        "OP-46",  # Customer Enquiry lodged
        "OP-52",  # Parcel Redirection Requested
        "OP-53",  # Parcel Redirected
        "OP-91",  # Parcel Blocked - Declared LIT
    ]
    delivered = [
        "OP-71",  # Delivered in part
        "OP-72",  # Delivered
        "OP-73",  # Delivered to neighbour
        "OP-74",  # Delivered - Authority to Leave / Safe Drop
        "OP-75",  # Delivered - Parcel Collected
        "OP-76",  # Delivered to locker/collection point
        "OP-77",  # Delivered to alternate delivery point
    ]
    in_transit = [
        "OP-18",  # In transit
        "OP-20",  # Sub-contractor update
        "OP-22",  # Received by Sub-contractor
        "OP-3",  # Processed through Export Hub
        "OP-4",  # International transit to destination country
        "OP-5",  # Customs cleared
        "OP-47",  # Processed through Sorting Facility
        "OP-50",  # Parcel arrived to courier processing facility
        "OP-51",  # Parcel departed courier processing facility
        "OP-78",  # Flight Arrived
        "OP-79",  # InTransit
        "OP-80",  # Reshipped
        "OP-81",  # Flight Departed
        "OP-7",  # Picked up by Delivery Courier
        "OP-10",  # Received by carrier
        "OP-14",  # Parcel received and accepted
        "OP-31",  # Information
        "OP-32",  # Information
        "OP-33",  # Collected from sender
        "OP-48",  # With Delivery Courier
        "OP-82",  # Inbound freight received
        "OP-83",  # Delivery exception
        "OP-84",  # Recipient not available
        "OP-89",  # Collected from sender
        "OP-54",  # Transferred to Collection Point
        "OP-56",  # Transferred to delivery provider
    ]
    delivery_failed = [
        "OP-24",  # Attempted Delivery - Receiver carded
        "OP-27",  # Attempted Delivery - Customer not known at address
        "OP-28",  # Attempted Delivery - Refused by customer
        "OP-29",  # Return to sender
        "OP-30",  # Non delivery
        "OP-37",  # Attempted Delivery - No access to receivers address
        "OP-38",  # Attempted Delivery - Customer Identification failed
        "OP-45",  # Attempted delivery
        "OP-55",  # Attempted Delivery - Returned to Sender
        "OP-15",  # Parcel lost
        "OP-17",  # Parcel Damaged
        "OP-23",  # Invalid / Insufficient Address
        "OP-86",  # Attempted delivery
        "OP-40",  # Package disposed
        "OP-92",  # Amazon RTS - DESTROY
        "OP-43",  # Not collected from store
    ]
    delivery_delayed = [
        "OP-16",  # Parcel Delayed
        "OP-13",  # Misdirected
        "OP-35",  # Mis sorted by carrier
    ]
    out_for_delivery = [
        "OP-21",  # Out for delivery
    ]
    ready_for_pickup = [
        "OP-19",  # Awaiting Collection
        "OP-25",  # Customer to collect from carrier
        "OP-42",  # Awaiting collection
    ]
    cancelled = [
        "OP-34",  # Cancelled
        "OP-67",  # RTS - Cancelled Order
    ]
    return_to_sender = [
        "OP-57",  # RTS Received  - Authorised Return
        "OP-58",  # RTS Received - Cancelled Order
        "OP-59",  # RTS Received - Card Left, Never Collected
        "OP-60",  # RTS - Fraudulant
        "OP-61",  # RTS Received - Invalid or Insufficient Address
        "OP-62",  # RTS Received- No Reason Given
        "OP-63",  # RTS - High Value Rejected
        "OP-64",  # RTS Received - Refused
        "OP-65",  # RTS Received - Unclaimed
        "OP-66",  # Return to Sender
        "OP-68",  # RTS Received
        "OP-69",  # RTS Received - Damaged Parcel
        "OP-85",  # RTS - In transit
        "OP-90",  # Return processed
        "OP-94",  # RTS consolidated
    ]
