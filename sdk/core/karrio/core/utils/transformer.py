from functools import reduce
from typing import Dict, List, Optional, Tuple
from karrio.core.models import Documents, RateDetails
from karrio.core.models import ChargeDetails
from karrio.core.utils import NF
from karrio.core.models import ShipmentDetails
from karrio.core.utils.helpers import bundle_base64


def to_multi_piece_rates(
    package_rates: List[Tuple[str, List[RateDetails]]]
) -> List[RateDetails]:
    """
    Convert a list of package rates to a multi-piece combined rates.
    """
    multi_piece_rates = []
    max_rates = max([len(rates) for _, rates in package_rates])
    main_piece_rates: List[RateDetails] = next(
        (rates for _, rates in package_rates if len(rates) == max_rates), []
    )

    for main in main_piece_rates:
        similar_rates: List[Optional[RateDetails]] = [
            next((rate for rate in rates if rate.service == main.service), None)
            for _, rates in package_rates
        ]

        if all(rate is not None for rate in similar_rates):
            all_charges: List[ChargeDetails] = sum(
                [rate.extra_charges for rate in similar_rates], []
            )
            extra_charges: Dict[str, ChargeDetails] = reduce(
                lambda acc, charge: {
                    **acc,
                    charge.name: ChargeDetails(
                        name=charge.name,
                        amount=charge.amount
                        + getattr(acc.get(charge.name), "amount", 0.0),
                    ),
                },
                all_charges,
                {},
            )
            discount = (
                sum((NF.decimal(rate.discount or 0) for rate in similar_rates), 0.0)
                if any(rate.discount for rate in similar_rates)
                else None
            )
            base_charge = (
                sum((NF.decimal(rate.base_charge or 0) for rate in similar_rates), 0.0)
                if any(rate.base_charge for rate in similar_rates)
                else None
            )
            total_charge = (
                sum((NF.decimal(rate.total_charge or 0) for rate in similar_rates), 0.0)
                if any(rate.total_charge for rate in similar_rates)
                else None
            )
            duties_and_taxes = (
                sum(
                    (NF.decimal(rate.duties_and_taxes or 0) for rate in similar_rates),
                    0.0,
                )
                if any(rate.duties_and_taxes for rate in similar_rates)
                else None
            )

            multi_piece_rates.append(
                RateDetails(
                    carrier_name=main.carrier_name,
                    carrier_id=main.carrier_id,
                    currency=main.currency,
                    transit_days=main.transit_days,
                    service=main.service,
                    discount=discount,
                    base_charge=base_charge,
                    total_charge=total_charge,
                    duties_and_taxes=duties_and_taxes,
                    extra_charges=list(extra_charges.values()),
                    meta=main.meta,
                )
            )

    return multi_piece_rates


def to_multi_piece_shipment(
    package_shipments: List[Tuple[str, ShipmentDetails]]
) -> ShipmentDetails:
    master_shipment = next((shipment for _, shipment in package_shipments), None)

    if master_shipment is None or len(package_shipments) == 1:
        return master_shipment

    labels = []
    tracking_numbers = set()
    tracking_identifiers = set()
    label_type = master_shipment.label_type

    for _, shipment in package_shipments:
        labels.append(shipment.docs.label)
        if shipment.tracking_number:
            tracking_numbers.add(shipment.tracking_number)
        if shipment.shipment_identifier:
            tracking_identifiers.add(shipment.shipment_identifier)

    return ShipmentDetails(
        carrier_name=master_shipment.carrier_name,
        carrier_id=master_shipment.carrier_id,
        tracking_number=master_shipment.tracking_number,
        shipment_identifier=master_shipment.shipment_identifier,
        label_type=label_type,
        docs=Documents(label=bundle_base64(labels, label_type)),
        meta={
            **master_shipment.meta,
            "tracking_numbers": list(tracking_numbers),
            "tracking_identifiers": list(tracking_identifiers),
        },
    )
