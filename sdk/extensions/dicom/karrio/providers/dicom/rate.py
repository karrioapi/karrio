from karrio.schemas.dicom.rates import (
    RateRequest as DicomRateRequest,
    Address,
    Parcel,
    Surcharge,
    Rate,
    RateResponse,
)

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.dicom.error as provider_error
import karrio.providers.dicom.units as provider_units
import karrio.providers.dicom.utils as provider_utils


def parse_rate_response(
    _response: lib.Deserializable[dict], settings: provider_utils.Settings
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    errors = provider_error.parse_error_response(response, settings)
    rate_response = (
        lib.to_object(RateResponse, response) if "rates" in response else RateResponse()
    )
    details = [
        _extract_details(rate, rate_response, settings)
        for rate in (rate_response.rates or [])
    ]

    return details, errors


def _extract_details(
    rate: Rate, response: RateResponse, settings: provider_utils.Settings
) -> models.RateDetails:
    charges = [
        ("Base Charge", rate.basicCharge),
        ("Discount", rate.discountAmount),
        ("Taxes", rate.taxes),
        *((charge.name, charge.amount) for charge in rate.surcharges),
    ]

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        currency="CAD",
        transit_days=response.delay,
        service=provider_units.Service(rate.rateType),
        total_charge=lib.to_decimal(rate.total),
        extra_charges=[
            provider_units.ChargeDetails(
                currency="CAD",
                name=name,
                amount=lib.to_decimal(charge),
            )
            for name, charge in charges
            if charge
        ],
        meta=dict(accountType=rate.accountType),
    )


def rate_request(
    payload: models.RateRequest, settings: provider_utils.Settings
) -> lib.Serializable:
    packages = lib.to_packages(payload.parcels)
    service = (
        provider_units.Services(payload.services, provider_units.Service).first
        or provider_units.Service.dicom_ground_delivery.value
    ).value
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    request = DicomRateRequest(
        category="Parcel",
        paymentType=provider_units.PaymentType.prepaid.value,
        deliveryType=service,
        unitOfMeasurement=provider_units.UnitOfMeasurement.KC.value,
        sender=Address(
            postalCode=payload.shipper.postal_code,
            provinceCode=payload.shipper.state_code,
            countryCode=payload.shipper.country_code,
            name=(payload.shipper.company_name or payload.shipper.person_name),
        ),
        consignee=Address(
            postalCode=payload.recipient.postal_code,
            provinceCode=payload.recipient.state_code,
            countryCode=payload.recipient.country_code,
            name=(payload.recipient.company_name or payload.recipient.person_name),
        ),
        parcels=[
            Parcel(
                quantity=1,
                parcelType=provider_units.ParcelType[
                    package.packaging_type or "dicom_box"
                ].value,
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
            Surcharge(
                type=option.code,
                value=lib.to_money(option.state),
            )
            for _, option in options.items()
        ],
        appointment=None,
    )

    return lib.Serializable(request, lib.to_dict)
