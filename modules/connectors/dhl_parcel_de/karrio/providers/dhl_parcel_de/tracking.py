import karrio.schemas.dhl_parcel_de.tracking_request as dhl
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.dhl_parcel_de.error as error
import karrio.providers.dhl_parcel_de.units as provider_units
import karrio.providers.dhl_parcel_de.utils as provider_utils


def parse_tracking_response(
    _response: lib.Deserializable[typing.List[lib.Element]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    responses = _response.deserialize()
    shipments = sum(
        [
            [
                s for s in lib.find_element("data", r)
                if s.get("name") == "piece-shipment"
                and (s.get("error-status") or "0") == "0"
            ]
            for r in responses
            if (r.get("code") or "0") == "0"
        ],
        [],
    )
    messages = sum(
        [
            error.parse_tracking_error_response(r, settings)
            for r in responses
            if r.get("code") and r.get("code") != "0"
        ]
        + [
            error.parse_tracking_error_response(s, settings)
            for r in responses
            for s in lib.find_element("data", r)
            if s.get("name") == "piece-shipment"
            and s.get("error-status")
            and s.get("error-status") != "0"
        ],
        [],
    )
    tracking_details = [
        _extract_tracking(s, settings) for s in shipments
    ]

    return [d for d in tracking_details if d], messages


def _extract_tracking(
    shipment: lib.Element,
    settings: provider_utils.Settings,
) -> typing.Optional[models.TrackingDetails]:
    tracking_number = (
        shipment.get("piece-code")
        or shipment.get("piece-identifier")
        or shipment.get("searched-piece-code")
    )
    if not tracking_number:
        return None

    delivered = shipment.get("delivery-event-flag") == "1"
    ice_code = (shipment.get("ice") or "").lower()
    status = (
        provider_units.TrackingStatus.delivered.name
        if delivered
        else next(
            (
                s.name
                for s in list(provider_units.TrackingStatus)
                if ice_code in s.value
            ),
            provider_units.TrackingStatus.in_transit.name,
        )
    )

    return models.TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=tracking_number,
        status=status,
        delivered=delivered,
        estimated_delivery=lib.fdate(shipment.get("delivery-date"), "%d.%m.%Y"),
        events=list(
            reversed(
                [
                    models.TrackingEvent(
                        date=lib.fdate(e.get("event-timestamp"), "%d.%m.%Y %H:%M"),
                        time=lib.flocaltime(e.get("event-timestamp"), "%d.%m.%Y %H:%M"),
                        timestamp=lib.fiso_timestamp(
                            e.get("event-timestamp"), current_format="%d.%m.%Y %H:%M"
                        ),
                        description=(
                            e.get("event-status")
                            or e.get("event-text")
                            or e.get("event-short-status")
                            or ""
                        ),
                        location=lib.join(
                            e.get("event-location"),
                            e.get("event-country"),
                            join=True,
                            separator=", ",
                        ),
                        code=e.get("standard-event-code") or (e.get("ice") or "").upper(),
                        status=next(
                            (
                                s.name
                                for s in list(provider_units.TrackingStatus)
                                if (e.get("ice") or "").lower() in s.value
                            ),
                            None,
                        ),
                        reason=next(
                            (
                                r.name
                                for r in list(provider_units.TrackingIncidentReason)
                                if (e.get("ric") or "").lower() in r.value
                            ),
                            None,
                        ),
                    )
                    for el in lib.find_element("data", shipment)
                    if el.get("name") == "piece-event-list"
                    for e in lib.find_element("data", el)
                    if e.get("name") == "piece-event" and e.get("event-timestamp")
                ]
            )
        ),
        info=models.TrackingInfo(
            carrier_tracking_link=settings.tracking_url.format(tracking_number),
            customer_name=(
                shipment.get("recipient-name") or shipment.get("pan-recipient-name")
            ),
            shipment_destination_country=shipment.get("dest-country"),
            shipment_destination_postal_code=shipment.get("pan-recipient-postalcode"),
            shipment_origin_country=shipment.get("origin-country"),
            shipment_service=shipment.get("product-name"),
            package_weight=lib.to_decimal(shipment.get("shipment-weight")),
            package_weight_unit="KG" if shipment.get("shipment-weight") else None,
            signed_by=shipment.get("recipient-id-text"),
        ),
        meta=dict(
            piece_id=shipment.get("piece-id"),
            product_code=shipment.get("product-code"),
            reference=(
                shipment.get("piece-customer-reference")
                or shipment.get("shipment-customer-reference")
            ),
        ),
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    tracking_numbers = payload.tracking_numbers
    batch_size = 20

    requests = [
        dhl.TrackingRequestType(
            appname=settings.tracking_appname,
            password=settings.tracking_password,
            request="d-get-piece-detail",
            language_code="en",
            piece_code=";".join(tracking_numbers[i : i + batch_size]),
        )
        for i in range(0, len(tracking_numbers), batch_size)
    ]

    return lib.Serializable(
        requests,
        lambda reqs: [
            f'<?xml version="1.0" encoding="UTF-8" standalone="no"?>{lib.to_xml(req, name_="data")}'
            for req in reqs
        ],
    )
