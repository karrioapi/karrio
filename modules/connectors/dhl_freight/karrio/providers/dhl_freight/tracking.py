"""DHL Freight tracking — DHL Group Unified Tracking API (UTAPI).

`GET /track/shipments?trackingNumber=<id>&service=freight` with a
`DHL-API-Key` header (the same cross-BU API dhl_universal uses). See SPECS.md.
"""

import karrio.core.models as models
import karrio.lib as lib
import karrio.providers.dhl_freight.error as error
import karrio.providers.dhl_freight.units as provider_units
import karrio.providers.dhl_freight.utils as provider_utils
import karrio.schemas.dhl_freight.tracking_response as dhl_freight_track

date_formats = ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S%z"]


def parse_tracking_response(
    _response: lib.Deserializable[list[dict]],
    settings: provider_utils.Settings,
) -> tuple[list[models.TrackingDetails], list[models.Message]]:
    responses = _response.deserialize()
    messages = error.parse_error_response(
        [r for r in responses if "shipments" not in r],
        settings,
    )
    details = [
        _extract_details(lib.to_object(dhl_freight_track.ShipmentType, r["shipments"][0]), settings)
        for r in responses
        if r.get("shipments")
    ]

    return details, messages


def _extract_details(
    shipment: dhl_freight_track.ShipmentType,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    latest = lib.failsafe(
        lambda: (shipment.status.statusCode or shipment.status.status or shipment.events[0].statusCode) or ""
    ).lower()
    status = next(
        (s.name for s in provider_units.TrackingStatus if latest in s.value),
        provider_units.TrackingStatus.in_transit.name,
    )

    def _short(ts):
        return ts.split(".")[0] if ts else None

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=str(shipment.id),
        status=status,
        events=[
            models.TrackingEvent(
                date=lib.fdate(_short(event.timestamp), try_formats=date_formats),
                time=lib.flocaltime(_short(event.timestamp), try_formats=date_formats),
                description=event.description or event.status or " ",
                code=event.statusCode or "",
                location=lib.failsafe(lambda e=event: e.location.address.addressLocality),
                timestamp=lib.fiso_timestamp(_short(event.timestamp), current_format="%Y-%m-%dT%H:%M:%S"),
                status=next(
                    (
                        s.name
                        for s in provider_units.TrackingStatus
                        if (event.statusCode or "").lower() in s.value or (event.status or "").lower() in s.value
                    ),
                    None,
                ),
            )
            for event in (shipment.events or [])
        ],
        estimated_delivery=lib.fdate(_short(shipment.estimatedTimeOfDelivery), try_formats=date_formats),
        delivered=status == "delivered",
        info=models.TrackingInfo(
            carrier_tracking_link=settings.tracking_url.format(shipment.id),
            shipment_service=lib.failsafe(lambda: shipment.details.product.productName),
            shipment_origin_country=lib.failsafe(lambda: shipment.origin.address.countryCode),
            shipment_destination_country=lib.failsafe(lambda: shipment.destination.address.countryCode),
            package_weight=lib.failsafe(lambda: shipment.details.weight.value),
        ),
        meta=dict(
            license_plates=lib.failsafe(lambda: shipment.details.pieceIds) or [],
            reference=lib.failsafe(lambda: shipment.details.references.number),
        ),
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    # One UTAPI query per tracking number; `service=freight` scopes the lookup
    # to the DHL Freight business unit.
    requests = [
        dict(
            trackingNumber=number,
            service="freight",
            language=settings.connection_config.language.state or "en",
        )
        for number in payload.tracking_numbers
    ]

    return lib.Serializable(requests, lib.to_dict)
