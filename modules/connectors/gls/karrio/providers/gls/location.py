"""GLS ParcelShop finder — backs the unified `karrio.Location` interface. See SPECS.md."""

import karrio.core.models as models
import karrio.lib as lib
import karrio.providers.gls.error as error
import karrio.providers.gls.units as provider_units
import karrio.providers.gls.utils as provider_utils


def parse_location_response(
    _response: lib.Deserializable,
    settings: provider_utils.Settings,
) -> tuple[list[models.LocationDetails], list[models.Message]]:
    """Parse a ParcelShop finder response into unified `LocationDetails`."""
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    if any(messages):
        return [], messages

    shops = provider_utils.extract_parcel_shops(response)
    locations = [_extract_details(shop, settings) for shop in shops]

    return locations, messages


def _extract_details(
    shop: dict,
    settings: provider_utils.Settings,
) -> models.LocationDetails:
    """Map a single GLS ParcelShop dict to a unified `LocationDetails`."""
    address = shop.get("Address") or {}
    location = shop.get("Location") or {}
    airline = shop.get("AirlineDistance")

    return models.LocationDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        location_id=shop.get("ParcelShopID"),
        location_type=(shop.get("Type") or "parcel_shop").lower(),
        name=address.get("Name1"),
        address=models.Address(
            address_line1=lib.text(address.get("Street"), address.get("StreetNumber"), separator=" "),
            city=address.get("City"),
            postal_code=address.get("ZIPCode"),
            country_code=address.get("CountryCode"),
        ),
        latitude=lib.failsafe(lambda: float(location.get("Latitude"))),
        longitude=lib.failsafe(lambda: float(location.get("Longitude"))),
        distance=lib.failsafe(lambda: float(airline)) if airline is not None else None,
        opening_hours=provider_utils.normalize_opening_hours(shop.get("WorkingDay")),
        meta=dict(raw=shop),
    )


def location_request(
    payload: models.LocationRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Build a ParcelShop finder request. See SPECS.md."""
    config = settings.connection_config
    options = payload.options or {}
    address = lib.to_address(payload.address)

    shop_id = options.get("parcel_shop_id") or options.get("ParcelShopID")
    country = (address.country_code or options.get("country") or "").upper() or None
    latitude = options.get("latitude")
    longitude = options.get("longitude")
    parcel_shop_type = (
        options.get("parcel_shop_type")
        or provider_units.LOCATION_TYPE_TO_PARCEL_SHOP_TYPE.get(payload.location_type or "")
        or config.parcel_shop_default_type.state
    )
    max_results = payload.max_results or options.get("max_results") or config.parcel_shop_default_max_results.state
    distance = payload.radius_km or options.get("distance") or config.parcel_shop_default_radius.state

    base = f"{settings.shipment_api_url}/rs/parcelshop"

    if shop_id:
        method, url, body = "GET", f"{base}/{shop_id}", None
    elif latitude is not None and longitude is not None:
        method, url = "POST", f"{base}/distance"
        body = dict(
            Latitude=str(latitude),
            Longitude=str(longitude),
            Distance=str(int(distance)) if distance else None,
            MaxNumberOfShops=str(int(max_results)) if max_results else None,
            ParcelShopType=parcel_shop_type,
        )
    elif address.address_line1 or address.postal_code or address.city:
        method, url = "POST", f"{base}/address"
        body = dict(
            Street=address.address_line1,
            StreetNumber=address.address_line2,
            CountryCode=country,
            ZIPCode=address.postal_code,
            City=address.city,
            Distance=str(int(distance)) if distance else None,
            MaxNumberOfShops=str(int(max_results)) if max_results else None,
            ParcelShopType=parcel_shop_type,
        )
    else:
        method, url, body = "GET", f"{base}/country/{country or 'DE'}", None

    return lib.Serializable(
        body or {},
        lib.to_dict,
        dict(method=method, url=url, has_body=body is not None),
    )
