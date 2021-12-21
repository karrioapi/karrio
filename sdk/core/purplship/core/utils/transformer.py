from functools import reduce
from typing import Dict, List, Optional, Tuple
from purplship.core.models import RateDetails
from purplship.core.models import ChargeDetails
from purplship.core.utils import NF


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
