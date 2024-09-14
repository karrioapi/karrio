"""Karrio Easyship rating API implementation."""

import karrio.schemas.easyship.rate_request as easyship
import karrio.schemas.easyship.rate_response as rating

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.easyship.error as error
import karrio.providers.easyship.utils as provider_utils
import karrio.providers.easyship.units as provider_units


def parse_rate_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    rates = [_extract_details(rate, settings) for rate in response]

    return rates, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    details = None  # parse carrier rate type

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service="",  # extract service from rate
        total_charge=lib.to_money(0.0),  # extract the rate total rate cost
        currency="",  # extract the rate pricing currency
        transit_days=0,  # extract the rate transit days
        meta=dict(
            service_name="",  # extract the rate service human readable name
        ),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    services = lib.to_services(payload.services, provider_units.ShippingService)
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    # map data to convert karrio model to easyship specific type
    request = easyship.RateRequestType(
        courierselection=easyship.CourierSelectionType(
            applyshippingrules=None,
            showcourierlogourl=None,
        ),
        destinationaddress=easyship.NAddressType(
            countryalpha2=None,
            city=None,
            companyname=easyship.Any(),
            contactemail=None,
            contactname=None,
            contactphone=easyship.Any(),
            line1=None,
            line2=None,
            postalcode=None,
            state=None,
            validation=easyship.ValidationType(
                detail=None,
                status=None,
                comparison=easyship.ComparisonType(
                    changes=None,
                    post=None,
                    pre=None,
                ),
            ),
        ),
        incoterms=None,
        insurance=easyship.InsuranceType(
            insuredamount=None,
            insuredcurrency=None,
            isinsured=None,
        ),
        originaddress=easyship.NAddressType(
            countryalpha2=None,
            city=None,
            companyname=easyship.Any(),
            contactemail=None,
            contactname=None,
            contactphone=easyship.Any(),
            line1=None,
            line2=None,
            postalcode=None,
            state=None,
            validation=easyship.ValidationType(
                detail=None,
                status=None,
                comparison=easyship.ComparisonType(
                    changes=None,
                    post=None,
                    pre=None,
                ),
            ),
        ),
        parcels=[
            easyship.ParcelType(
                box=easyship.BoxType(
                    height=None,
                    length=None,
                    weight=None,
                    width=None,
                    slug=None,
                ),
                items=[
                    easyship.ItemType(
                        containsbatterypi966=None,
                        containsbatterypi967=None,
                        containsliquids=None,
                        declaredcurrency=None,
                        dimensions=easyship.DimensionsType(
                            height=None,
                            length=None,
                            width=None,
                        ),
                        origincountryalpha2=None,
                        quantity=None,
                        actualweight=None,
                        category=None,
                        declaredcustomsvalue=None,
                        description=None,
                        sku=None,
                    )
                ],
                totalactualweight=None,
            )
        ],
        shippingsettings=easyship.ShippingSettingsType(
            outputcurrency=None,
            units=easyship.UnitsType(
                dimensions=None,
                weight=None,
            ),
        ),
    )

    return lib.Serializable(request, lib.to_dict)
