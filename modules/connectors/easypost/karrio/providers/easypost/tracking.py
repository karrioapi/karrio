import karrio.schemas.easypost.trackers_response as easypost
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.easypost.error as error
import karrio.providers.easypost.utils as provider_utils
import karrio.providers.easypost.units as provider_units


def parse_tracking_response(
    _responses: lib.Deserializable[typing.List[typing.Tuple[str, dict]]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    responses = _responses.deserialize()
    errors: typing.List[models.Message] = sum(
        [
            error.parse_error_response(response, settings, tracking_number=code)
            for code, response in responses
            if "error" in response
        ],
        start=[],
    )
    trackers = [
        _extract_details(response, settings)
        for _, response in responses
        if "error" not in response
    ]

    return trackers, errors


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    tracker = lib.to_object(easypost.Tracker, data)
    expected_delivery = lib.fdate(tracker.est_delivery_date, "%Y-%m-%dT%H:%M:%SZ")
    events: typing.List[dict] = data.get("tracking_details", [])

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracker.tracking_code,
        events=[
            models.TrackingEvent(
                date=lib.fdate(event.get("datetime"), "%Y-%m-%dT%H:%M:%SZ"),
                description=event.get("message") or "",
                code=event.get("status"),
                time=lib.flocaltime(event.get("datetime"), "%Y-%m-%dT%H:%M:%SZ"),
                location=lib.join(
                    event.get("tracking_location", {}).get("city"),
                    event.get("tracking_location", {}).get("state"),
                    event.get("tracking_location", {}).get("zip"),
                    event.get("tracking_location", {}).get("country"),
                    join=True,
                    separator=", ",
                ),
            )
            for event in events
            if event.get("datetime") is not None
        ],
        delivered=(tracker.status == "delivered"),
        estimated_delivery=expected_delivery,
        info=models.TrackingInfo(
            carrier_tracking_link=tracker.public_url,
            package_weight=tracker.weight,
            signed_by=tracker.signed_by,
            shipment_destination_postal_code=getattr(
                tracker.carrier_detail, "zip", None
            ),
            shipment_origin_country=getattr(tracker.carrier_detail, "country", None),
            shipment_service=getattr(tracker.carrier_detail, "service", None),
        ),
        meta=dict(
            carrier=provider_units.CarrierId.map(tracker.carrier).name_or_key,
            shipment_id=tracker.shipment_id,
            tracker_id=tracker.id,
            fees=lib.to_dict(tracker.fees),
        ),
    )


def tracking_request(payload: models.TrackingRequest, _) -> lib.Serializable:
    """Send one or multiple tracking request(s) to EasyPost.
    the payload must match the following schema:
    {
        "tracking_numbers": ["123456789"],
        "options": {
            "123456789": {
                "carrier": "usps",
                "tracker_id": "trk_xxxxxxxx",  # optional
            }
        }
    }
    """
    requests = []

    for tracking_code in payload.tracking_numbers:
        options = payload.options.get(tracking_code)

        if options is None:
            raise ValueError(f"No options found for {tracking_code}")

        if "carrier" not in options:
            raise ValueError(
                "invalid options['tracking_number'].carriers."
                "Please provide a 'carrier_name' for each tracking_number"
            )

        requests.append(
            dict(
                tracking_code=tracking_code,
                carrier=provider_units.CarrierId.map(options["carrier"]).value_or_key,
                tracker_id=options.get("tracker_id"),
            )
        )

    return lib.Serializable(requests, lib.to_dict)
