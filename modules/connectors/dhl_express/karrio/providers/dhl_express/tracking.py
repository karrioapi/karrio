import karrio.schemas.dhl_express.tracking_request_known_1_0 as tracking
import karrio.schemas.dhl_express.tracking_response as dhl
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.dhl_express.error as error
import karrio.providers.dhl_express.utils as provider_utils
import karrio.providers.dhl_express.units as provider_units


def parse_tracking_response(
    _response: lib.Deserializable[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    nodes = lib.find_element("AWBInfo", response)

    tracking_details = [
        _extract_tracking(node, settings)
        for node in nodes
        if len(lib.find_element("ShipmentInfo", node)) > 0
    ]
    return (
        tracking_details,
        error.parse_error_response(response, settings),
    )


def _extract_tracking(
    details: lib.Element,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    tracking_number = details.findtext("AWBNumber")
    info: lib.Element = lib.find_element("ShipmentInfo", details, first=True)
    estimated_delivery = lib.fdate(
        info.findtext("EstDlvyDate"), "%Y-%m-%d %H:%M:%S %Z%z"
    )
    events: typing.List[dhl.ShipmentEvent] = lib.find_element(
        "ShipmentEvent", info, dhl.ShipmentEvent
    )
    delivered = any(e.ServiceEvent.EventCode == "OK" for e in events)
    status = next(
        (
            status.name
            for status in list(provider_units.TrackingStatus)
            if events[-1].ServiceEvent.EventCode in status.value
        ),
        provider_units.TrackingStatus.in_transit.name,
    )

    return models.TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=tracking_number,
        status=status,
        events=[
            models.TrackingEvent(
                date=lib.fdate(e.Date),
                time=lib.flocaltime(e.Time),
                code=e.ServiceEvent.EventCode,
                location=e.ServiceArea.Description,
                description=lib.text(e.ServiceEvent.Description, e.Signatory),
            )
            for e in reversed(events)
        ],
        estimated_delivery=estimated_delivery,
        delivered=delivered,
        info=models.TrackingInfo(
            customer_name=lib.text(info.findtext("Consignee")),
            carrier_tracking_link=settings.tracking_url.format(tracking_number),
            shipping_date=lib.fdate(info.findtext("ShipmentDate"), "%Y-%m-%dT%H:%M:%S"),
            package_weight=lib.to_decimal(info.findtext("Weight")),
            package_weight_unit=provider_units.WeightUnit.map(
                info.findtext("WeightUnit")
            ).name_or_key,
        ),
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    options = lib.units.Options(payload.options or {})

    request = tracking.KnownTrackingRequest(
        Request=settings.Request(),
        LanguageCode=options.language_code.state or "en",
        LevelOfDetails=options.level_of_details.state or "ALL_CHECK_POINTS",
        AWBNumber=payload.tracking_numbers,
    )

    return lib.Serializable(request, _request_serializer)


def _request_serializer(request: tracking.KnownTrackingRequest) -> str:
    return lib.to_xml(
        request,
        name_="req:KnownTrackingRequest",
        namespacedef_=(
            'xmlns:req="http://www.dhl.com" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'xsi:schemaLocation="http://www.dhl.com TrackingRequestKnown.xsd"'
        ),
    ).replace('schemaVersion="1"', 'schemaVersion="1.0"')
