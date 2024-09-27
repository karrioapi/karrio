"""Karrio Easyship tracking API implementation."""

# import karrio.schemas.easyship.tracking_request as easyship
# import karrio.schemas.easyship.tracking_response as tracking
import karrio.schemas.easyship.shipment_response as shipping

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
            error.parse_error_response(response, settings, shipment_id=_)
            for _, response in responses
        ],
        start=[],
    )
    tracking_details = [
        _extract_details(details, settings)
        for _, details in responses
        if details.get("shipment") is not None and any(details["shipment"]["trackings"])
    ]

    return tracking_details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    details = lib.to_object(shipping.ShipmentType, data["shipment"])
    master = details.trackings[0]
    status = next(
        (
            status.name
            for status in list(provider_units.TrackingStatus)
            if getattr(master, "tracking_state", None) in status.value
        ),
        provider_units.TrackingStatus.in_transit.name,
    )

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=master.tracking_number,
        delivered=status == "delivered",
        status=status,
        events=[
            models.TrackingEvent(
                code=str(master.leg_number),
                date=lib.ftime(details.updated_at, "%Y-%m-%dT%H:%M:%SZ"),
                time=lib.ftime(details.updated_at, "%Y-%m-%dT%H:%M:%SZ"),
                description="",
            )
        ],
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipment_ids = list(
        set(
            [
                payload.options.get("easyship_shipment_id"),
                *(payload.options.get("shipment_ids") or []),
            ]
        )
    )

    if len(shipment_ids) == 0:
        raise Exception(f"easyship_shipment_id is required for tracking request")

    # map data to convert karrio model to easyship specific type
    request = shipment_ids

    return lib.Serializable(request, lib.to_dict)
