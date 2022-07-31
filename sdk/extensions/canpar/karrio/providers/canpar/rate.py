import time
from functools import partial
from canpar_lib.CanparRatingService import (
    rateShipment,
    RateShipmentRq,
    Shipment,
    Package,
    Address,
)
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.canpar.error as provider_error
import karrio.providers.canpar.units as provider_units
import karrio.providers.canpar.utils as provider_utils


def parse_rate_response(
    response: lib.Element, settings: provider_utils.Settings
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    shipment_nodes = lib.find_element("shipment", response)
    rates: typing.List[models.RateDetails] = [
        _extract_rate_details(node, settings) for node in shipment_nodes
    ]
    return rates, provider_error.parse_error_response(response, settings)


def _extract_rate_details(
    node: lib.Element, settings: provider_utils.Settings
) -> models.RateDetails:
    shipment = lib.to_object(Shipment, node)
    service = provider_units.Service.map(shipment.service_type)

    surcharges = [
        models.ChargeDetails(
            name=charge.value,
            amount=lib.to_decimal(getattr(shipment, charge.name)),
            currency="CAD",
        )
        for charge in list(provider_units.Charges)
        if lib.to_decimal(getattr(shipment, charge.name)) > 0.0
    ]
    taxes = [
        models.ChargeDetails(
            name=f"{getattr(shipment, code, '')} Tax Charge",
            amount=lib.to_decimal(charge),
            currency="CAD",
        )
        for code, charge in [
            ("tax_code_1", shipment.tax_charge_1),
            ("tax_code_2", shipment.tax_charge_2),
        ]
        if lib.to_decimal(charge) > 0.0
    ]

    return models.RateDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        currency="CAD",
        transit_days=shipment.transit_time,
        service=service.name_or_key,
        total_charge=sum([c.amount for c in (surcharges + taxes)], 0.0),
        extra_charges=(surcharges + taxes),
        meta=dict(service_name=(service.name or shipment.service_type)),
    )


def rate_request(
    payload: models.RateRequest, settings: provider_utils.Settings
) -> lib.Serializable[lib.Envelope]:
    packages = lib.to_packages(payload.parcels)
    service_type = lib.to_services(payload.services, provider_units.Service).first
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    shipment_date = lib.fdatetime(
        options.shipment_date.state or time.strftime("%Y-%m-%d"),
        current_format="%Y-%m-%d",
        output_format="%Y-%m-%dT%H:%M:%S",
    )

    request = lib.create_envelope(
        body_content=rateShipment(
            request=RateShipmentRq(
                apply_association_discount=False,
                apply_individual_discount=False,
                apply_invoice_discount=False,
                password=settings.password,
                shipment=Shipment(
                    cod_type=options.canpar_cash_on_delivery.state,
                    delivery_address=Address(
                        address_line_1=payload.recipient.address_line1,
                        address_line_2=payload.recipient.address_line2,
                        address_line_3=None,
                        attention=payload.recipient.person_name,
                        city=payload.recipient.city,
                        country=payload.recipient.country_code,
                        email=payload.recipient.email,
                        extension=None,
                        name=payload.recipient.company_name,
                        phone=payload.recipient.phone_number,
                        postal_code=payload.recipient.postal_code,
                        province=payload.recipient.state_code,
                        residential=payload.recipient.residential,
                    ),
                    description=None,
                    dg=options.canpar_dangerous_goods.state,
                    dimention_unit=provider_units.DimensionUnit.IN.value,
                    handling=None,
                    handling_type=None,
                    instruction=None,
                    nsr=provider_units.ShippingOption.is_nsr(options),
                    packages=[
                        Package(
                            alternative_reference=None,
                            cod=None,
                            cost_centre=None,
                            declared_value=None,
                            height=pkg.height.CM,
                            length=pkg.length.CM,
                            lg=None,
                            reference=None,
                            reported_weight=pkg.weight.LB,
                            store_num=None,
                            width=pkg.width.CM,
                            xc=options.canpar_extra_care.state,
                        )
                        for pkg in packages
                    ],
                    pickup_address=Address(
                        address_line_1=payload.shipper.address_line1,
                        address_line_2=payload.shipper.address_line2,
                        address_line_3=None,
                        attention=payload.shipper.person_name,
                        city=payload.shipper.city,
                        country=payload.shipper.country_code,
                        email=payload.shipper.email,
                        extension=None,
                        name=payload.shipper.company_name,
                        phone=payload.shipper.phone_number,
                        postal_code=payload.shipper.postal_code,
                        province=payload.shipper.state_code,
                        residential=payload.shipper.residential,
                    ),
                    premium=provider_units.ShippingOption.is_premium(options),
                    proforma=None,
                    reported_weight_unit=provider_units.WeightUnit.LB.value,
                    send_email_to_delivery=payload.recipient.email,
                    send_email_to_pickup=payload.shipper.email,
                    service_type=service_type.value,
                    shipper_num=None,
                    shipping_date=shipment_date,
                    subtotal=None,
                    subtotal_with_handling=None,
                    total=None,
                    total_with_handling=None,
                    user_id=None,
                ),
                user_id=settings.username,
            )
        )
    )

    return lib.Serializable(
        request,
        partial(
            settings.serialize,
            extra_namespace='xmlns:xsd1="http://dto.canshipws.canpar.com/xsd"',
            special_prefixes=dict(shipment_children="xsd1"),
        ),
    )
