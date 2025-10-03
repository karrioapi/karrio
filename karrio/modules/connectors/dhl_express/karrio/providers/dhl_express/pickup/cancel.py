import karrio.schemas.dhl_express.cancel_pickup_global_req_3_0 as dhl
import time
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.dhl_express.units as provider_units
import karrio.providers.dhl_express.error as provider_error
import karrio.providers.dhl_express.utils as provider_utils


def parse_pickup_cancel_response(
    _response: lib.Deserializable[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    successful = len(lib.find_element("ConfirmationNumber", response)) > 0
    cancellation = (
        models.ConfirmationDetails(
            carrier_name=settings.carrier_name,
            carrier_id=settings.carrier_id,
            success=successful,
            operation="Cancel Pickup",
        )
        if successful
        else None
    )

    return cancellation, provider_error.parse_error_response(response, settings)


def pickup_cancel_request(
    payload: models.PickupCancelRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    request = dhl.CancelPURequest(
        Request=settings.Request(
            MetaData=dhl.MetaData(SoftwareName="XMLPI", SoftwareVersion=1.0)
        ),
        schemaVersion=3.0,
        RegionCode=(
            provider_units.CountryRegion[payload.address.country_code].value
            if payload.address is not None and payload.address.country_code is not None
            else "AM"
        ),
        ConfirmationNumber=payload.confirmation_number,
        RequestorName=payload.address.person_name,
        CountryCode=payload.address.country_code,
        Reason="006",
        PickupDate=payload.pickup_date,
        CancelTime=time.strftime("%H:%M:%S"),
    )

    return lib.Serializable(
        request,
        lambda _: provider_utils.reformat_time(
            "CancelTime",
            lib.to_xml(
                _,
                name_="req:CancelPURequest",
                namespacedef_=(
                    'xmlns:req="http://www.dhl.com" '
                    'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
                    'xsi:schemaLocation="http://www.dhl.com cancel-pickup-global-req.xsd"'
                ),
            ).replace('schemaVersion="3"', 'schemaVersion="3.0"'),
        ),
    )
