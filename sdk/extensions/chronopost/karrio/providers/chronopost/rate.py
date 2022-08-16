from chronopost_lib.quickcostservice import(
    calculateProducts,
    calculateProductsResponse,
    product,
)
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.chronopost.error as provider_error
import karrio.providers.chronopost.units as provider_units
import karrio.providers.chronopost.utils as provider_utils



def parse_rate_response(
    response: lib.Element, settings: provider_utils.Settings
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    product_nodes = lib.find_element("productList", response, calculateProductsResponse)
    products: typing.List[models.RateDetails] = [
        _extract_service_details(product_node, settings) for product_node in product_nodes
    ]
    return products, provider_error.parse_error_response(response, settings)
    

def _extract_service_details(
    node: lib.Element, settings: provider_utils.Settings
) -> models.RateDetails:
    shipment = lib.to_object(product, node)
    service = provider_units.Service.map(shipment.productCode)

    tax = lib.to_decimal(shipment.amountTVA) if lib.to_decimal(shipment.amountTVA) > 0.0 else None

    return models.RateDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        currency="EUR",
        service=service.name_or_key,
        total_charge=lib.to_money(shipment.amountTTC or 0),
        extra_charges=tax,
        meta=dict(service_name=(service.name or shipment.productCode)),
    )

def rate_request(
    payload: models.RateRequest, settings: provider_utils.Settings
) -> lib.Serializable[lib.Envelope]:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)

    request = lib.create_envelope(
        body_content=calculateProducts(
            accountNumber=settings.account_number,
            password=settings.password,
            depCountryCode=shipper.country_code,
            depZipCode=shipper.postal_code,
            arrCountryCode=recipient.country_code,
            arrZipCode=recipient.postal_code,
            arrCity=recipient.city,
            type="M",
            weight="1",

        )
    )
    return lib.Serializable(
        request,
        lambda req: settings.serialize(req, "calculateProdcuts", settings.server_url),
    )


