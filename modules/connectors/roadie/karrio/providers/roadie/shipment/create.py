import datetime
import karrio.schemas.roadie.shipment_request as roadie
import karrio.schemas.roadie.shipment_response as shipping
import typing
import base64
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.roadie.error as error
import karrio.providers.roadie.utils as provider_utils
import karrio.providers.roadie.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    shipment = (
        _extract_details(response, settings) if response.get("errors") is None else None
    )

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    shipment = lib.to_object(shipping.ShipmentResponse, data)
    label = lib.failsafe(
        lambda: lib.request(
            url=f"{settings.base_url}/v1/shipments/{shipment.id}/label?format=PDF",
            decoder=lambda _: base64.encodebytes(_).decode("utf-8"),
        )
    )

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=shipment.id,
        shipment_identifier=str(shipment.id),
        docs=models.Documents(label=label or ""),
        meta=dict(
            tracking_number=shipment.tracking_number,
            service_name=provider_units.ShippingService.roadie_local_delivery.value,
            reference_ids=[
                _.reference_id for _ in shipment.items if any(_.reference_id or "")
            ],
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    pickup_after = lib.to_date(
        options.pickup_after.state or datetime.datetime.now(),
        current_format="%Y-%m-%d %H:%M:%S",
    )
    deliver_start = lib.fdatetime(
        options.deliver_start.state or (pickup_after + datetime.timedelta(minutes=30)),
        current_format="%Y-%m-%d %H:%M:%S",
        output_format="%Y-%m-%dT%H:%M:%SZ",
    )
    deliver_end = lib.fdatetime(
        options.deliver_end.state or (pickup_after + datetime.timedelta(minutes=60)),
        current_format="%Y-%m-%d %H:%M:%S",
        output_format="%Y-%m-%dT%H:%M:%SZ",
    )

    request = roadie.ShipmentRequest(
        reference_id=payload.reference,
        description=packages.description,
        items=[
            roadie.Item(
                description=package.description,
                reference_id=package.parcel.reference_number,
                length=package.length.IN,
                width=package.width.IN,
                height=package.height.IN,
                weight=package.weight.LB,
                quantity=1,
                value=(
                    package.options.declared_value.state or options.declared_value.state
                ),
            )
            for package in packages
        ],
        pickup_location=roadie.Location(
            address=roadie.Address(
                name=shipper.company_name,
                store_number=None,
                street1=shipper.street,
                street2=shipper.address_line2,
                city=shipper.city,
                state=shipper.state_code,
                zip=shipper.postal_code,
            ),
            contact=roadie.Contact(
                name=shipper.contact,
                phone=shipper.phone_number,
            ),
        ),
        delivery_location=roadie.Location(
            address=roadie.Address(
                name=recipient.company_name,
                store_number=None,
                street1=recipient.street,
                street2=recipient.address_line2,
                city=recipient.city,
                state=recipient.state_code,
                zip=recipient.postal_code,
            ),
            contact=roadie.Contact(
                name=recipient.contact,
                phone=recipient.phone_number,
            ),
        ),
        pickup_after=lib.fdatetime(pickup_after, output_format="%Y-%m-%dT%H:%M:%SZ"),
        deliver_between=roadie.DeliverBetween(
            start=deliver_start,
            end=deliver_end,
        ),
        options=(
            roadie.Options(
                signature_required=options.roadie_signature_required.state,
                notifications_enabled=options.roadie_notifications_enabled.state,
                over_21__required=options.roadie_over_21_required.state,
                extra_compensation=options.roadie_extra_compensation.state,
                trailer_required=options.roadie_trailer_required.state,
            )
            if any(
                [
                    options.roadie_signature_required.state,
                    options.roadie_notifications_enabled.state,
                    options.roadie_over_21_required.state,
                    options.roadie_extra_compensation.state,
                    options.roadie_trailer_required.state,
                ]
            )
            else None
        ),
    )

    return lib.Serializable(
        request,
        lambda _: lib.to_dict(
            lib
            .to_json(_)
            .replace("over_21__required", "over_21_required")
        ),
    )
