"""Karrio DTDC tracking API implementation."""

import karrio.schemas.dtdc.tracking_request as dtdc_req
import karrio.schemas.dtdc.tracking_response as dtdc_res

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.dtdc.error as error
import karrio.providers.dtdc.utils as provider_utils
import karrio.providers.dtdc.units as provider_units


def parse_tracking_response(
    _response: lib.Deserializable[typing.List[typing.Tuple[str, dict]]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    responses = _response.deserialize()

    messages: typing.List[models.Message] = sum(
        [
            error.parse_error_response(
                response, settings, tracking_number=tracking_number
            )
            for tracking_number, response in responses
        ],
        start=[],
    )

    tracking_details = [
        _extract_details(details, settings, tracking_number)
        for tracking_number, details in responses
        if details.get("statusCode") == 200 and details.get("status") == "SUCCESS"
    ]

    return tracking_details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
    tracking_number: str = None,
) -> models.TrackingDetails:
    """Extract tracking details from DTDC response data."""

    details: dtdc_res.TrackingResponseType = lib.to_object(
        dtdc_res.TrackingResponseType, data
    )

    tracking_number = lib.identity(
        lib.text(details.trackHeader.strRefNo)
        or lib.text(details.trackHeader.strShipmentNo)
    )
    status = next(
        (
            status.name
            for status in list(provider_units.TrackingStatus)
            if details.trackHeader.strStatus.upper() in status.value
        ),
        provider_units.TrackingStatus.in_transit.name,
    )
    delivered = status == "delivered"

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        events=[
            models.TrackingEvent(
                date=lib.fdate(event.strActionDate, "%d%m%Y"),
                time=lib.ftime(event.strActionTime, "%H%M"),
                description=event.strAction,
                location=event.strOrigin,
                code=event.strCode,
            )
            for event in reversed(details.trackDetails)
        ],
        delivered=delivered,
        status=status,
        info=models.TrackingInfo(
            carrier_tracking_link=settings.tracking_url.format(tracking_number),
            customer_name=details.trackHeader.strCNTypeName,
            package_weight=lib.failsafe(
                lambda: units.Weight(details.trackHeader.strWeight, "KG").value
            ),
            shipment_package_count=lib.to_int(details.trackHeader.strPieces),
            shipment_service=details.trackHeader.strCNTypeName,
        ),
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create tracking requests for DTDC API."""
    options = lib.units.Options(
        payload.options,
        option_type=lib.units.create_enum(
            "TrackingOptions",
            {
                "addtnlDtl": lib.OptionEnum("addtnlDtl", str, "Y"),
                "trkType": lib.OptionEnum(
                    "trkType",
                    lib.units.create_enum("TrkType", ["cnno", "reference"]),
                    "reference",
                ),
            },
        ),
    )

    request = [
        dtdc_req.TrackingRequestType(
            strcnno=tracking_number,
            trkType=options.trkType.state,
            addtnlDtl=options.addtnlDtl.state,
        )
        for tracking_number in payload.tracking_numbers
    ]

    return lib.Serializable(request, lib.to_dict)
