import typing
import functools
import karrio.core.utils as utils
import karrio.core.models as models


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
                        amount=charge.amount
                        + getattr(acc.get(charge.name), "amount", 0.0),
                    ),
                },
                all_charges,
                {},
            )
            total_charge = (
                sum(
                    (
                        utils.NF.decimal(rate.total_charge or 0)
                        for rate in similar_rates
                    ),
                    0.0,
                )
                if any(rate.total_charge for rate in similar_rates)
                else None
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
