"""DPD Meta location finder — backs the unified `karrio.Location` interface.

DPD's location surface is the DepotDataService SOAP API: it resolves the
depot that serves a country + postal code. Mirroring the dpd (classic)
connector, the request envelope is built here with an `[AUTH_TOKEN]`
placeholder that the proxy swaps for the public-WS token once authenticated.

References:
  vendor/LoginService_V2_0_C0.pdf
  vendor/DepotDataService_V1_0.pdf
"""

import karrio.core.models as models
import karrio.lib as lib
import karrio.providers.dpd_meta.error as error
import karrio.providers.dpd_meta.utils as provider_utils
import karrio.schemas.dpd_meta.webapi as webapi


def parse_location_response(
    _response: lib.Deserializable,
    settings: provider_utils.Settings,
) -> tuple[list[models.LocationDetails], list[models.Message]]:
    """Parse a DepotDataService response into unified `LocationDetails`."""
    response = _response.deserialize()

    # The proxy short-circuits to a list of Messages when the public-WS
    # login fails — only a SOAP XML string is parseable as depot data.
    if not isinstance(response, str):
        return [], [m for m in (response or []) if isinstance(m, models.Message)]

    element = lib.to_element(response)
    messages = error.parse_soap_faults(element, settings)
    depot = lib.find_element("DepotData", element, webapi.DepotData, first=True)
    locations = [_extract_details(depot, settings)] if (depot is not None and depot.depot) else []

    return locations, messages


def _extract_details(
    depot: webapi.DepotData,
    settings: provider_utils.Settings,
) -> models.LocationDetails:
    """Map a DPD `DepotData` node to a unified `LocationDetails`."""
    return models.LocationDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        location_id=depot.depot,
        location_type="depot",
        name=depot.name,
        address=models.Address(
            address_line1=depot.street,
            city=depot.city,
            postal_code=depot.zipCode,
            country_code=depot.country,
            phone_number=depot.phone,
            email=depot.email,
        ),
    )


def location_request(
    payload: models.LocationRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Build the DepotDataService `getDepotData` SOAP request.

    The `<authentication>` header carries an `[AUTH_TOKEN]` placeholder the
    proxy substitutes with the public-WS token. `ctx` carries the country +
    postal code so the proxy can key the 24h depot cache without re-parsing
    the envelope.
    """
    address = lib.to_address(payload.address)
    country = (address.country_code or "").upper()
    zip_code = address.postal_code or None

    envelope = lib.create_envelope(
        envelope_prefix="soapenv",
        header_prefix="ns",
        body_prefix="ns1",
        header_content=webapi.Authentication(
            delisId=settings.dpd_login,
            authToken="[AUTH_TOKEN]",
            messageLanguage="en_US",
        ),
        header_tag_name="authentication",
        body_content=webapi.getDepotData(
            country=country,
            zipCode=zip_code,
            depot=(payload.options or {}).get("depot"),
        ),
    )

    return lib.Serializable(
        envelope,
        # DPD WSDLs are elementFormDefault="unqualified": operation elements
        # carry the service namespace prefix, their child fields do not.
        lambda env: lib.envelope_serializer(
            env,
            namespace=(
                'xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" '
                'xmlns:ns="http://dpd.com/common/service/types/Authentication/2.0" '
                'xmlns:ns1="http://dpd.com/common/service/types/DepotDataService/1.0"'
            ),
            prefixes=dict(
                Envelope="soapenv",
                Authentication="ns",
                getDepotData="ns1",
                delisId="",
                authToken="",
                messageLanguage="",
                country="",
                zipCode="",
                depot="",
            ),
        ),
        dict(country=country, zip_code=zip_code),
    )
