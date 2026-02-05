import csv
import pathlib

import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models


class CustomsContentType(lib.StrEnum):
    other = "9"
    sale_of_goods = "11"
    return_of_goods = "21"
    gifts = "31"
    samples_of_goods = "32"
    documents = "91"

    """ Unified Content type mapping """
    gift = gifts
    sample = samples_of_goods
    merchandise = sale_of_goods
    return_merchandise = return_of_goods


class LabelType(lib.StrEnum):
    BLP_LABEL = "BLP"
    LBLP_LABEL_A4_PDF = "LBLP"
    ZBLP_LABEL_ZPL = "ZBLP"

    """ Unified Label type mapping """
    PDF = BLP_LABEL
    ZPL = ZBLP_LABEL_ZPL


class PaymentType(lib.StrEnum):
    shipper = "SHIPPER"
    receiver = "RECEIVER"
    user = "USER"

    """ Unified Payment type mapping """
    sender = shipper
    recipient = receiver
    third_party = user


class PackagingType(lib.StrEnum):
    dhl_poland_envelope = "ENVELOPE"
    dhl_poland_package = "PACKAGE"
    dhl_poland_pallet = "PALLET"

    """ Unified Packaging type mapping """
    envelope = dhl_poland_envelope
    pak = dhl_poland_package
    tube = dhl_poland_package
    pallet = dhl_poland_pallet
    small_box = dhl_poland_package
    medium_box = dhl_poland_package
    large_box = dhl_poland_package
    your_packaging = dhl_poland_package


class Service(lib.Enum):
    dhl_poland_premium = "PR"
    dhl_poland_polska = "AH"
    dhl_poland_09 = "09"
    dhl_poland_12 = "12"
    dhl_poland_connect = "EK"
    dhl_poland_international = "PI"


class ShippingOption(lib.Enum):
    dhl_poland_delivery_in_18_22_hours = lib.OptionEnum("1722", bool, meta=dict(category="DELIVERY_OPTIONS"))
    dhl_poland_delivery_on_saturday = lib.OptionEnum("SATURDAY", bool, meta=dict(category="DELIVERY_OPTIONS"))
    dhl_poland_pickup_on_staturday = lib.OptionEnum("NAD_SOBOTA", bool, meta=dict(category="DELIVERY_OPTIONS"))
    dhl_poland_insuration = lib.OptionEnum("UBEZP", float, meta=dict(category="INSURANCE"))
    dhl_poland_collect_on_delivery = lib.OptionEnum("COD", float, meta=dict(category="COD"))
    dhl_poland_information_to_receiver = lib.OptionEnum("PDI", meta=dict(category="NOTIFICATION"))
    dhl_poland_return_of_document = lib.OptionEnum("ROD", bool, meta=dict(category="RETURN"))
    dhl_poland_proof_of_delivery = lib.OptionEnum("POD", bool, meta=dict(category="DELIVERY_OPTIONS"))
    dhl_poland_delivery_to_neighbour = lib.OptionEnum("SAS", bool, meta=dict(category="DELIVERY_OPTIONS"))
    dhl_poland_self_collect = lib.OptionEnum("ODB", bool, meta=dict(category="PUDO"))

    """ Unified Option type mapping """
    insurance = dhl_poland_insuration
    cash_on_delivery = dhl_poland_collect_on_delivery
    saturday_delivery = dhl_poland_delivery_on_saturday


def shipping_options_initializer(
    options: dict,
    package_options: units.ShippingOptions = None,
) -> units.ShippingOptions:
    """
    Apply default values to the given options.
    """
    _options = options.copy()

    if package_options is not None:
        _options.update(package_options.content)

    def items_filter(key: str) -> bool:
        return key in ShippingOption  # type: ignore

    return units.ShippingOptions(_options, ShippingOption, items_filter=items_filter)


def load_services_from_csv() -> list:
    csv_path = pathlib.Path(__file__).resolve().parent / "services.csv"
    if not csv_path.exists():
        return []
    services_dict: dict[str, dict] = {}
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            service_code = row["service_code"]
            karrio_service_code = Service.map(service_code).name_or_key
            row_min_weight = float(row["min_weight"]) if row.get("min_weight") else None
            row_max_weight = float(row["max_weight"]) if row.get("max_weight") else None
            if karrio_service_code not in services_dict:
                services_dict[karrio_service_code] = {
                    "service_name": row["service_name"],
                    "service_code": karrio_service_code,
                    "currency": row.get("currency", "PLN"),
                    "min_weight": row_min_weight,
                    "max_weight": row_max_weight,
                    "max_length": float(row["max_length"]) if row.get("max_length") else None,
                    "max_width": float(row["max_width"]) if row.get("max_width") else None,
                    "max_height": float(row["max_height"]) if row.get("max_height") else None,
                    "weight_unit": "KG",
                    "dimension_unit": "CM",
                    "domicile": True if (row.get("domicile") or "").lower() == "true" else None,
                    "international": True if (row.get("international") or "").lower() == "true" else None,
                    "zones": [],
                }
            else:
                # Update service-level weight bounds to cover all zones
                current = services_dict[karrio_service_code]
                if row_min_weight is not None:
                    if current["min_weight"] is None or row_min_weight < current["min_weight"]:
                        current["min_weight"] = row_min_weight
                if row_max_weight is not None:
                    if current["max_weight"] is None or row_max_weight > current["max_weight"]:
                        current["max_weight"] = row_max_weight
            country_codes = [c.strip() for c in row.get("country_codes", "").split(",") if c.strip()]
            zone = models.ServiceZone(
                label=row.get("zone_label", "Default Zone"),
                rate=float(row.get("rate", 0.0)),
                min_weight=row_min_weight,
                max_weight=row_max_weight,
                transit_days=int(row["transit_days"].split("-")[0]) if row.get("transit_days") and row["transit_days"].split("-")[0].isdigit() else None,
                country_codes=country_codes if country_codes else None,
            )
            services_dict[karrio_service_code]["zones"].append(zone)
    return [models.ServiceLevel(**service_data) for service_data in services_dict.values()]


DEFAULT_SERVICES = load_services_from_csv()
