import time
from functools import partial
from canpar_lib.CanshipBusinessService import (
    Address,
    Package,
    Shipment,
    processShipment,
    ProcessShipmentRq,
)
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.canpar.error as provider_error
import karrio.providers.canpar.units as provider_units
import karrio.providers.canpar.utils as provider_utils
import karrio.providers.canpar.shipment.label as label
import karrio.providers.canpar.rate as rate


def parse_shipment_response(
    response: lib.Element, settings: provider_utils.Settings
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    shipment = lib.to_object(
        Shipment,
        next(iter(response.xpath(".//*[local-name() = $name]", name="shipment")), None),
    )
    success = shipment is not None and shipment.id is not None
    shipment_details = _extract_details(response, settings) if success else None

    return shipment_details, provider_error.parse_error_response(response, settings)


def _extract_details(
    response: lib.Element, settings: provider_utils.Settings
) -> models.ShipmentDetails:
    shipment_node = next(
        iter(response.xpath(".//*[local-name() = $name]", name="shipment")), None
    )
    label = next(
        iter(response.xpath(".//*[local-name() = $name]", name="labels")), None
    )
    shipment = lib.to_object(Shipment, shipment_node)
    tracking_number = next(iter(shipment.packages), Package()).barcode

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        shipment_identifier=str(shipment.id),
        selected_rate=rate._extract_rate_details(shipment_node, settings),
        docs=models.Documents(label=str(label.text)),
    )


def shipment_request(
    payload: models.ShipmentRequest, settings: provider_utils.Settings
) -> lib.Serializable[lib.Pipeline]:

    request: lib.Pipeline = lib.Pipeline(
        process=lambda *_: _process_shipment(payload, settings),
        get_label=partial(_get_label, settings=settings),
    )

    return lib.Serializable(request)


def _process_shipment(
    payload: models.ShipmentRequest, settings: provider_utils.Settings
) -> lib.Job:
    service_type = provider_units.Service.map(payload.service).value_or_key
    packages = lib.to_packages(payload.parcels)
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    shipping_date = lib.fdatetime(
        options.shipment_date.state or time.strftime("%Y-%m-%d"),
        current_format="%Y-%m-%d",
        output_format="%Y-%m-%dT%H:%M:%S",
    )

    request = lib.create_envelope(
        body_content=processShipment(
            request=ProcessShipmentRq(
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
                    nsr=(
                        options.canpar_no_signature_required.state
                        or options.canpar_not_no_signature_required.state
                    ),
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
                            xc=("canpar_extra_care" in options) or None,
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
                    service_type=service_type,
                    shipper_num=None,
                    shipping_date=shipping_date,
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

    data = lib.Serializable(
        request,
        partial(
            settings.serialize,
            extra_namespace='xmlns:xsd1="http://dto.canshipws.canpar.com/xsd"',
            special_prefixes=dict(shipment_children="xsd1"),
        ),
    )
    return lib.Job(id="process", data=data)


def _get_label(shipment_response: str, settings: provider_utils.Settings) -> lib.Job:
    response = lib.to_element(shipment_response)
    shipment = lib.to_object(
        Shipment,
        next(iter(response.xpath(".//*[local-name() = $name]", name="shipment")), None),
    )
    success = shipment is not None and shipment.id is not None
    data = (
        label.get_label_request(label.LabelRequest(shipment_id=shipment.id), settings)
        if success
        else None
    )

    return lib.Job(id="get_label", data=data, fallback=("" if not success else None))
