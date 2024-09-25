"""Karrio TNT Connect Italy tracking API implementation."""

import karrio.schemas.tnt_it.tracking as tnt

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.tnt_it.error as error
import karrio.providers.tnt_it.utils as provider_utils
import karrio.providers.tnt_it.units as provider_units


def parse_tracking_response(
    _response: lib.Deserializable[typing.List[typing.Tuple[str, lib.Element]]],
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
    data: lib.Element,
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

    # map data to convert karrio model to tnt_it specific type
    request = tnt.Document(
        Application=settings.connection_config.application.state or "MYTRA",
        Version="3.0",
        Login=tnt.LoginType(
            Customer=settings.customer,
            User=settings.username,
            Password=settings.password,
            LangID=settings.connection_config.lang_id.state or "IT",
        ),
        SearchCriteria=tnt.SearchCriteriaType(
            AccountNo=settings.account_number,
            ConNo=payload.tracking_number,
            RTLSearch=None,
            StartDate=None,
            EndDate=None,
        ),
        SearchParameters=tnt.SearchParametersType(
            SearchType="Detail",
            SearchOption="ConsignmentTracking",
            SearchKeyValue=None,
            SearchMethod=None,
        ),
        ExtraDetails=None,
    )

    return lib.Serializable(request, lib.to_xml)
