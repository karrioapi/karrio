from typing import List, Tuple, cast
from ics_courier_lib.services import (
    GetEstimatedCharges,
    Authenticate,
    PackgeInfoToGetCharges,
    ArrayOfPieceInfo,
    PieceInfo,
    ResponseGetCharges,
    SurCharge,
)
from purplship.core.models import (
    RateRequest,
    RateDetails,
    Message,
    ChargeDetails
)
from purplship.core.units import Packages, Services, Currency
from purplship.core.utils import create_envelope, Serializable, Envelope, Element, NF, XP
from purplship.providers.ics_courier.error import parse_error_response
from purplship.providers.ics_courier.utils import Settings
from purplship.providers.ics_courier.units import Service


def parse_rate_response(response: Element, settings: Settings) -> Tuple[List[RateDetails], List[Message]]:
    estimate = XP.find("GetEstimatedChargesResult", response, ResponseGetCharges, first=True)
    product = XP.find("product", response, first=True)

    details: List[RateDetails] = [
        _extract_rate_details((product, estimate), settings)
    ]

    return details, parse_error_response(response, settings)


def _extract_rate_details(response: Tuple[Element, ResponseGetCharges], settings: Settings) -> RateDetails:
    product, rate = response
    charges = [
        *[
            (charge.SurChargeName, charge.SurChargeAmount)
            for charge in cast(List[SurCharge], rate.SurCharges)
        ],
        *[
            (name, value) for name, value in
            [("Fuel Charges", rate.FuelCharges),
             ("Insurance Charges", rate.InsuranceCharges)]
            if (value or 0) > 0
        ]
    ]

    return RateDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        service=Service(product.text),
        currency=Currency.CAD.name,
        base_charge=NF.decimal(rate.BaseCharges),
        total_charge=NF.decimal(rate.BaseCharges),
        extra_charges=[
            ChargeDetails(
                name=name,
                amount=amount,
                currency=Currency.CAD.name,
            )
            for name, amount in charges
        ]
    )


def rate_request(payload: RateRequest, settings: Settings) -> Serializable[Envelope]:
    packages = Packages(payload.parcels)
    product = Services(payload.services, Service).first

    request = create_envelope(
        body_content=GetEstimatedCharges(
            AuthenicateAccount=Authenticate(
                AccountID=settings.account_id,
                Password=settings.password,
            ),
            PkgInfo=PackgeInfoToGetCharges(
                Product=(product or Service.ics_courier_ground.value),
                Pieces=ArrayOfPieceInfo(
                    PieceInfo=[
                        PieceInfo(
                            Weight=piece.weight.value,
                            WeightUnit=piece.weight.unit,
                            Length=piece.length.value,
                            Width=piece.width.value,
                            Height=piece.height.value,
                            DeclaredValue=None,
                        )
                        for piece in packages
                    ]
                ),
                FromPost=payload.shipper.postal_code,
                ToPost=payload.recipient.postal_code,
            )
        )
    )

    return Serializable(request, lambda _: (product, Settings.serialize(_)))
