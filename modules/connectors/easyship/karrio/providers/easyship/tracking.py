"""Karrio Easyship tracking API implementation."""

import karrio.schemas.easyship.tracking_request as easyship
import karrio.schemas.easyship.tracking_response as tracking

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.easyship.error as error
import karrio.providers.easyship.utils as provider_utils
import karrio.providers.easyship.units as provider_units


def parse_tracking_response(
    _response: lib.Deserializable[typing.List[typing.Tuple[str, dict]]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    responses = _response.deserialize()

    messages: typing.List[models.Message] = sum(
        [
            error.parse_error_response(response, settings, tracking_number=_)
            for _, response in responses
        ],
        start=[],
    )
    tracking_details = [_extract_details(details, settings) for _, details in responses]

    return tracking_details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    details = None  # parse carrier tracking object type
    status = next(
        (
            status.name
            for status in list(provider_units.TrackingStatus)
            if getattr(details, "status", None) in status.value
        ),
        provider_units.TrackingStatus.in_transit.name,
    )

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number="",
        events=[
            models.TrackingEvent(
                date=lib.fdate(""),
                description="",
                code="",
                time=lib.flocaltime(""),
                location="",
            )
            for event in []
        ],
        estimated_delivery=lib.fdate(""),
        delivered=status == "delivered",
        status=status,
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:

    # map data to convert karrio model to easyship specific type
    request = easyship.TrackingRequestType(
        destinationaddress=easyship.NAddressType(
            city=None,
            companyname=None,
            contactemail=None,
            contactname=None,
            contactphone=None,
            countryalpha2=None,
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
        originaddress=easyship.NAddressType(
            city=None,
            companyname=None,
            contactemail=None,
            contactname=None,
            contactphone=None,
            countryalpha2=None,
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
        courierid=None,
        originaddressid=None,
        platformordernumber=None,
        items=[
            easyship.ItemType(
                description=None,
                quantity=None,
            )
        ],
        trackingnumber=None,
    )

    return lib.Serializable(request, lib.to_dict)
