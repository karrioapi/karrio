import karrio.lib as lib
import karrio.core.units as units


class PackagingType(lib.StrEnum):
    """Carrier specific packaging type"""

    teleship_parcel = "parcel"
    teleship_envelope = "envelope"
    teleship_document = "document"

    """ Unified Packaging type mapping """
    envelope = teleship_envelope
    pak = teleship_envelope
    small_box = teleship_parcel
    medium_box = teleship_parcel
    your_packaging = teleship_parcel


class ShippingService(lib.StrEnum):
    """Carrier specific services"""

    teleship_expedited_pickup = "TELESHIP-EXPEDITED-PICKUP"
    teleship_expedited_dropoff = "TELESHIP-EXPEDITED-DROPOFF"
    teleship_standard_dropoff = "TELESHIP-STANDARD-DROPOFF"
    teleship_standard_pickup = "TELESHIP-STANDARD-PICKUP"


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    teleship_customer_reference = lib.OptionEnum("customerReference")
    teleship_order_tracking_reference = lib.OptionEnum("orderTrackingReference")
    teleship_include_first_mile = lib.OptionEnum("includeFirstMile", bool)
    teleship_label_format = lib.OptionEnum("labelFormat")
    teleship_service_code = lib.OptionEnum("serviceCode")
    teleship_shipment_description = lib.OptionEnum("shipmentDescription")
    teleship_return_address = lib.OptionEnum("returnAddress", bool)
    teleship_signature_required = lib.OptionEnum("signatureRequired", bool)
    teleship_delivery_warranty = lib.OptionEnum("deliveryWarranty", bool)
    teleship_delivery_pudo = lib.OptionEnum("deliveryPUDO", bool)
    teleship_low_carbon = lib.OptionEnum("lowCarbon", bool)
    teleship_duty_tax_calculation = lib.OptionEnum("dutyTaxCalculation", bool)

    """ Unified Option type mapping """
    insurance = lib.OptionEnum("insurance", float)
    signature_required = lib.OptionEnum("signature", bool)
    shipment_date = lib.OptionEnum("shipDate")


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


class CustomsContentType(lib.StrEnum):
    """Teleship customs content types"""

    # Teleship-specific values (PascalCase)
    teleship_documents = "Documents"
    teleship_gift = "Gift"
    teleship_sample = "Sample"
    teleship_other = "Other"
    teleship_commercial_goods = "CommercialGoods"
    teleship_return_of_goods = "ReturnOfGoods"

    """ Unified content type mapping """
    documents = teleship_documents
    gift = teleship_gift
    sample = teleship_sample
    other = teleship_other
    merchandise = teleship_commercial_goods
    returned_goods = teleship_return_of_goods


class CustomsOption(lib.Enum):
    """Teleship customs identifiers"""

    EORI = lib.OptionEnum("EORI")
    IOSS = lib.OptionEnum("IOSS")
    VAT = lib.OptionEnum("VAT")
    EIN = lib.OptionEnum("EIN")
    VOECNUMBER = lib.OptionEnum("VOECNUMBER")

    # Commercial invoice and tax IDs
    commercial_invoice_reference = lib.OptionEnum("commercialInvoiceReference")
    tax_id_type = lib.OptionEnum("taxIdType")
    tax_id = lib.OptionEnum("taxId")

    # GST numbers
    importer_gst = lib.OptionEnum("importerGST")
    exporter_gst = lib.OptionEnum("exporterGST")
    consignee_gst = lib.OptionEnum("consigneeGST")

    # GPSR Contact Information
    gpsr_contact_name = lib.OptionEnum("gpsrContactName")
    gpsr_contact_email = lib.OptionEnum("gpsrContactEmail")
    gpsr_contact_phone = lib.OptionEnum("gpsrContactPhone")
    gpsr_contact_address_line1 = lib.OptionEnum("gpsrContactAddressLine1")
    gpsr_contact_city = lib.OptionEnum("gpsrContactCity")
    gpsr_contact_state = lib.OptionEnum("gpsrContactState")
    gpsr_contact_country = lib.OptionEnum("gpsrContactCountry")
    gpsr_contact_postcode = lib.OptionEnum("gpsrContactPostcode")

    # Importer of Record
    importer_name = lib.OptionEnum("importerName")
    importer_company = lib.OptionEnum("importerCompany")
    importer_email = lib.OptionEnum("importerEmail")
    importer_phone = lib.OptionEnum("importerPhone")
    importer_address_line1 = lib.OptionEnum("importerAddressLine1")
    importer_address_line2 = lib.OptionEnum("importerAddressLine2")
    importer_city = lib.OptionEnum("importerCity")
    importer_state = lib.OptionEnum("importerState")
    importer_country = lib.OptionEnum("importerCountry")
    importer_postcode = lib.OptionEnum("importerPostcode")
    importer_tax_id_type = lib.OptionEnum("importerTaxIdType")
    importer_tax_id = lib.OptionEnum("importerTaxId")

    """ Unified Customs Identifier type mapping """

    ioss = IOSS
    eori_number = EORI
    vat = VAT
    ein = EIN
    voec_number = VOECNUMBER
    vat_registration_number = VAT


class TrackingStatus(lib.Enum):
    """Teleship tracking statuses"""

    delivered = ["delivered"]
    in_transit = [
        "in_transit",
        "collected",
        "in_hub",
        "out_for_delivery",
        "customs_cleared",
    ]
    out_for_delivery = ["out_for_delivery"]
    delivery_failed = ["delivery_failed", "returned", "cancelled"]
    pending = ["pending", "created", "label_created"]
