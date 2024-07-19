import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.chronopost.utils as provider_utils
import karrio.providers.chronopost.error as provider_error
import karrio.schemas.chronopost.trackingservice as chronopost


def parse_tracking_response(
    _responses: lib.Deserializable[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    responses = _responses.deserialize()
    tracking_nodes: typing.List[chronopost.listEventInfoComps] = lib.find_element(
        "listEventInfoComp", responses, chronopost.listEventInfoComps
    )
    errors = provider_error.parse_error_response(responses, settings)
    tracking_details: typing.List[models.TrackingDetails] = [
        _extract_details(tracking_node, settings) for tracking_node in tracking_nodes
    ]
    return tracking_details, errors


def _extract_details(
    detail: chronopost.listEventInfoComps,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    delivery: chronopost.eventInfoComp = next(
        (event for event in detail.events if event.code == "D"), None
    )

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=detail.skybillNumber,
        events=[
            models.TrackingEvent(
                date=lib.fdate(event.eventDate, "%Y-%m%dT%H%:%M:%S"),
                description=event.eventLabel,
                code=event.code,
                time=lib.flocaltime(event.eventDate, "%Y-%m%dT%H%:%M:%S"),
                location=event.officeLabel,
            )
            for event in detail.events
        ],
        delivered=(delivery is not None),
        info=models.TrackingInfo(
            carrier_tracking_link=settings.tracking_url.format(detail.skybillNumber),
            customer_name=(
                getattr(delivery.infoCompList, "name", None) if delivery else None
            ),
            shipment_destination_postal_code=getattr(delivery, "zipCode", None),
        ),
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    request = [
        lib.Envelope(
            Body=lib.Body(
                chronopost.trackSkybillV2(
                    language=settings.language, skybillNumber=tracking_number
                )
            ),
        )
        for tracking_number in payload.tracking_numbers
    ]

    return lib.Serializable(
        request,
        lambda requests: [
            lib.envelope_serializer(
                req,
                namespace=(
                    'xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" '
                    'xmlns:cxf="http://cxf.tracking.soap.chronopost.fr/"'
                ),
                prefixes=dict(Envelope="soapenv"),
            )
            for req in requests
        ],
    )
