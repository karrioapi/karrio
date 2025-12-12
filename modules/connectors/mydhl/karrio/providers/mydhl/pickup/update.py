"""Karrio MyDHL pickup update API implementation."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.mydhl.error as error
import karrio.providers.mydhl.utils as provider_utils
import karrio.providers.mydhl.units as provider_units
import karrio.schemas.mydhl.pickup_update_request as pickup_req
import karrio.schemas.mydhl.pickup_update_response as pickup_res


def parse_pickup_update_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.PickupDetails, typing.List[models.Message]]:
    """
    Parse pickup update response from MyDHL API

    _response: The carrier response to deserialize
    settings: The carrier connection settings

    Returns a tuple with (PickupDetails, List[Message])
    """
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    pickup = lib.identity(
        _extract_details(
            lib.to_object(pickup_res.PickupUpdateResponseType, response),
            settings,
        )
        if response.get("status") is None
        and response.get("dispatchConfirmationNumbers") is not None
        else None
    )

    return pickup, messages


def _extract_details(
    pickup: pickup_res.PickupUpdateResponseType,
    settings: provider_utils.Settings,
) -> models.PickupDetails:
    """
    Extract pickup details from MyDHL pickup update response

    pickup: The MyDHL PickupUpdateResponseType object
    settings: The carrier connection settings

    Returns a PickupDetails object with the pickup information
    """
    confirmation_number = next(
        (num for num in (pickup.dispatchConfirmationNumbers or []) if num),
        ""
    )

    return models.PickupDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        confirmation_number=confirmation_number,
        pickup_date=lib.fdate(pickup.nextPickupDate),
        ready_time=lib.ftime(pickup.readyByTime, try_formats=["%H:%M:%S", "%H:%M"]),
        meta=dict(
            confirmation_numbers=pickup.dispatchConfirmationNumbers,
            warnings=pickup.warnings,
        ),
    )


def pickup_update_request(
    payload: models.PickupUpdateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """
    Create a pickup update request for the carrier API

    payload: The standardized PickupUpdateRequest from karrio
    settings: The carrier connection settings

    Returns a Serializable object that can be sent to the carrier API
    """
    address = lib.to_address(payload.address)
    packages = lib.to_packages(payload.parcels)
    options = lib.to_shipping_options(payload.options)
    service = provider_units.ShippingService.map(
        payload.options.get("service") or "P"
    ).value_or_key

    # Build planned pickup date time in DHL format
    pickup_datetime = lib.fdatetime(
        f"{payload.pickup_date}T{payload.ready_time}:00",
        "%Y-%m-%dT%H:%M:%S",
        output_format="%Y-%m-%dT%H:%M:%S GMT+00:00",
    )

    request = pickup_req.PickupUpdateRequestType(
        dispatchConfirmationNumber=payload.confirmation_number,
        originalShipperAccountNumber=settings.account_number,
        plannedPickupDateAndTime=pickup_datetime,
        closeTime=payload.closing_time,
        location=options.pickup_location.state or "reception",
        locationType="residence" if address.residential else "business",
        accounts=[
            pickup_req.AccountType(
                typeCode="shipper",
                number=settings.account_number,
            )
        ],
        specialInstructions=lib.identity(
            [
                pickup_req.SpecialInstructionType(
                    value=payload.instruction,
                )
            ]
            if payload.instruction
            else []
        ),
        remark=payload.instruction,
        customerDetails=pickup_req.CustomerDetailsType(
            shipperDetails=pickup_req.ErDetailsType(
                postalAddress=pickup_req.ReceiverDetailsPostalAddressType(
                    postalCode=address.postal_code,
                    cityName=address.city,
                    countryCode=address.country_code,
                    provinceCode=address.state_code,
                    addressLine1=address.address_line1,
                    addressLine2=address.address_line2,
                    countyName=address.suburb,
                    provinceName=address.state_name,
                    countryName=address.country_name,
                ),
                contactInformation=pickup_req.ContactInformationType(
                    email=address.email,
                    phone=address.phone_number,
                    mobilePhone=address.phone_number,
                    companyName=address.company_name,
                    fullName=address.person_name,
                ),
            ),
        ),
        shipmentDetails=[
            pickup_req.ShipmentDetailType(
                productCode=service,
                isCustomsDeclarable=False,
                unitOfMeasurement="metric",
                packages=[
                    pickup_req.PackageType(
                        typeCode=provider_units.PackagingType.map(package.packaging_type or "your_packaging").value,
                        weight=package.weight.value,
                        dimensions=pickup_req.DimensionsType(
                            length=package.length.value,
                            width=package.width.value,
                            height=package.height.value,
                        )
                        if package.length.value and package.width.value and package.height.value
                        else None,
                    )
                    for package in packages
                ]
                if packages
                else [pickup_req.PackageType(weight=1.0)],
            )
        ],
    )

    return lib.Serializable(request, lib.to_dict)
