import karrio.schemas.fedex_ws.track_service_v19 as fedex
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.fedex_ws.error as provider_error
import karrio.providers.fedex_ws.utils as provider_utils
import karrio.providers.fedex_ws.units as provider_units

estimated_date_formats = [
    "%Y-%m-%dT%H:%M:%S%z",
    "%Y-%m-%dT%H:%M:%S",
]


def parse_tracking_response(
    _response: lib.Deserializable[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    tracking_details = [
        _extract_tracking(track_detail_node, settings)
        for track_detail_node in lib.find_element("TrackDetails", response)
    ]
    return (
        [details for details in tracking_details if details is not None],
        provider_error.parse_error_response(response, settings),
    )


def _extract_tracking(
    detail_node: lib.Element,
    settings: provider_utils.Settings,
) -> typing.Optional[models.TrackingDetails]:
    track_detail = lib.to_object(fedex.TrackDetail, detail_node)

    if track_detail.Notification.Severity == "ERROR":
        return None

    date_or_timestamps = lib.find_element(
        "DatesOrTimes", detail_node, fedex.TrackingDateOrTimestamp
    )
    estimated_delivery = (
        _parse_date_or_timestamp(date_or_timestamps, "ACTUAL_DELIVERY")
        or _parse_date_or_timestamp(date_or_timestamps, "ACTUAL_TENDER")
        or _parse_date_or_timestamp(date_or_timestamps, "ANTICIPATED_TENDER")
        or _parse_date_or_timestamp(date_or_timestamps, "ESTIMATED_DELIVERY")
    )
    last_event = (
        track_detail.Events[0].EventType
        if any(track_detail.Events)
        else getattr(track_detail.StatusDetail, "Code", "")
    )
    status = next(
        (
            status.name
            for status in list(provider_units.TrackingStatus)
            if last_event in status.value
        ),
        provider_units.TrackingStatus.in_transit.name,
    )

    return models.TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=track_detail.TrackingNumber,
        status=status,
        events=[
            models.TrackingEvent(
                date=lib.fdate(e.Timestamp, "%Y-%m-%d %H:%M:%S%z"),
                time=lib.ftime(e.Timestamp, "%Y-%m-%d %H:%M:%S%z"),
                code=e.EventType,
                location=(
                    lib.join(
                        e.Address.City,
                        e.Address.StateOrProvinceCode,
                        e.Address.PostalCode,
                        e.Address.CountryCode,
                        join=True,
                        separator=", ",
                    )
                    if e.Address and any(e.Address.City or "")
                    else e.ArrivalLocation
                ),
                description=e.EventDescription,
            )
            for e in track_detail.Events
        ],
        estimated_delivery=estimated_delivery,
        delivered=any(e.EventType == "DL" for e in track_detail.Events),
        info=models.TrackingInfo(
            carrier_tracking_link=settings.tracking_url.format(
                track_detail.TrackingNumber
            ),
            shipment_service=getattr(track_detail.Service, "Description", None),
            package_weight_unit=getattr(track_detail.PackageWeight, "Units", None),
            package_weight=lib.to_decimal(
                getattr(track_detail.PackageWeight, "Value", None)
            ),
            shipment_destination_country=getattr(
                track_detail.ShipperAddress, "CountryCode", None
            ),
            shipment_origin_country=getattr(
                track_detail.DestinationAddress, "CountryCode", None
            ),
        ),
    )


def _parse_date_or_timestamp(
    date_or_timestamps: typing.List[fedex.TrackingDateOrTimestamp], type: str
) -> typing.Optional[str]:
    return next(
        iter(
            [
                lib.fdate(d.DateOrTimestamp, try_formats=estimated_date_formats)
                for d in date_or_timestamps
                if d.Type == type
            ]
        ),
        None,
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    options = lib.units.Options(payload.options or {})

    request = fedex.TrackRequest(
        WebAuthenticationDetail=settings.webAuthenticationDetail,
        ClientDetail=settings.clientDetail,
        TransactionDetail=fedex.TransactionDetail(
            CustomerTransactionId="Track By Number_v18",
            Localization=fedex.Localization(
                LanguageCode=options.language_code.state or "en"
            ),
        ),
        Version=fedex.VersionId(ServiceId="trck", Major=18, Intermediate=0, Minor=0),
        SelectionDetails=[
            fedex.TrackSelectionDetail(
                CarrierCode="FDXE",  # Read doc for carrier code customization
                OperatingCompany=None,
                PackageIdentifier=fedex.TrackPackageIdentifier(
                    Type="TRACKING_NUMBER_OR_DOORTAG", Value=tracking_number
                ),
                TrackingNumberUniqueIdentifier=None,
                ShipDateRangeBegin=None,
                ShipDateRangeEnd=None,
                ShipmentAccountNumber=None,
                SecureSpodAccount=None,
                Destination=None,
                PagingDetail=None,
                CustomerSpecifiedTimeOutValueInMilliseconds=None,
            )
            for tracking_number in payload.tracking_numbers
        ],
        TransactionTimeOutValueInMilliseconds=None,
        ProcessingOptions=["INCLUDE_DETAILED_SCANS"],
    )
    return lib.Serializable(request, _request_serializer)


def _request_serializer(request: fedex.TrackRequest) -> str:
    namespacedef_ = (
        'xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" '
        'xmlns:v18="http://fedex.com/ws/track/v18"'
    )

    envelope = lib.create_envelope(body_content=request)
    envelope.Body.ns_prefix_ = envelope.ns_prefix_
    lib.apply_namespaceprefix(envelope.Body.anytypeobjs_[0], "v18")

    return lib.to_xml(envelope, namespacedef_=namespacedef_)
