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
    """Send one or multiple tracking request(s) to Easyship.
    the payload must match the following schema:
    {
        "tracking_numbers": ["123456789"],
        "shipment_ids": ["ESSG10006002"],
        "options": {
            "123456789": {
                "carrier": "usps",
                "easyship_shipment_id": "trk_xxxxxxxx",  # optional
            }
        }
    }
    """

    requests: typing.List[dict] = []

    for tracking_number in payload.tracking_numbers:
        options = payload.options.get(tracking_number) or {}
        shipment_id = lib.identity(
            options.get("easyship_shipment_id")
            or payload.options.get("easyship_shipment_id")
        )
        should_add = lib.identity(
            shipment_id is not None
            and not any(_.get("easyship_shipment_id") == shipment_id for _ in requests)
        )

        if should_add:
            requests.append(
                dict(
                    tracking_number=tracking_number,
                    shipment_id=shipment_id,
                    carrier=options.get("carrier"),
                )
            )

    return lib.Serializable(requests, lib.to_dict)
