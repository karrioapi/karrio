from tnt_lib.pricing_response import (
    priceResponse,
    ratedServices,
    ratedService,
)
from tnt_lib.pricing_request import (
    priceRequest,
    priceCheck,
    address,
    account,
    product,
    insurance,
    options as optionsType,
    consignmentDetails,
)

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.purolator.error as provider_error
import karrio.providers.purolator.units as provider_units
import karrio.providers.purolator.utils as provider_utils


def parse_rate_response(
    response: lib.Element,
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    price_response = lib.find_element(
        "priceResponse", response, priceResponse, first=True
    )

    if price_response is not None and price_response.ratedServices is not None:
        rate_details = [
            _extract_detail((price_response.ratedServices, service), settings)
            for service in price_response.ratedServices.ratedService
        ]
    else:
        rate_details = []

    return rate_details, provider_error.parse_error_response(response, settings)


def _extract_detail(
    details: typing.Tuple[ratedServices, ratedService],
    settings: provider_utils.Settings,
) -> models.RateDetails:
    rate, service = details
    charges = [
        ("Base charge", service.totalPriceExclVat),
        ("VAT", service.vatAmount),
        *(
            (charge.description, charge.chargeValue)
            for charge in service.chargeElements.chargeElement
        ),
    ]

    return models.RateDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        currency=rate.currency,
        service=str(service.product.id),
        total_charge=lib.to_decimal(service.totalPrice),
        extra_charges=[
            models.ChargeDetails(
                name=name,
                amount=lib.to_decimal(amount),
                currency=rate.currency,
            )
            for name, amount in charges
            if amount
        ],
        meta=dict(service_name=service.product.productDesc),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable[priceRequest]:
    package = lib.to_packages(payload.parcels).single
    service = lib.to_services(payload.services, provider_units.ShipmentService).first
    options = lib.to_shipping_options(
        payload.options,
        package_options=package.options,
        initializer=provider_units.shipping_options_initializer,
    )

    request = priceRequest(
        appId=settings.username,
        appVersion="3.0",
        priceCheck=priceCheck(
            rateId=None,
            sender=address(
                country=payload.shipper.country_code,
                town=payload.shipper.city,
                postcode=payload.shipper.postal_code,
            ),
            delivery=address(
                country=payload.recipient.country_code,
                town=payload.recipient.city,
                postcode=payload.recipient.postal_code,
            ),
            collectionDateTime=lib.fdatetime(
                options.shipment_date, output_format="%Y-%m-%dT%H:%M:%S"
            ),
            product=product(
                id=getattr(service, "value", None),
                division=next(
                    (code for label, code in options if "division" in label), None
                ),
                productDesc=None,
                type_=("D" if package.parcel.is_document else "N"),
                options=(
                    optionsType(
                        option=[
                            option(optionCode=option.code)
                            for _, option in options.items()
                        ]
                    )
                    if any(options.items())
                    else None
                ),
            ),
            account=(
                account(
                    accountNumber=settings.account_number,
                    accountCountry=settings.account_country_code,
                )
                if any([settings.account_number, settings.account_country_code])
                else None
            ),
            insurance=(
                insurance(
                    insuranceValue=options.insurance, goodsValue=options.declared_value
                )
                if options.insurance is not None
                else None
            ),
            termsOfPayment=provider_units.PaymentType.sender.value,
            currency=options.currency,
            priceBreakDown=True,
            consignmentDetails=consignmentDetails(
                totalWeight=package.weight.KG,
                totalVolume=package.volume.value,
                totalNumberOfPieces=1,
            ),
            pieceLine=None,
        ),
    )

    return lib.Serializable(request, lib.to_xml)
