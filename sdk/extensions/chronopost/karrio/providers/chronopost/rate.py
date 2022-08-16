import chronopost_lib.quickcostservice as chronopost
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.chronopost.error as provider_error
import karrio.providers.chronopost.units as provider_units
import karrio.providers.chronopost.utils as provider_utils


def parse_rate_response(
    response: lib.Element, settings: provider_utils.Settings
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    product_nodes: typing.List[chronopost.service] = lib.find_element(
        "service", response, chronopost.service
    )
    products: typing.List[models.RateDetails] = [
        _extract_service_details(product_node, settings)
        for product_node in product_nodes
        if product_node.amount > 0.0
    ]
    return products, provider_error.parse_error_response(response, settings)


def _extract_service_details(
    detail: chronopost.service, settings: provider_utils.Settings
) -> models.RateDetails:
    service = provider_units.ShippingService.map(detail.codeService)

    charges = [("TVA", lib.to_decimal(detail.amountTVA))]

    return models.RateDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        currency="EUR",
        service=service.name_or_key,
        total_charge=lib.to_money(detail.amountTTC),
        extra_charges=[
            models.ChargeDetails(
                name=name,
                amount=lib.to_money(amount),
                currency="EUR",
            )
            for name, amount in charges
            if amount > 0.0
        ],
        meta=dict(service_name=detail.label or service.name_or_key),
    )


def rate_request(
    payload: models.RateRequest, settings: provider_utils.Settings
) -> lib.Serializable[lib.Envelope]:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    package = lib.to_packages(payload.parcels).single
    service = lib.to_services(payload.services, provider_units.ShippingService).first
    is_international = shipper.country_code != recipient.country_code
    product = (
        service
        if service is not None
        else (
            provider_units.ShippingService.chronopost_express_international
            if is_international
            else provider_units.ShippingService.chronopost_10
        )
    ).value

    request = lib.Envelope(
        Body=lib.Body(
            chronopost.quickCost(
                accountNumber=settings.account_number,
                password=settings.password,
                depCode=(
                    shipper.country_code if is_international else shipper.postal_code
                ),
                arrCode=(
                    recipient.country_code
                    if is_international
                    else recipient.postal_code
                ),
                weight=package.weight.KG,
                productCode=product,
            )
        )
    )

    return lib.Serializable(
        request,
        lambda envelope: lib.envelope_serializer(
            envelope,
            namespace=(
                'xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" '
                'xmlns:cxf="http://cxf.quickcost.soap.chronopost.fr/"'
            ),
            prefixes=dict(Envelope="soapenv"),
        ),
    )
