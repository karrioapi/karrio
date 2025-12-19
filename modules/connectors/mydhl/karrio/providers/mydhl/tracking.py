"""Karrio MyDHL tracking API implementation."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.mydhl.error as error
import karrio.providers.mydhl.utils as provider_utils
import karrio.providers.mydhl.units as provider_units
import karrio.schemas.mydhl.tracking_response as mydhl_res


def parse_tracking_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    tracking_details = [
        _extract_details(shipment, settings)
        for shipment in (response.get("shipments") or [])
    ]

    return tracking_details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    shipment = lib.to_object(mydhl_res.ShipmentType, data)
    # Events are ordered from most recent to oldest
    latest_event = shipment.events[0] if shipment.events else None
    status = next(
        (
            status.name
            for status in list(provider_units.TrackingStatus)
            if latest_event and getattr(latest_event, "typeCode", None) in status.value
        ),
        provider_units.TrackingStatus.in_transit.name,
    )
    delivered = status == "delivered"
    estimated_delivery = lib.fdate(
        shipment.estimatedTimeOfDelivery, "%Y-%m-%dT%H:%M:%S"
    )
    signature_image = lib.failsafe(
        lambda: (
            provider_utils.get_proof_of_delivery(
                str(shipment.shipmentTrackingNumber), settings
            )
            if delivered
            else None
        )
    )

    # fmt: off
    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=str(shipment.shipmentTrackingNumber),
        events=[
            models.TrackingEvent(
                date=lib.fdate(event.date),
                description=event.description,
                code=event.typeCode,
                time=lib.ftime(event.time, try_formats=["%H:%M:%S", "%H:%M"]),
                location=next((e.description for e in event.serviceArea or []), None),
                timestamp=lib.fiso_timestamp(
                    lib.fdate(event.date),
                    lib.ftime(event.time, try_formats=["%H:%M:%S", "%H:%M"]),
                ),
                status=next(
                    (
                        s.name
                        for s in list(provider_units.TrackingStatus)
                        if getattr(event, "typeCode", None) in s.value
                    ),
                    None,
                ),
                reason=next(
                    (
                        r.name
                        for r in list(provider_units.TrackingIncidentReason)
                        if getattr(event, "typeCode", None) in r.value
                    ),
                    None,
                ),
            )
            for event in (shipment.events or [])
        ],
        estimated_delivery=estimated_delivery,
        delivered=delivered,
        status=status,
        info=models.TrackingInfo(
            carrier_tracking_link=settings.tracking_url.format(shipment.shipmentTrackingNumber),
            shipment_service=provider_units.ShippingService.map(shipment.productCode).name_or_key,
            shipment_origin_country=lib.failsafe(lambda: shipment.shipperDetails.postalAddress.countryCode),
            shipment_origin_postal_code=lib.failsafe(lambda: shipment.shipperDetails.postalAddress.postalCode),
            shipment_destination_country=lib.failsafe(lambda: shipment.receiverDetails.postalAddress.countryCode),
            shipment_destination_postal_code=lib.failsafe(lambda: shipment.receiverDetails.postalAddress.postalCode),
            shipping_date=lib.fdate(shipment.shipmentTimestamp, "%Y-%m-%dT%H:%M:%S"),
            signed_by=getattr(latest_event, "signedBy", None),
            package_weight=lib.to_decimal(shipment.totalWeight),
            package_weight_unit=lib.failsafe(lambda: provider_units.WeightUnit.map(shipment.weightUnit).name),
            shipment_package_count=lib.to_int(shipment.numberOfPieces),
            expected_delivery=estimated_delivery,
        ),
        images=models.Images(signature_image=signature_image),
        meta=dict(
            product_code=shipment.productCode,
            description=shipment.description,
            shipment_timestamp=shipment.shipmentTimestamp,
        ),
    )
    # fmt: on


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    request = payload.tracking_numbers
    return lib.Serializable(
        request,
        lambda tracking_numbers: "&".join(
            f"shipmentTrackingNumber={num}" for num in tracking_numbers
        ),
    )
