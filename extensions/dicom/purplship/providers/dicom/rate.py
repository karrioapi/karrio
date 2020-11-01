from typing import Tuple, List
from pydicom.rates import (
    RateRequest as DicomRateRequest,
    Address,
    Parcel,
    Surcharge,
    Rate,
    RateResponse,
)
from purplship.core.units import Packages
from purplship.core.utils import Serializable, to_dict, decimal
from purplship.core.models import (
    ChargeDetails,
    RateRequest,
    RateDetails,
    Message
)

from purplship.providers.dicom.units import (
    UnitOfMeasurement,
    ParcelType,
    Service,
    Option,
    PaymentType
)
from purplship.providers.dicom.error import parse_error_response
from purplship.providers.dicom.utils import Settings


def parse_rate_response(response: dict, settings: Settings) -> Tuple[List[RateDetails], List[Message]]:
    errors = parse_error_response(response, settings)
    rate_response = (RateResponse(**response) if 'rates' in response else RateResponse())
    details = [
        _extract_details(rate, rate_response, settings)
        for rate in (rate_response.rates or [])
    ]

    return details, errors


def _extract_details(rate: Rate, response: RateResponse, settings: Settings) -> RateDetails:

    return RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        currency="CAD",
        transit_days=response.delay,
        service=Service(rate.rateType),
        discount=decimal(rate.discountAmount),
        base_charge=decimal(rate.basicCharge),
        total_charge=decimal(rate.total),
        duties_and_taxes=decimal(rate.taxes),
        extra_charges=[
            ChargeDetails(
                name=charge.name,
                amount=decimal(charge.amount),
                currency="CAD",
            )
            for charge in rate.surcharges
        ],
        meta=dict(accountType=rate.accountType)
    )


def rate_request(payload: RateRequest, settings: Settings) -> Serializable[DicomRateRequest]:
    packages = Packages(payload.parcels)
    service = next(
        (Service[s] for s in payload.services if s in Service.__members__),
        Service.dicom_ground_delivery
    ).value
    options = {
        key: (value if Option[key].value in ['DCV', 'COD'] else None)
        for key, value in payload.options
        if key in Option.__members__
    }

    request = DicomRateRequest(
        category="Parcel",
        paymentType=PaymentType.prepaid.value,
        deliveryType=service,
        unitOfMeasurement=UnitOfMeasurement.KC.value,
        sender=Address(
            postalCode=payload.shipper.postal_code,
            provinceCode=payload.shipper.state_code,
            countryCode=payload.shipper.country_code,
            name=(payload.shipper.company_name or payload.shipper.person_name)
        ),
        consignee=Address(
            postalCode=payload.recipient.postal_code,
            provinceCode=payload.recipient.state_code,
            countryCode=payload.recipient.country_code,
            name=(payload.recipient.company_name or payload.recipient.person_name)
        ),
        parcels=[
            Parcel(
                quantity=1,
                parcelType=ParcelType[package.packaging_type or "dicom_box"].value,
                id=None,
                weight=package.weight.KG,
                length=package.height.CM,
                depth=package.length.CM,
                width=package.width.CM,
                note=None,
                status=None,
                FCA_Class=None,
                hazmat=None,
                requestReturnLabel=None,
                returnWaybill=None,
            )
            for package in packages
        ],
        billing=settings.billing_account,
        promoCodes=None,
        surcharges=[
            Surcharge(type=key, value=value) for key, value in options.items()
        ],
        appointment=None,
    )

    return Serializable(request, to_dict)
