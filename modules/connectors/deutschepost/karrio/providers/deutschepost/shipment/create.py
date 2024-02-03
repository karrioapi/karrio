import karrio.schemas.deutschepost.shipping_request as deutschepost
import karrio.schemas.deutschepost.shipping_response as shipping
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.deutschepost.error as error
import karrio.providers.deutschepost.utils as provider_utils
import karrio.providers.deutschepost.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    shipment = _extract_details(response, settings)

    return shipment, messages


def _extract_details(
    data: dict,
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
    packages = lib.to_packages(payload.parcels)
    service = provider_units.ShippingService.map(payload.service).value_or_key
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        option_type=provider_units.ShippingOption,
    )

    request = deutschepost.ShippingRequestType(
        profile=None,
        shipments=[
            deutschepost.ShipmentType(
                product=None,
                billingNumber=None,
                refNo=None,
                shipper=deutschepost.ConsigneeType(),
                consignee=None,
                details=None,
                customs=None,
                services=None,
            )
        ],
    )

    return lib.Serializable(request)
