import time
from functools import partial
from karrio.schemas.canpar.CanshipBusinessService import (
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
    _response: lib.Deserializable[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    shipment = lib.to_object(
        Shipment,
        lib.find_element("shipment", response, first=True),
    )
    success = shipment is not None and shipment.id is not None
    shipment_details = _extract_details(response, settings) if success else None

    return shipment_details, provider_error.parse_error_response(response, settings)


def _extract_details(
    response: lib.Element, settings: provider_utils.Settings
) -> models.ShipmentDetails:
    shipment_node = lib.find_element("shipment", response, first=True)
    label = lib.find_element("labels", response, first=True)
    shipment = lib.to_object(Shipment, shipment_node)
    tracking_number = next(iter(shipment.packages), Package()).barcode

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        shipment_identifier=str(shipment.id),
        selected_rate=rate._extract_rate_details(shipment_node, settings),
        docs=models.Documents(label=str(label.text)),
        meta=dict(
            carrier_tracking_link=settings.tracking_url.format(tracking_number),
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest, settings: provider_utils.Settings
) -> lib.Serializable:
    request: lib.Pipeline = lib.Pipeline(
        process=lambda *_: _process_shipment(payload, settings),
        get_label=partial(_get_label, settings=settings),
    )

    return lib.Serializable(request)


def _process_shipment(
    payload: models.ShipmentRequest, settings: provider_utils.Settings
) -> lib.Job:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
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
                        address_line_1=recipient.street,
                        address_line_2=recipient.address_line2,
                        address_line_3=None,
                        attention=recipient.person_name,
                        city=recipient.city,
                        country=recipient.country_code,
                        email=recipient.email,
                        extension=None,
                        name=recipient.company_name,
                        phone=recipient.phone_number,
                        postal_code=recipient.postal_code,
                        province=recipient.state_code,
                        residential=recipient.residential,
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
                        address_line_1=shipper.street,
                        address_line_2=shipper.address_line2,
                        address_line_3=None,
                        attention=shipper.person_name,
                        city=shipper.city,
                        country=shipper.country_code,
                        email=shipper.email,
                        extension=None,
                        name=shipper.company_name,
                        phone=shipper.phone_number,
                        postal_code=shipper.postal_code,
                        province=shipper.state_code,
                        residential=shipper.residential,
                    ),
                    premium=provider_units.ShippingOption.is_premium(options),
                    proforma=None,
                    reported_weight_unit=provider_units.WeightUnit.LB.value,
                    send_email_to_delivery=recipient.email,
                    send_email_to_pickup=shipper.email,
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
