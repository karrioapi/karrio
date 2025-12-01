import csv
import pathlib
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models


class PackagingType(lib.StrEnum):
    """Carrier specific packaging type"""

    PACKAGE = "PACKAGE"

    """ Unified Packaging type mapping """
    envelope = PACKAGE
    pak = PACKAGE
    tube = PACKAGE
    pallet = PACKAGE
    small_box = PACKAGE
    medium_box = PACKAGE
    your_packaging = PACKAGE


class CustomsContentType(lib.StrEnum):
    other = "OTHER"
    present = "PRESENT"
    document = "DOCUMENT"
    return_of_goods = "RETURN_OF_GOODS"
    commercial_goods = "COMMERCIAL_GOODS"
    commercial_sample = "COMMERCIAL_SAMPLE"

    """ Unified Content type mapping """
    gift = present
    documents = document
    sample = commercial_sample
    merchandise = commercial_goods
    return_merchandise = return_of_goods


class Incoterm(lib.StrEnum):
    """Carrier specific incoterm"""

    DDU = "DDU"
    DAP = "DAP"
    DDP = "DDP"
    DDX = "DDX"
    DXV = "DXV"


class LabelType(lib.Enum):
    """Carrier specific label type"""

    PDF_A4 = ("PDF", "A4")
    ZPL2_A4 = ("ZPL2", "A4")
    PDF_910_300_700 = ("PDF", "910-300-700")
    ZPL2_910_300_700 = ("ZPL2", "910-300-700")
    PDF_910_300_700_oz = ("PDF", "910-300-700-oz")
    ZPL2_910_300_700_oz = ("ZPL2", "910-300-700-oz")
    PDF_910_300_710 = ("PDF", "910-300-710")
    ZPL2_910_300_710 = ("ZPL2", "910-300-710")
    PDF_910_300_600 = ("PDF", "910-300-600")
    ZPL2_910_300_600 = ("ZPL2", "910-300-600")
    PDF_910_300_610 = ("PDF", "910-300-610")
    ZPL2_910_300_610 = ("ZPL2", "910-300-610")
    PDF_910_300_400 = ("PDF", "910-300-400")
    ZPL2_910_300_400 = ("ZPL2", "910-300-400")
    PDF_910_300_410 = ("PDF", "910-300-410")
    ZPL2_910_300_410 = ("ZPL2", "910-300-410")
    PDF_910_300_300 = ("PDF", "910-300-300")
    ZPL2_910_300_300 = ("ZPL2", "910-300-300")
    PDF_910_300_300_oz = ("PDF", "910-300-300-oz")
    ZPL2_910_300_300_oz = ("ZPL2", "910-300-300-oz")

    """ Unified Label type mapping """
    PDF = PDF_A4
    ZPL = ZPL2_A4
    PNG = PDF_A4


class ConnectionConfig(lib.Enum):
    profile = lib.OptionEnum("profile")
    cost_center = lib.OptionEnum("cost_center")
    creation_software = lib.OptionEnum("creation_software")
    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)
    language = lib.OptionEnum(
        "language",
        lib.units.create_enum("Language", ["de", "en"]),
    )
    label_type = lib.OptionEnum(
        "label_type",
        lib.units.create_enum("LabelType", [_.name for _ in LabelType]),  # type: ignore
    )


class ShippingService(lib.Enum):
    """Carrier specific services"""

    dhl_parcel_de_paket = "V01PAK"
    dhl_parcel_de_kleinpaket = "V62KP"
    dhl_parcel_de_europaket = "V54EPAK"
    dhl_parcel_de_paket_international = "V53WPAK"
    dhl_parcel_de_warenpost_international = "V66WPI"

    # Alias for backwards compatibility (Warenpost replaced by Kleinpaket as of 2025)
    dhl_parcel_de_warenpost = dhl_parcel_de_kleinpaket


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    # fmt: off
    dhl_parcel_de_preferred_neighbour = lib.OptionEnum("preferredNeighbour")
    dhl_parcel_de_preferred_location = lib.OptionEnum("preferredLocation")
    dhl_parcel_de_visual_check_of_age = lib.OptionEnum("visualCheckOfAge")
    dhl_parcel_de_named_person_only = lib.OptionEnum("namedPersonOnly", bool)
    dhl_parcel_de_signed_for_by_recipient = lib.OptionEnum("signedForByRecipient", bool)
    dhl_parcel_de_endorsement = lib.OptionEnum("endorsement")
    dhl_parcel_de_preferred_day = lib.OptionEnum("preferredDay")
    dhl_parcel_de_no_neighbour_delivery = lib.OptionEnum("noNeighbourDelivery", bool)
    dhl_parcel_de_additional_insurance = lib.OptionEnum("additionalInsurance", float)
    dhl_parcel_de_bulky_goods = lib.OptionEnum("bulkyGoods", bool)
    dhl_parcel_de_cash_on_delivery = lib.OptionEnum("cashOnDelivery", float)
    dhl_parcel_de_individual_sender_requirement = lib.OptionEnum("individualSenderRequirement")
    dhl_parcel_de_premium = lib.OptionEnum("premium", bool)
    dhl_parcel_de_closest_drop_point = lib.OptionEnum("closestDropPoint", bool)
    dhl_parcel_de_parcel_outlet_routing = lib.OptionEnum("parcelOutletRouting")
    dhl_parcel_de_postal_delivery_duty_paid = lib.OptionEnum("postalDeliveryDutyPaid", bool)
    dhl_parcel_de_postal_charges = lib.OptionEnum("postalCharges", float)
    dhl_parcel_de_dhl_retoure = lib.OptionEnum("dhlRetoure", bool)
    dhl_parcel_de_locker_id = lib.OptionEnum("lockerID")
    dhl_parcel_de_post_number = lib.OptionEnum("postNumber")
    dhl_parcel_de_retail_id = lib.OptionEnum("retailID")
    dhl_parcel_de_po_box_id = lib.OptionEnum("poBoxID")
    dhl_parcel_de_shipper_customs_ref = lib.OptionEnum("shipperCustomsRef")
    dhl_parcel_de_consignee_customs_ref = lib.OptionEnum("consigneeCustomsRef")
    dhl_parcel_de_permit_no = lib.OptionEnum("permitNo")
    dhl_parcel_de_attestation_no = lib.OptionEnum("attestationNo")
    dhl_parcel_de_has_electronic_export_notification = lib.OptionEnum("hasElectronicExportNotification")
    dhl_parcel_de_MRN = lib.OptionEnum("MRN")

    """ Unified Option type mapping """
    signature_confirmation = dhl_parcel_de_signed_for_by_recipient
    hold_at_location = dhl_parcel_de_closest_drop_point
    cash_on_delivery = dhl_parcel_de_cash_on_delivery
    shipping_charges = dhl_parcel_de_postal_charges
    insurance = dhl_parcel_de_additional_insurance
    # fmt: on


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
        return key in ShippingOption or key in units.ShippingOption  # type: ignore

    return units.ShippingOptions(options, ShippingOption, items_filter=items_filter)


class CustomsOption(lib.Enum):
    mrn = lib.OptionEnum("MRN")
    permit_number = lib.OptionEnum("permitNo")
    attestation_number = lib.OptionEnum("attestationNo")
    shipper_customs_ref = lib.OptionEnum("shipperCustomsRef")
    consignee_customs_ref = lib.OptionEnum("consigneeCustomsRef")
    electronic_export_notification = lib.OptionEnum("electronicExportNotification")


class TrackingStatus(lib.Enum):
    delivered = ["delivered"]
    in_transit = ["transit"]
    delivery_failed = ["failure"]
    delivery_delayed = ["unknown"]


def load_services_from_csv() -> list:
    """
    Load service definitions from CSV file.
    CSV format: service_code,service_name,zone_label,country_codes,min_weight,max_weight,max_length,max_width,max_height,rate,currency,transit_days,domicile,international
    """
    csv_path = pathlib.Path(__file__).resolve().parent / "services.csv"

    if not csv_path.exists():
        # Fallback to simple default if CSV doesn't exist
        return [
            models.ServiceLevel(
                service_name="DHL Paket",
                service_code="dhl_parcel_de_paket",
                currency="EUR",
                domicile=True,
                zones=[models.ServiceZone(rate=0.0)],
            )
        ]

    # Group zones by service
    services_dict: dict[str, dict] = {}

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            service_code = row["service_code"]
            service_name = row["service_name"]

            # Map carrier service code to karrio service code
            karrio_service_code = ShippingService.map(service_code).name_or_key

            # Initialize service if not exists
            if karrio_service_code not in services_dict:
                services_dict[karrio_service_code] = {
                    "service_name": service_name,
                    "service_code": karrio_service_code,
                    "currency": row.get("currency", "EUR"),
                    "min_weight": (
                        float(row["min_weight"]) if row.get("min_weight") else None
                    ),
                    "max_weight": (
                        float(row["max_weight"]) if row.get("max_weight") else None
                    ),
                    "max_length": (
                        float(row["max_length"]) if row.get("max_length") else None
                    ),
                    "max_width": (
                        float(row["max_width"]) if row.get("max_width") else None
                    ),
                    "max_height": (
                        float(row["max_height"]) if row.get("max_height") else None
                    ),
                    "weight_unit": "KG",
                    "dimension_unit": "CM",
                    "domicile": row.get("domicile", "").lower() == "true",
                    "international": (
                        True if row.get("international", "").lower() == "true" else None
                    ),
                    "zones": [],
                }

            # Parse country codes
            country_codes = [
                c.strip() for c in row.get("country_codes", "").split(",") if c.strip()
            ]

            # Create zone
            zone = models.ServiceZone(
                label=row.get("zone_label", "Default Zone"),
                rate=float(row.get("rate", 0.0)),
                transit_days=(
                    int(row["transit_days"]) if row.get("transit_days") else None
                ),
                country_codes=country_codes if country_codes else None,
            )

            services_dict[karrio_service_code]["zones"].append(zone)

    # Convert to ServiceLevel objects
    return [
        models.ServiceLevel(**service_data) for service_data in services_dict.values()
    ]


DEFAULT_SERVICES = load_services_from_csv()
