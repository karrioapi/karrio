"""Karrio DPD France tracking (GetShipmentTrace)."""

import typing

import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.dpd_france.error as error
import karrio.providers.dpd_france.units as provider_units
import karrio.providers.dpd_france.utils as provider_utils
import karrio.schemas.dpd_france.webtraceservice as dpd_france


def parse_tracking_response(
    _response: lib.Deserializable[typing.List[typing.Tuple[str, lib.Element]]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    responses = _response.deserialize()

    messages: typing.List[models.Message] = sum(
        [
            error.parse_error_response(response, settings, tracking_number=tracking_number)
            for tracking_number, response in responses
        ],
        start=[],
    )

    details = [_extract_details(trace, settings) for _, response in responses for trace in _iter_traces(response)]

    return details, messages


def _iter_traces(response: lib.Element) -> typing.List[dpd_france.ShipmentTrace]:
    """Walk to ShipmentTrace nodes — cargoNET nests them under
    GetShipmentTrace*Result (single trace) or ArrayOfShipmentTrace (batch)."""
    nested = lib.find_element("ShipmentTrace", response, dpd_france.ShipmentTrace)
    if nested:
        return nested
    result = lib.find_element("GetShipmentTraceResult", response, first=True)
    return [lib.to_object(dpd_france.ShipmentTrace, result)] if result is not None else []


def _extract_details(
    trace: dpd_france.ShipmentTrace,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    events = (trace.Traces.clsTrace if trace.Traces is not None else None) or []
    last = events[-1] if events else None
    status = (
        provider_units.TrackingStatus.map(str(last.StatusNumber)).name
        if last is not None and last.StatusNumber is not None
        else None
    )

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=trace.ShipmentNumber,
        events=[
            models.TrackingEvent(
                date=lib.fdate(event.ScanDate),
                time=lib.flocaltime(event.ScanTime),
                code=str(event.StatusNumber) if event.StatusNumber is not None else None,
                description=event.StatusDescription,
                location=event.CenterName,
            )
            for event in events
        ],
        delivered=(status == "delivered"),
        status=status,
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    requests = [
        (
            tracking_number,
            lib.Envelope(
                Header=lib.Header(
                    dpd_france.UserCredentials(
                        userid=settings.userid,
                        password=settings.password,
                    )
                ),
                Body=lib.Body(
                    dpd_france.GetShipmentTrace(
                        request=dpd_france.ShipmentDetailRequest(
                            Customer=dpd_france.Customer(
                                countrycode=settings.customer_country_code,
                                centernumber=settings.customer_center_number,
                                number=settings.customer_number,
                            ),
                            Language=settings.language,
                            ShipmentNumber=tracking_number,
                        )
                    )
                ),
            ),
        )
        for tracking_number in payload.tracking_numbers
    ]

    return lib.Serializable(
        requests,
        lambda envs: [
            (
                num,
                lib.envelope_serializer(
                    env,
                    namespace=(
                        'xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" '
                        'xmlns:imt="http://www.cargonet.software/"'
                    ),
                    prefixes={
                        "Envelope": "soapenv",
                        "UserCredentials": "imt",
                        "GetShipmentTrace": "imt",
                    },
                ),
            )
            for num, env in envs
        ],
    )
