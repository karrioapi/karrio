"""Karrio GLS Group sporadic pickup scheduling implementation."""

import karrio.core.models as models
import karrio.lib as lib
import karrio.providers.gls.error as error
import karrio.providers.gls.units as provider_units
import karrio.providers.gls.utils as provider_utils
import karrio.schemas.gls.pickup_request as gls_request
import karrio.schemas.gls.pickup_response as gls_response


def parse_pickup_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> tuple[models.PickupDetails | None, list[models.Message]]:
    """Parse a SporadicCollectionResponse from POST /rs/sporadiccollection."""
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    pickup = _extract_details(response, settings) if not any(messages) and response.get("EstimatedPickUpDate") else None

    return pickup, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.PickupDetails:
    pickup = lib.to_object(gls_response.PickupResponseType, data)
    estimated = pickup.EstimatedPickUpDate
    pickup_date = lib.fdate(estimated, try_formats=["%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d"])

    return models.PickupDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        confirmation_number=estimated,
        pickup_date=pickup_date,
        meta=dict(estimated_pickup_date=estimated),
    )


def pickup_request(
    payload: models.PickupRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Build a SporadicCollection request body. ContactID identifies the
    pickup location at GLS — the address itself is registered against it."""
    options = lib.to_shipping_options(
        payload.options or {},
        initializer=provider_units.shipping_options_initializer,
    )
    packages = lib.to_packages(payload.parcels or [])
    ready_time = payload.ready_time or "09:00"

    request = gls_request.PickupRequestType(
        ContactID=settings.contact_id,
        PreferredPickUpDate=f"{payload.pickup_date}T{ready_time}:00Z",
        NumberOfParcels=len(packages) or None,
        Product=options.gls_pickup_product.state or "PARCEL",
        ExpectedTotalWeight=lib.failsafe(lambda: float(packages.weight.KG)),
        ContainsHazGoods=options.gls_contains_haz_goods.state,
        AdditionalInformation=payload.instruction,
    )

    return lib.Serializable(request, lib.to_dict)
