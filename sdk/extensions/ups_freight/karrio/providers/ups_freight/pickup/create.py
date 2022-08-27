import ups_freight_lib.freight_pickup_request as ups
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.ups_freight.error as error
import karrio.providers.ups_freight.utils as provider_utils
import karrio.providers.ups_freight.units as provider_units


def parse_pickup_response(
    response: dict,
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    pickup_response = response.get("FreightPickupResponse") or {}
    response_messages = [
        *response.get("response", {}).get("errors", []),
        *pickup_response.get("Response", {}).get("Alert", []),
    ]

    messages = error.parse_error_response(response_messages, settings)
    pickup = (
        _extract_details(pickup_response, settings)
        if pickup_response.get("PickupRequestConfirmationNumber") is not None
        else None
    )

    return pickup, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.PickupDetails:
    return models.PickupDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        confirmation_number=data["PickupRequestConfirmationNumber"],
    )


def pickup_request(
    payload: models.PickupRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    address = lib.to_address(payload.address)
    packages = lib.to_packages(payload.parcels, options=payload.options)
    options = units.Options(payload.options, provider_units.PickupOption)

    request = ups.FreightPickupRequestType(
        FreightPickupRequest=ups.FreightPickupRequestClassType(
            Request=ups.RequestType(
                TransactionReference=ups.TransactionReferenceType(
                    CustomerContext="Pickup transactions",
                    TransactionIdentifier=None,
                )
            ),
            DestinationPostalCode=options.recipient_postal_code.state,
            DestinationCountryCode=(
                options.recipient_country_code.state or address.country_code
            ),
            Requester=ups.RequesterType(
                ThirdPartyIndicator=options.ups_freight_third_party_indicator.state,
                AttentionName=(address.person_name or address.company_name or "N/A"),
                EMailAddress=address.email,
                Name=(address.company_name or address.person_name or "N/A"),
                Phone=ups.PhoneType(Number=address.phone_number or "000 000 0000"),
            ),
            ShipFrom=ups.RequesterType(
                AttentionName=(address.person_name or address.company_name or "N/A"),
                EMailAddress=address.email,
                Name=(address.company_name or address.person_name or "N/A"),
                Phone=ups.PhoneType(Number=address.phone_number or "000 000 0000"),
                Address=ups.AddressType(
                    AddressLine=address.address_line,
                    City=address.city,
                    StateProvinceCode=address.state_code,
                    PostalCode=address.postal_code,
                    CountryCode=address.country_code,
                ),
            ),
            PickupDate=lib.to_date(payload.pickup_date).strftime("%Y%m%d"),
            EarliestTimeReady=lib.ftime(payload.ready_time, "%H:%M", "%H%M"),
            LatestTimeReady=lib.ftime(payload.closing_time, "%H:%M", "%H%M"),
            ShipmentServiceOptions=(
                ups.ShipmentServiceOptionsType(
                    FreezableProtectionIndicator=options.ups_freight_freezable_protection_indicator.state,
                    LimitedAccessPickupIndicator=options.ups_freight_limited_access_pickup_indicator.state,
                    LimitedAccessDeliveryIndicator=options.ups_freight_limited_access_delivery_indicator.state,
                    ExtremeLengthIndicator=options.ups_freight_extreme_length_indicator.state,
                )
                if any(
                    [
                        options.ups_freight_freezable_protection_indicator.state,
                        options.ups_freight_limited_access_pickup_indicator.state,
                        options.ups_freight_limited_access_delivery_indicator.state,
                        options.ups_freight_extreme_length_indicator.state,
                    ]
                )
                else None
            ),
            ShipmentDetail=(
                ups.ShipmentDetailType(
                    PackagingType=ups.PackagingTypeType(
                        Code=(
                            provider_units.PackagingType.map(packages.package_type)
                            or provider_units.PackagingType.ups_other
                        ).value
                    ),
                    NumberOfPieces=len(packages),
                    DescriptionOfCommodity=packages.description,
                    Weight=ups.WeightType(
                        UnitOfMeasurement=ups.PackagingTypeType(
                            Code=provider_units.WeightUnit.map(
                                packages.weight_unit
                            ).value,
                        ),
                        Value=packages.weight.value,
                    ),
                )
                if any(payload.parcels)
                else None
            ),
            PickupInstructions=payload.package_location,
            AdditionalComments=None,
            HandlingInstructions=None,
            SpecialInstructions=payload.instruction,
            DeliveryInstructions=None,
        )
    )

    return lib.Serializable(request, lib.to_dict)
