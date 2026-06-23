"""Hermes ParcelShop finder — backs the unified karrio.Location interface.

The PSF (ParcelShop Finder) Search API is a separate Hermes service from HSI,
authenticated with an `apiKey` header. See SPECS.md (ParcelShop finder).
"""

import karrio.core.models as models
import karrio.lib as lib
import karrio.providers.hermes.utils as provider_utils
import karrio.schemas.hermes.parcelshop as hermes_psf

# PSF typeID -> unified location_type (ParcelShop: 0, ByBox: 1).
LOCATION_TYPES = {0: "parcel_shop", 1: "locker"}


def parse_location_response(
    _response: lib.Deserializable,
    settings: provider_utils.Settings,
) -> tuple[list[models.LocationDetails], list[models.Message]]:
    """Parse a PSF search response into unified `LocationDetails`."""
    response = _response.deserialize()

    shops = response if isinstance(response, list) else []
    messages = [m for m in shops if isinstance(m, models.Message)]
    if messages:
        return [], messages

    locations = [
        _extract_details(lib.to_object(hermes_psf.ParcelshopType, shop), settings)
        for shop in shops
        if isinstance(shop, dict)
    ]

    return locations, []


def _extract_details(
    shop: hermes_psf.ParcelshopType,
    settings: provider_utils.Settings,
) -> models.LocationDetails:
    """Map a PSF `ParcelshopType` node to a unified `LocationDetails`."""
    return models.LocationDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        location_id=shop.parcelShopNumber,
        location_type=LOCATION_TYPES.get(shop.typeID, "parcel_shop"),
        name=shop.name or shop.description,
        address=models.Address(
            address_line1=lib.join(shop.street, shop.houseNumber, join=True),
            city=shop.city,
            postal_code=shop.zip,
            country_code=shop.countryIsoA2Code,
            phone_number=shop.phone,
        ),
        latitude=shop.latitude,
        longitude=shop.longitude,
        distance=shop.distance,
        opening_hours=[lib.to_dict(hour) for hour in (shop.hours or [])],
    )


def location_request(
    payload: models.LocationRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Build a PSF search query, picking the endpoint from the inputs.

    by coordinates -> findParcelShopByLocation; by structured address ->
    findParcelShopByAddress; otherwise -> findParcelShopByAddressString.
    """
    address = lib.to_address(payload.address)
    options = payload.options or {}
    lat = options.get("latitude") or options.get("lat")
    lng = options.get("longitude") or options.get("lng")

    query = dict(
        country=(address.country_code or "DE").upper(),
        maxDist=payload.radius_km,
        maxResult=payload.max_results,
        typeId=options.get("type_id"),
        openNow=options.get("open_now"),
    )

    if lat and lng:
        endpoint = "findParcelShopByLocation"
        query.update(lat=lat, lng=lng)
    elif address.city and address.postal_code and address.street_name:
        endpoint = "findParcelShopByAddress"
        query.update(
            city=address.city,
            zipCode=address.postal_code,
            street=address.street_name,
            houseNumber=address.street_number,
        )
    else:
        endpoint = "findParcelShopByAddressString"
        query.update(
            adressSearchString=lib.join(
                address.address_line1, address.postal_code, address.city, join=True, separator=" "
            )
        )

    return lib.Serializable(query, lib.to_dict, dict(endpoint=endpoint))
