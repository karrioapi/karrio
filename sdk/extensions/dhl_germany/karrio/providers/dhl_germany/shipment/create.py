
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.dhl_germany.error as error
import karrio.providers.dhl_germany.utils as provider_utils
import karrio.providers.dhl_germany.units as provider_units


def parse_shipment_response(
    response: lib.Element,
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response_messages = []  # extract carrier response errors
    response_shipment = None  # extract carrier response shipment

    messages = error.parse_error_response(response_messages, settings)
    shipment = _extract_details(response_shipment, settings)

    return shipment, messages


def _extract_details(
    data: lib.Element,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    shipment = None  # parse carrier shipment type from "data"
    label = ""  # extract and process the shipment label to a valid base64 text
    # invoice = ""  # extract and process the shipment invoice to a valid base64 text if applies

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number="",  # extract tracking number from shipment
        shipment_identifier="",  # extract shipment identifier from shipment
        label_type="PDF",  # extract shipment label file format
        docs=models.Documents(
            label=label,  # pass label base64 text
            # invoice=invoice,  # pass invoice base64 text if applies
        ),
        meta=dict(
            # any relevent meta
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    packages = units.Packages(payload.parcels)  # preprocess the request parcels
    options = units.Options(payload.options, provider_units.ShippingOption)  # preprocess the request options
    services = units.Services(payload.services, provider_units.ShippingService)  # preprocess the request services

    request = None  # map data to convert karrio model to dhl_germany specific type

    return lib.Serializable(request)
