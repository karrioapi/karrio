import karrio.schemas.allied_express.tracking_request as allied
import karrio.schemas.allied_express.tracking_response as tracking
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.allied_express.error as error
import karrio.providers.allied_express.utils as provider_utils
import karrio.providers.allied_express.units as provider_units


def parse_tracking_response(
    _response: lib.Deserializable[
        typing.List[typing.Tuple[str, provider_utils.AlliedResponse]]
    ],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    responses = _response.deserialize()

    messages: typing.List[models.Message] = sum(
        [
            error.parse_error_response(response, settings, tracking_number=_)
            for _, response in responses
            if response.is_error
        ],
        start=[],
    )
    tracking_details = [
        _extract_details(details.data["result"], settings)
        for _, details in responses
        if not details.is_error and "result" in (details.data or {})
    ]

    return tracking_details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    result = lib.to_object(tracking.ResultType, data)
    description = result.statusBarcodesList.scannedStatus or "In Transit"
    delivered = "delivered" in description
    status = next(
        (
            status.name
            for status in list(provider_units.TrackingStatus)
            if description in status.value
        ),
        provider_units.TrackingStatus.in_transit.name,
    )

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=result.statusBarcodesList.consignmentNote,
        events=[
            models.TrackingEvent(
                code=result.statusBarcodesList.scannedBarcode,
                location=result.statusBarcodesList.depotLocation,
                description=description,
                date=lib.fdate(
                    result.statusBarcodesList.scannnedTimestamp,
                    "%Y-%m-%dT%H:%M:%S.%f%z",
                ),
                time=lib.flocaltime(
                    result.statusBarcodesList.scannnedTimestamp,
                    "%Y-%m-%dT%H:%M:%S.%f%z",
                ),
            )
        ],
        status=status,
        delivered=delivered,
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    request = [
        allied.TrackingRequestType(shipmentno=tracking_number)
        for tracking_number in payload.tracking_numbers
    ]

    return lib.Serializable(request, lib.to_dict)
