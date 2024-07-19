import karrio.schemas.canpar.CanparAddonsService as canpar
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.canpar.error as error
import karrio.providers.canpar.utils as provider_utils


def parse_tracking_response(
    _response: lib.Deserializable[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    results = lib.find_element("result", response)
    details: typing.List[models.TrackingDetails] = [
        _extract_tracking_details(result, settings) for result in results
    ]

    return details, error.parse_error_response(response, settings)


def _extract_tracking_details(
    node: lib.Element,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    is_en = settings.language == "en"
    result = lib.to_object(canpar.TrackingResult, node)
    estimated_delivery = lib.fdate(result.estimated_delivery_date, "%Y%m%d")
    events = [
        models.TrackingEvent(
            date=lib.fdate(event.local_date_time, "%Y%m%d %H%M%S"),
            description=(
                event.code_description_en if is_en else event.code_description_fr
            ),
            location=lib.join(
                event.address.address_line_1,
                event.address.address_line_2,
                event.address.city,
                event.address.province,
                event.address.country,
                join=True,
                separator=", ",
            ),
            code=event.code,
            time=lib.flocaltime(event.local_date_time, "%Y%m%d %H%M%S"),
        )
        for event in typing.cast(typing.List[canpar.TrackingEvent], result.events)
    ]
    delivered = any(event.code == "DEL" for event in events)

    return models.TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=result.barcode,
        estimated_delivery=estimated_delivery,
        delivered=delivered,
        events=events,
        info=models.TrackingInfo(
            shipment_destination_country=result.consignee_address.country,
            shipment_destination_postal_code=result.consignee_address.postal_code,
            shipping_date=lib.fdate(result.shipping_date, current_format="%Y%m%d"),
            carrier_tracking_link=(
                result.tracking_url_en if is_en else result.tracking_url_fr
            ),
            shipment_service=(
                result.service_description_en
                if is_en
                else result.service_description_fr
            ),
            signed_by=result.signed_by,
        ),
    )


def tracking_request(payload: models.TrackingRequest, _) -> lib.Serializable:
    request = [
        lib.create_envelope(
            body_content=canpar.trackByBarcodeV2(
                request=canpar.TrackByBarcodeV2Rq(
                    barcode=barcode, filter=None, track_shipment=True
                )
            )
        )
        for barcode in payload.tracking_numbers
    ]

    return lib.Serializable(request, _request_serializer)


def _request_serializer(envelopes: typing.List[lib.Envelope]) -> typing.List[str]:
    return [provider_utils.Settings.serialize(envelope) for envelope in envelopes]
