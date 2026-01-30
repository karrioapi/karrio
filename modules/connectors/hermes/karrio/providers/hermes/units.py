import csv
import pathlib
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models


class ConnectionConfig(lib.Enum):
    """Carrier connection configuration options."""

    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)
    label_type = lib.OptionEnum("label_type", str, "PDF")
    language = lib.OptionEnum("language", str, "DE")  # DE or EN


class ParcelClass(lib.StrEnum):
    """Hermes parcel size classes."""

    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"


class ProductType(lib.StrEnum):
    """Hermes product types."""

    BAG = "BAG"
    BIKE = "BIKE"
    LARGE_ITEM = "LARGE_ITEM"
    PARCEL = "PARCEL"


class PackagingType(lib.StrEnum):
    """Carrier specific packaging type."""

    hermes_parcel = "PARCEL"
    hermes_bag = "BAG"
    hermes_bike = "BIKE"
    hermes_large_item = "LARGE_ITEM"

    """Unified Packaging type mapping."""
    envelope = hermes_parcel
    pak = hermes_parcel
    tube = hermes_parcel
    pallet = hermes_large_item
    small_box = hermes_parcel
    medium_box = hermes_parcel
    your_packaging = hermes_parcel


class ShippingService(lib.StrEnum):
    """Carrier specific services."""

    hermes_standard = "hermes_standard"
    hermes_next_day = "hermes_next_day"
    hermes_stated_day = "hermes_stated_day"
    hermes_parcel_shop = "hermes_parcel_shop"
    hermes_international = "hermes_international"


class ShippingOption(lib.Enum):
    """Carrier specific options."""

    # Hermes services as options
    hermes_tan_service = lib.OptionEnum("tanService", bool)
    hermes_limited_quantities = lib.OptionEnum("limitedQuantitiesService", bool, meta=dict(category="DANGEROUS_GOOD"))
    hermes_bulk_goods = lib.OptionEnum("bulkGoodService", bool)
    hermes_household_signature = lib.OptionEnum("householdSignatureService", bool, meta=dict(category="SIGNATURE"))
    hermes_compact_parcel = lib.OptionEnum("compactParcelService", bool)
    hermes_next_day = lib.OptionEnum("nextDayService", bool, meta=dict(category="DELIVERY_OPTIONS"))
    hermes_signature = lib.OptionEnum("signatureService", bool, meta=dict(category="SIGNATURE"))
    hermes_redirection_prohibited = lib.OptionEnum("redirectionProhibitedService", bool, meta=dict(category="DELIVERY_OPTIONS"))
    hermes_exclude_parcel_shop_auth = lib.OptionEnum("excludeParcelShopAuthorization", bool, meta=dict(category="PUDO"))
    hermes_late_injection = lib.OptionEnum("lateInjectionService", bool)

    # Cash on delivery
    hermes_cod_amount = lib.OptionEnum("codAmount", float, meta=dict(category="COD"))
    hermes_cod_currency = lib.OptionEnum("codCurrency", str, meta=dict(category="COD"))

    # Customer alert service
    hermes_notification_email = lib.OptionEnum("notificationEmail", str, meta=dict(category="NOTIFICATION"))
    hermes_notification_type = lib.OptionEnum("notificationType", str, meta=dict(category="NOTIFICATION"))  # EMAIL, SMS, EMAIL_SMS

    # Stated day service
    hermes_stated_day = lib.OptionEnum("statedDay", str, meta=dict(category="DELIVERY_OPTIONS"))  # YYYY-MM-DD format

    # Stated time service
    hermes_time_slot = lib.OptionEnum("timeSlot", str, meta=dict(category="DELIVERY_OPTIONS"))  # FORENOON, NOON, AFTERNOON, EVENING

    # Ident service
    hermes_ident_id = lib.OptionEnum("identID", str, meta=dict(category="SIGNATURE"))
    hermes_ident_type = lib.OptionEnum("identType", str, meta=dict(category="SIGNATURE"))  # GERMAN_IDENTITY_CARD, etc.
    hermes_ident_fsk = lib.OptionEnum("identVerifyFsk", str, meta=dict(category="SIGNATURE"))  # 18
    hermes_ident_birthday = lib.OptionEnum("identVerifyBirthday", str, meta=dict(category="SIGNATURE"))  # YYYY-MM-DD

    # Parcel shop delivery
    hermes_parcel_shop_id = lib.OptionEnum("psID", str, meta=dict(category="PUDO"))
    hermes_parcel_shop_selection_rule = lib.OptionEnum("psSelectionRule", str, meta=dict(category="PUDO"))  # SELECT_BY_ID, SELECT_BY_RECEIVER_ADDRESS
    hermes_parcel_shop_customer_firstname = lib.OptionEnum("psCustomerFirstName", str, meta=dict(category="PUDO"))
    hermes_parcel_shop_customer_lastname = lib.OptionEnum("psCustomerLastName", str, meta=dict(category="PUDO"))

    # Multipart service
    hermes_part_number = lib.OptionEnum("partNumber", int)
    hermes_number_of_parts = lib.OptionEnum("numberOfParts", int)
    hermes_parent_shipment_order_id = lib.OptionEnum("parentShipmentOrderID", str)

    """Unified Option type mapping."""
    signature_required = hermes_signature
    cash_on_delivery = hermes_cod_amount


def shipping_options_initializer(
    options: dict,
    package_options: units.ShippingOptions = None,
) -> units.ShippingOptions:
    """Apply default values to the given options."""

    if package_options is not None:
        options.update(package_options.content)

    def items_filter(key: str) -> bool:
        return key in ShippingOption  # type: ignore

    return units.ShippingOptions(options, ShippingOption, items_filter=items_filter)


class TrackingStatus(lib.Enum):
    """Hermes tracking status mapping.

    Maps Hermes 2x2 event codes (4-digit) to Karrio unified statuses.
    Based on Hermes Germany Eventcodes.csv.
    """

    pending = [
        "0000",  # Die Sendung wurde Hermes elektronisch angekündigt
        "0600",  # Shipment has not arrived at the depot (1st notice)
        "0700",  # Shipment has not arrived at the depot (2nd notice)
        "0800",  # Shipment has not arrived at the depot (7 days)
        "0900",  # Shipment has not arrived at the depot (28 days)
    ]
    picked_up = [
        "1000",  # Die Sendung hat das Lager des Auftraggebers verlassen
        "1900",  # Shipment accepted after collection
        "1901",  # Shipment arrived at branch by self-delivery
        "1910",  # Shipment received on tour
    ]
    in_transit = [
        "1510",  # Sendung am LC umgeschlagen (sorted at logistics center)
        "1610",  # Shipment in international transit
        "1710",  # Customs export created
        "1720",  # Customs clearance completed
        "1810",  # Handed to partner carrier (international)
        "1820",  # Handed to partner carrier (international)
        "2000",  # Die Sendung ist eingetroffen (arrived at depot)
        "2100",  # Arrived without advice data
        "2300",  # Automatic shipment received
        "2400",  # Shipment handed in at ParcelShop
    ]
    out_for_delivery = [
        "3000",  # Die Sendung ist auf Zustelltour gegangen
        "3010",  # Shipment has left depot on tour
        "3300",  # Sorted for delivery tour (automatic)
    ]
    ready_for_pickup = [
        "3410",  # Die Sendung liegt im PaketShop zur Abholung bereit
        "3430",  # Handed over to island carrier
    ]
    delivered = [
        "3500",  # Die Sendung wurde zugestellt
        "3510",  # Shipment delivered (with scanner)
        "3511",  # Delivered in letterbox
        "3520",  # Shipment delivered (without scanner)
        "3530",  # Collected by recipient from ParcelShop
        "7500",  # Return shipment arrived at client
    ]
    delivery_failed = [
        "3710",  # Annahmeverweigerung (refused)
        "3715",  # COD not paid
        "3720",  # Address not found
        "3731",  # Recipient not present (1st attempt)
        "3732",  # Recipient not present (2nd attempt)
        "3733",  # Recipient not present (3rd attempt)
        "3734",  # Recipient not present (4th attempt)
        "3740",  # Damage detected
        "3750",  # Tour cancellation
        "3751",  # Incorrect TAN (1st attempt)
        "3752",  # Incorrect TAN (2nd attempt)
        "3753",  # Incorrect TAN (3rd attempt)
        "3754",  # Incorrect TAN (4th attempt)
        "3760",  # Return shipment collected
        "3761",  # Return shipment taken
        "3780",  # Misdirected
        "3782",  # Ident failed - photo mismatch
        "3783",  # Ident failed - name mismatch
        "3784",  # Ident failed - DOB mismatch
        "3785",  # Ident failed - document mismatch
        "3786",  # Ident failed - PIN code
        "3787",  # Ident failed - age verification
        "3795",  # Shipment stopped
    ]
    on_hold = [
        "1730",  # Held by customs
        "1751",  # Rejected by customs
        "4100",  # Sendung wird aufbewahrt (shipment stored)
        "4500",  # Stored (stocktaking)
        "4610",  # ParcelShop - high volume, cannot pick up
        "4620",  # ParcelShop - shipment not available
        "4630",  # ParcelShop - shipment not found
        "4690",  # Status corrected at ParcelShop
    ]
    delivery_delayed = [
        "4010",  # Return - refused
        "4015",  # Return - COD not paid
        "4020",  # Return - address not found
        "4024",  # Return - too large/heavy for ParcelShop
        "4025",  # Shipment returned to depot
        "4031",  # Return - N1 (1st attempt failed)
        "4032",  # Return - N2 (2nd attempt failed)
        "4033",  # Return - N3 (3rd attempt failed)
        "4034",  # Return - N4 (4th attempt failed)
        "4035",  # Return - not collected from ParcelShop
        "4040",  # Return - damage
        "4050",  # Return - tour cancellation
        "4051",  # Return - TAN 1
        "4052",  # Return - TAN 2
        "4053",  # Return - TAN 3
        "4054",  # Return - TAN 4
        "4060",  # Return shipment received (pickup)
        "4061",  # Return shipment received (take-away)
        "4062",  # Return handed in at ParcelShop
        "4070",  # Tour departure cancelled
        "4072",  # Return cancelled (correction)
        "4080",  # Misdirected
        "4081",  # Ident failed
        "4082",  # Ident failed - photo
        "4083",  # Ident failed - name
        "4084",  # Ident failed - DOB
        "4085",  # Ident failed - document
        "4086",  # Ident failed - PIN
        "4087",  # Ident failed - age
        "4095",  # Delivery stopped
    ]
    return_to_sender = [
        "1520",  # Return shipment sorted
        "6080",  # Rückversand (return shipment)
        "6081",  # Return - refused
        "6082",  # Return - address not readable
        "6083",  # Return - address not found
        "6084",  # Return - receiver not met
        "6085",  # Return - damage
        "6086",  # Return - sorting error
        "6087",  # Return - technical issue
        "6088",  # Redirected at receiver request
        "6089",  # Return - returns
        "6090",  # Forwarded to logistics center
        "6092",  # Return - ident failed
        "6093",  # Return - not collected from ParcelShop
        "6094",  # Return - COD not paid
        "6096",  # Return - too large/heavy for ParcelShop
        "6098",  # Return - incorrect TAN
        "6099",  # Return - delivery stopped
    ]


class TrackingIncidentReason(lib.Enum):
    """Maps Hermes exception codes to normalized incident reasons.

    Based on Hermes Germany Eventcodes.csv.
    Maps carrier-specific exception/status codes to standardized
    incident reasons for tracking events.
    """

    # Consignee-caused issues
    consignee_refused = [
        "3710",  # Annahmeverweigerung
        "4010",  # Return - refused
        "6081",  # Return - refused
    ]
    consignee_not_home = [
        "3731",  # Recipient not present (1st attempt)
        "3732",  # Recipient not present (2nd attempt)
        "3733",  # Recipient not present (3rd attempt)
        "3734",  # Recipient not present (4th attempt)
        "4031",  # Return - N1
        "4032",  # Return - N2
        "4033",  # Return - N3
        "4034",  # Return - N4
        "6084",  # Return - receiver not met
    ]
    consignee_incorrect_address = [
        "3720",  # Address not found
        "4020",  # Return - address not found
        "6082",  # Return - address not readable
        "6083",  # Return - address not found
    ]
    consignee_not_available = [
        "4035",  # Not collected from ParcelShop
        "6093",  # Return - not collected from ParcelShop
    ]
    consignee_cod_unpaid = [
        "3715",  # COD not paid
        "4015",  # Return - COD not paid
        "6094",  # Return - COD not paid
    ]
    consignee_id_failed = [
        "3782",  # Ident failed - photo mismatch
        "3783",  # Ident failed - name mismatch
        "3784",  # Ident failed - DOB mismatch
        "3785",  # Ident failed - document mismatch
        "3786",  # Ident failed - PIN code
        "3787",  # Ident failed - age verification
        "4081",  # Ident failed
        "4082",  # Ident failed - photo
        "4083",  # Ident failed - name
        "4084",  # Ident failed - DOB
        "4085",  # Ident failed - document
        "4086",  # Ident failed - PIN
        "4087",  # Ident failed - age
        "6092",  # Return - ident failed
    ]
    consignee_tan_invalid = [
        "3751",  # Incorrect TAN (1st attempt)
        "3752",  # Incorrect TAN (2nd attempt)
        "3753",  # Incorrect TAN (3rd attempt)
        "3754",  # Incorrect TAN (4th attempt)
        "4051",  # Return - TAN 1
        "4052",  # Return - TAN 2
        "4053",  # Return - TAN 3
        "4054",  # Return - TAN 4
        "6098",  # Return - incorrect TAN
    ]

    # Carrier-caused issues
    carrier_damaged_parcel = [
        "3740",  # Damage detected
        "4040",  # Return - damage
        "6085",  # Return - damage
    ]
    carrier_sorting_error = [
        "3780",  # Misdirected
        "4080",  # Misdirected
        "6086",  # Return - sorting error
        "6087",  # Return - technical issue
    ]
    carrier_not_enough_time = [
        "3750",  # Tour cancellation
        "4050",  # Return - tour cancellation
        "4070",  # Tour departure cancelled
    ]
    carrier_parcel_too_large = [
        "4024",  # Return - too large/heavy for ParcelShop
        "6096",  # Return - too large/heavy for ParcelShop
    ]

    # Customs-related issues
    customs_delay = [
        "1730",  # Held by customs
    ]
    customs_rejected = [
        "1751",  # Rejected by customs
    ]

    # Shipment stopped
    shipment_stopped = [
        "3795",  # Shipment stopped
        "4095",  # Delivery stopped
        "6099",  # Return - delivery stopped
    ]


class LabelType(lib.StrEnum):
    """Hermes label formats - use +json variants for JSON response with base64 label."""

    PDF = "application/shippinglabel-pdf+json"
    ZPL = "application/shippinglabel-zpl+json;dpi=300"
    PNG = "application/shippinglabel-data+json"


class PickupTimeSlot(lib.StrEnum):
    """Hermes pickup time slots per OpenAPI spec."""

    BETWEEN_10_AND_13 = "BETWEEN_10_AND_13"
    BETWEEN_12_AND_15 = "BETWEEN_12_AND_15"
    BETWEEN_14_AND_17 = "BETWEEN_14_AND_17"


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
                service_name="Hermes Standard",
                service_code="hermes_standard",
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
                    int(row["transit_days"].split("-")[0]) if row.get("transit_days") and row["transit_days"].split("-")[0].isdigit() else None
                ),
                country_codes=country_codes if country_codes else None,
            )

            services_dict[karrio_service_code]["zones"].append(zone)

    # Convert to ServiceLevel objects
    return [
        models.ServiceLevel(**service_data) for service_data in services_dict.values()
    ]


DEFAULT_SERVICES = load_services_from_csv()
