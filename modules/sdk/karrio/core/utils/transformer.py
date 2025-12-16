import typing
import functools
import karrio.core.utils as utils
import karrio.core.models as models


def transform_to_shared_zones_format(
    services: typing.List[typing.Union[models.ServiceLevel, dict]],
) -> typing.Dict[str, typing.Any]:
    """Transform legacy service levels with embedded zones to the new shared zones format.

    This function extracts unique zones from service levels and creates a shared zones
    structure where zones are defined once at the rate sheet level and referenced by ID.

    Args:
        services: List of ServiceLevel objects or dicts with embedded zones

    Returns:
        Dictionary with:
        - zones: List of unique shared zone definitions
        - services: List of services with zone_ids referencing shared zones
        - service_rates: List of service-zone rate mappings

    Example:
        Input:
        [
            {
                "service_code": "express",
                "service_name": "Express",
                "zones": [
                    {"label": "Zone 1", "country_codes": ["US"], "rate": 10.0},
                    {"label": "Zone 2", "country_codes": ["CA"], "rate": 15.0}
                ]
            },
            {
                "service_code": "standard",
                "service_name": "Standard",
                "zones": [
                    {"label": "Zone 1", "country_codes": ["US"], "rate": 5.0}
                ]
            }
        ]

        Output:
        {
            "zones": [
                {"id": "zone_1", "label": "Zone 1", "country_codes": ["US"], ...},
                {"id": "zone_2", "label": "Zone 2", "country_codes": ["CA"], ...}
            ],
            "services": [
                {"service_code": "express", "zone_ids": ["zone_1", "zone_2"], ...},
                {"service_code": "standard", "zone_ids": ["zone_1"], ...}
            ],
            "service_rates": [
                {"service_id": "0", "zone_id": "zone_1", "rate": 10.0},
                {"service_id": "0", "zone_id": "zone_2", "rate": 15.0},
                {"service_id": "1", "zone_id": "zone_1", "rate": 5.0}
            ]
        }
    """
    # Zone deduplication: use (label, country_codes tuple) as key
    zone_registry: typing.Dict[str, typing.Dict] = {}  # key -> zone definition
    zone_key_to_id: typing.Dict[str, str] = {}  # key -> zone_id

    transformed_services: typing.List[typing.Dict] = []
    service_rates: typing.List[typing.Dict] = []
    zone_counter = 1

    def _get_zone_key(zone: typing.Dict) -> str:
        """Generate a unique key for zone deduplication."""
        label = zone.get("label") or ""
        country_codes = tuple(sorted(zone.get("country_codes") or []))
        postal_codes = tuple(sorted(zone.get("postal_codes") or []))
        cities = tuple(sorted(zone.get("cities") or []))
        return f"{label}:{country_codes}:{postal_codes}:{cities}"

    def _to_dict(obj: typing.Any) -> typing.Dict:
        """Convert object to dict if needed."""
        if hasattr(obj, "__dict__"):
            # attrs class - convert to dict
            return {k: v for k, v in obj.__dict__.items() if not k.startswith("_")}
        if hasattr(obj, "to_dict"):
            return obj.to_dict()
        return dict(obj) if obj else {}

    for idx, service_obj in enumerate(services):
        service = _to_dict(service_obj)
        service_id = service.get("id") or str(idx)
        legacy_zones = service.get("zones") or []

        zone_ids = []

        for zone_obj in legacy_zones:
            zone = _to_dict(zone_obj)
            zone_key = _get_zone_key(zone)

            # Check if we've seen this zone before
            if zone_key not in zone_key_to_id:
                # Create new shared zone
                zone_id = f"zone_{zone_counter}"
                zone_counter += 1
                zone_key_to_id[zone_key] = zone_id

                # Store zone definition (without rate - that goes in service_rates)
                zone_registry[zone_id] = {
                    "id": zone_id,
                    "label": zone.get("label"),
                    "country_codes": zone.get("country_codes") or [],
                    "postal_codes": zone.get("postal_codes") or [],
                    "cities": zone.get("cities") or [],
                    "transit_days": zone.get("transit_days"),
                    "transit_time": zone.get("transit_time"),
                    "radius": zone.get("radius"),
                    "latitude": zone.get("latitude"),
                    "longitude": zone.get("longitude"),
                }

            zone_id = zone_key_to_id[zone_key]
            zone_ids.append(zone_id)

            # Create service-zone rate mapping
            service_rates.append({
                "service_id": service_id,
                "zone_id": zone_id,
                "rate": zone.get("rate") or 0,
                "cost": zone.get("cost"),
                "min_weight": zone.get("min_weight"),
                "max_weight": zone.get("max_weight"),
                "transit_days": zone.get("transit_days"),
                "transit_time": zone.get("transit_time"),
            })

        # Create transformed service (without embedded zones)
        transformed_service = {
            k: v for k, v in service.items()
            if k not in ("zones", "surcharges")  # Remove embedded data
        }
        transformed_service["id"] = service_id
        # Deduplicate zone_ids preserving order (weight-bracket carriers repeat zones)
        transformed_service["zone_ids"] = list(dict.fromkeys(zone_ids))
        transformed_service["surcharge_ids"] = service.get("surcharge_ids") or []

        transformed_services.append(transformed_service)

    return {
        "zones": list(zone_registry.values()),
        "services": transformed_services,
        "service_rates": service_rates,
    }


def to_multi_piece_rates(
    package_rates: typing.List[typing.Tuple[str, typing.List[models.RateDetails]]]
) -> typing.List[models.RateDetails]:
    """Combine rates received separately per package into a single rate list.

    Example:
        package_rates = [
            ("pkg_1_id", { "service": "standard", "total_charge": 10, ... }),
            ("pkg_2_id", { "service": "standard", "total_charge": 15, ... })
        ]
        result = to_multi_piece_rates(package_rates)

        print(result) # [{ "service": "standard", "total_charge": 25, ... }]


    :param package_rates: a tuple of a package identifier and the list of rates returned for that package.
    :return: a unified list of combined rates of same services.
    """
    if len(package_rates) == 0:
        return []

    multi_piece_rates = []
    max_rates = max([len(rates) for _, rates in package_rates])
    main_piece_rates: typing.List[models.RateDetails] = next(
        (rates for _, rates in package_rates if len(rates) == max_rates), []
    )

    for main in main_piece_rates:
        similar_rates: typing.List[typing.Optional[models.RateDetails]] = [
            next((rate for rate in rates if rate.service == main.service), None)
            for _, rates in package_rates
        ]

        if all(rate is not None for rate in similar_rates):
            all_charges: typing.List[models.ChargeDetails] = sum(
                [rate.extra_charges for rate in similar_rates], []
            )
            extra_charges: typing.Dict[str, models.ChargeDetails] = functools.reduce(
                lambda acc, charge: {
                    **acc,
                    charge.name: models.ChargeDetails(
                        name=charge.name,
                        amount=utils.NF.decimal(
                            charge.amount + getattr(acc.get(charge.name), "amount", 0.0)
                        ),
                        currency=charge.currency,
                    ),
                },
                all_charges,
                {},
            )
            total_charge = utils.NF.decimal(
                sum(
                    (
                        utils.NF.decimal(rate.total_charge or 0.0)
                        for rate in similar_rates
                    ),
                    0.0,
                )
            )
            multi_piece_rates.append(
                models.RateDetails(
                    carrier_name=main.carrier_name,
                    carrier_id=main.carrier_id,
                    currency=main.currency,
                    transit_days=main.transit_days,
                    service=main.service,
                    total_charge=total_charge,
                    extra_charges=list(extra_charges.values()),
                    meta=main.meta,
                )
            )

    return multi_piece_rates


def to_multi_piece_shipment(
    package_shipments: typing.List[typing.Tuple[str, models.ShipmentDetails]]
) -> models.ShipmentDetails:
    """Combine shipment received separately per package into a single master shipment.

    Example:
        package_shipments = [
            { "tracking_number": "123", "shipment_identifier": "id_123", "docs": { "label": "label1_base64==" }, ... },
            { "tracking_number": "124", "shipment_identifier": "id_123", "docs": { "label": "label2_base64==" }, ... }
        ]
        result = to_multi_piece_shipment(package_shipments)

        print(result)
        # {
        #   "tracking_number": "123",
        #   "docs": { "label": "label1_base64label2_base64==" },
        #   "meta": { "tracking_numbers": ["123", "124"], "shipment_identifiers": ["id_123", "id_124"] },
        #   ...
        # }


    :param package_shipments: a tuple of a package identifier and the shipment returned for that package.
    :return: a unified master shipment object.
    """

    master_shipment = next((shipment for _, shipment in package_shipments), None)

    if master_shipment is None or len(package_shipments) == 1:
        return master_shipment

    labels = []
    tracking_numbers = set()
    shipment_identifiers = set()
    label_type = master_shipment.label_type

    for _, shipment in package_shipments:
        labels.append(shipment.docs.label)
        if shipment.tracking_number:
            tracking_numbers.add(shipment.tracking_number)
        if shipment.shipment_identifier:
            shipment_identifiers.add(shipment.shipment_identifier)

    return models.ShipmentDetails(
        carrier_name=master_shipment.carrier_name,
        carrier_id=master_shipment.carrier_id,
        tracking_number=master_shipment.tracking_number,
        shipment_identifier=master_shipment.shipment_identifier,
        label_type=label_type,
        docs=models.Documents(label=utils.bundle_base64(labels, label_type)),
        meta={
            **master_shipment.meta,
            "tracking_numbers": list(tracking_numbers),
            "shipment_identifiers": list(shipment_identifiers),
        },
    )
