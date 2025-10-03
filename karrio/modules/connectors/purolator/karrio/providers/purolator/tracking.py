import karrio.schemas.purolator.tracking_service_1_2_2 as purolator
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.purolator.error as error
import karrio.providers.purolator.utils as provider_utils
import karrio.providers.purolator.units as provider_units


def parse_tracking_response(
    _response: lib.Deserializable[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    track_infos = lib.find_element("TrackingInformation", response)
    return (
        [_extract_details(node, settings) for node in track_infos],
        error.parse_error_response(response, settings),
    )


def _extract_details(
    node: lib.Element, settings: provider_utils.Settings
) -> models.TrackingDetails:
    track = lib.to_object(purolator.TrackingInformation, node)
    delivered = any(scan.ScanType == "Delivery" for scan in track.Scans.Scan)
    last_event = track.Scans.Scan[0]
    status = next(
        (
            status.name
            for status in list(provider_units.TrackingStatus)
            if getattr(last_event, "ScanType", None) in status.value
        ),
        provider_units.TrackingStatus.in_transit.name,
    )

    return models.TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=str(track.PIN.Value),
        status=status,
        delivered=delivered,
        events=[
            models.TrackingEvent(
                date=lib.fdate(scan.ScanDate),
                time=lib.flocaltime(scan.ScanTime, "%H%M%S"),
                description=scan.Description,
                location=scan.Depot.Name,
                code=scan.ScanType,
            )
            for scan in track.Scans.Scan
        ],
        info=models.TrackingInfo(
            carrier_tracking_link=settings.tracking_url.format(track.PIN.Value)
        ),
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    request = lib.Envelope(
        Header=lib.Header(
            purolator.RequestContext(
                Version="1.2",
                Language=settings.language,
                GroupID="",
                RequestReference="",
                UserToken=settings.user_token,
            ),
        ),
        Body=lib.Body(
            purolator.TrackPackagesByPinRequest(
                PINs=purolator.ArrayOfPIN(
                    PIN=[purolator.PIN(Value=pin) for pin in payload.tracking_numbers]
                )
            ),
        ),
    )

    return lib.Serializable(
        request,
        lambda envelope: lib.envelope_serializer(
            envelope,
            namespace=(
                'xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" '
                'xmlns:v1="http://purolator.com/pws/datatypes/v1"'
            ),
            prefixes=dict(
                Envelope="soap",
                RequestContext="v1",
                TrackPackagesByPinRequest="v1",
            ),
        ),
    )
