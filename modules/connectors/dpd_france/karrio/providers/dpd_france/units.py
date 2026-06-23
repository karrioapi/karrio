import csv
import pathlib

import karrio.core.models as models
import karrio.core.units as units
import karrio.lib as lib


class ConnectionConfig(lib.Enum):
    """Carrier connection configuration options."""

    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)
    label_type = lib.OptionEnum("label_type", str, "PDF")


class LabelType(lib.StrEnum):
    """cargoNET eLabelType — per Shipping PDF §11.6."""

    Default = "Default"
    PDF = "PDF"
    PDF_A6 = "PDF_A6"
    EPL = "EPL"
    ZPL = "ZPL"
    ZPL300 = "ZPL300"
    ZPL_A6 = "ZPL_A6"
    ZPL300_A6 = "ZPL300_A6"


class ShippingService(lib.StrEnum):
    """cargoNET DPD France product catalog — per Shipping PDF §1."""

    dpd_france_classic = "DPD Classic"
    dpd_france_predict = "DPD Predict"
    dpd_france_medical = "DPD Medical"
    dpd_france_relais_pickup_consigne = "DPD Relais Pickup & Consigne"
    dpd_france_reverse_pickup = "DPD Reverse at Pickup shop"
    dpd_france_secure = "DPD Secure"


class ShippingOption(lib.Enum):
    """cargoNET DPD France service options — per Shipping PDF §10 STDSERVICES."""

    dpd_france_extra_insurance = lib.OptionEnum("extra_insurance", float)
    dpd_france_predict_contact = lib.OptionEnum("predict_contact", str)
    dpd_france_parcelshop = lib.OptionEnum("parcelshop", str)
    dpd_france_autoconsolidation = lib.OptionEnum("autoconsolidation", bool)


def shipping_options_initializer(
    options: dict,
    package_options: units.ShippingOptions = None,
) -> units.ShippingOptions:
    """Apply default DPD France options."""
    if package_options is not None:
        options.update(package_options.content)

    def items_filter(key: str) -> bool:
        return key in ShippingOption  # type: ignore

    return units.ShippingOptions(options, ShippingOption, items_filter=items_filter)


class TrackingStatus(lib.Enum):
    """Map cargoNET StatusNumber → karrio TrackingStatus.

    StatusNumber values will be refined once live response samples are available
    (Tracking PDF §8.8 documents StatusNumber: int without enumerating values).
    """

    on_hold = ["on_hold"]
    delivered = ["delivered"]
    in_transit = ["in_transit"]
    delivery_failed = ["delivery_failed"]
    delivery_delayed = ["delivery_delayed"]
    out_for_delivery = ["out_for_delivery"]
    ready_for_pickup = ["ready_for_pickup"]


def load_services_from_csv() -> list:
    """Load DPD France service definitions from `services.csv`.

    Mirrors `karrio/modules/connectors/dpd/karrio/providers/dpd/units.py`'s
    loader. cargoNET has no native rating endpoint, so karrio drives rating
    via the universal rate-sheet provider against this CSV.
    """
    csv_path = pathlib.Path(__file__).resolve().parent / "services.csv"

    if not csv_path.exists():
        return [
            models.ServiceLevel(
                service_name="DPD Classic",
                service_code="dpd_france_classic",
                currency="EUR",
                domicile=True,
                international=False,
                zones=[models.ServiceZone(rate=0.0)],
            )
        ]

    services_dict: dict = {}

    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            service_code = row["service_code"]
            service_name = row["service_name"]

            karrio_service_code = ShippingService.map(service_code).name_or_key

            if karrio_service_code not in services_dict:
                services_dict[karrio_service_code] = {
                    "service_name": service_name,
                    "service_code": karrio_service_code,
                    "currency": row.get("currency", "EUR"),
                    "min_weight": (float(row["min_weight"]) if row.get("min_weight") else None),
                    "max_weight": (float(row["max_weight"]) if row.get("max_weight") else None),
                    "max_length": (float(row["max_length"]) if row.get("max_length") else None),
                    "max_width": (float(row["max_width"]) if row.get("max_width") else None),
                    "max_height": (float(row["max_height"]) if row.get("max_height") else None),
                    "weight_unit": "KG",
                    "dimension_unit": "CM",
                    "domicile": row.get("domicile", "").lower() == "true",
                    "international": (True if row.get("international", "").lower() == "true" else None),
                    "zones": [],
                }

            country_codes = [c.strip() for c in row.get("country_codes", "").split(",") if c.strip()]

            zone = models.ServiceZone(
                label=row.get("zone_label", "Default Zone"),
                rate=float(row.get("rate", 0.0)),
                min_weight=float(row["min_weight"]) if row.get("min_weight") else None,
                max_weight=float(row["max_weight"]) if row.get("max_weight") else None,
                transit_days=(
                    int(row["transit_days"].split("-")[0])
                    if row.get("transit_days") and row["transit_days"].split("-")[0].isdigit()
                    else None
                ),
                country_codes=country_codes if country_codes else None,
            )

            services_dict[karrio_service_code]["zones"].append(zone)

    return [models.ServiceLevel(**service_data) for service_data in services_dict.values()]


DEFAULT_SERVICES = load_services_from_csv()
