import karrio.schemas.mydhl.rating_request as mydhl
import karrio.schemas.mydhl.rating_response as rating

import typing
import datetime
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.mydhl.error as error
import karrio.providers.mydhl.utils as provider_utils
import karrio.providers.mydhl.units as provider_units


def parse_rate_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    extra = dict(exchangeRate=response.get("exchangeRate", []))

    messages = error.parse_error_response(response, settings)
    rates = [
        _extract_details(rate, settings, extra=extra)
        for rate in response.get("products", [])
    ]

    return rates, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
    extra: typing.Optional[dict] = {},
) -> models.RateDetails:
    rate = lib.to_object(rating.ProductType, data)
    service = provider_units.ShippingService.map(rate.productCode)
    total_price = lib.identity(rate.totalPrice[0].priceValue)
    currency = lib.identity(
        lib.failsafe(lambda: extra["exchangeRates"][0]["currency"])
        or lib.failsafe(lambda: rate.totalPrice[0].priceCurrency)
        or "EUR"
    )

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=service.name_or_key,
        total_charge=lib.to_money(total_price),
        currency=currency,
        extra_charges=[
            models.ChargeDetails(
                name=charge.chargeType,
                amount=lib.to_money(charge.priceValue),
                currency=charge.priceCurrency,
            )
            for charge in rate.totalPrice[0].charges
        ],
        meta=dict(
            service_name=rate.productName,
            pricingDate=rate.pricingDate,
            **extra,
        ),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    billing_address = lib.to_address(payload.billing_address or shipper)
    packages = lib.to_packages(payload.parcels)
    services = lib.to_services(payload.services, provider_units.ShippingService)
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
    )

    # map data to convert karrio model to mydhl specific type
    request = mydhl.RatingRequestType(
        customerDetails=mydhl.CustomerDetailsType(
            shipperDetails=mydhl.ErDetailsType(
                postalCode=shipper.postal_code,
                cityName=shipper.city,
                addressLine1=shipper.address_line1,
                addressLine2=shipper.address_line2,
                countryCode=shipper.country_code,
                addressLine3=None,
            ),
            receiverDetails=mydhl.ErDetailsType(
                postalCode=recipient.postal_code,
                cityName=recipient.city,
                addressLine1=recipient.address_line1,
                addressLine2=recipient.address_line2,
                countryCode=recipient.country_code,
                addressLine3=None,
            ),
        ),
        accounts=[
            mydhl.AccountType(
                typeCode="shipper",
                number=settings.account_number,
            )
        ],
        productsAndServices=[
            mydhl.ProductsAndServiceType(
                productCode=service.code,
                localProductCode=None,
            )
            for service in services
        ],
        payerCountryCode=billing_address.country_code,
        plannedShippingDateAndTime=lib.fdatetime(
            options.shipment_date.state or datetime.datetime.now(),
            current_format="%Y-%m-%d",
            output_format="%Y-%m-%dT%H:%M:%SGMT%z",
        ),
        unitOfMeasurement="metric",
        isCustomsDeclarable=not packages.is_document,
        monetaryAmount=(
            [
                mydhl.MonetaryAmountType(
                    typeCode="declaredValue",
                    value=options.declared_value.amount,
                    currency=options.currency.state or "EUR",
                )
            ]
            if options.declared_value.state
            else []
        ),
        estimatedDeliveryDate=mydhl.EstimatedDeliveryDateType(
            isRequested=True,
            typeCode="QDDC",
        ),
        getAdditionalInformation=[
            mydhl.EstimatedDeliveryDateType(
                isRequested=True,
                typeCode="allValueAddedServices",
            )
        ],
        returnStandardProductsOnly=False,
        nextBusinessDay=True,
        productTypeCode="all",
        packages=[
            mydhl.PackageType(
                typeCode=provider_units.PackagingType.map(package.packaging).value,
                weight=package.weight.KG,
                dimensions=mydhl.DimensionsType(
                    length=package.length.CM,
                    width=package.width.CM,
                    height=package.height.CM,
                ),
            )
            for package in packages
        ],
    )

    return lib.Serializable(request, lib.to_dict)
