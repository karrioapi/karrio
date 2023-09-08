import karrio.schemas.locate2u.shipping_request as locate2u
import karrio.schemas.locate2u.shipping_response as shipping
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.locate2u.error as error
import karrio.providers.locate2u.utils as provider_utils
import karrio.providers.locate2u.units as provider_units


def parse_shipment_response(
    response: dict,
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    messages = error.parse_error_response(response, settings)
    shipment = _extract_details(response, settings) if len(messages) == 0 else None

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    shipment = lib.to_object(shipping.ShippingResponse, data)

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=str(shipment.stopId),
        shipment_identifier=str(shipment.stopId),
        label_type="PDF",
        docs=models.Documents(label=""),
        meta=dict(
            shipmentId=shipment.shipmentId,
            durationMinutes=shipment.durationMinutes,
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    recipient = lib.to_address(payload.recipient)
    package = lib.to_packages(payload.parcels).single
    service = provider_units.ShippingService.map(payload.service).value_or_key
    options = lib.to_shipping_options(
        payload.options,
        package_options=package.options,
        option_type=provider_units.ShippingOption,
    )

    request = locate2u.ShippingRequest(
        contact=locate2u.Contact(
            name=recipient.contact,
            phone=recipient.phone_number,
            email=recipient.email,
        ),
        name=recipient.company_name or recipient.person_name,
        address=recipient.address_line,
        location=(
            locate2u.Location(
                latitude=options.latitude.state,
                longitude=options.longitude.state,
            )
            if any([options.latitude.state, recipient.longitude.state])
            else None
        ),
        appointmentTime=options.appointment_time.state,
        timeWindowStart=options.time_window_start.state,
        timeWindowEnd=options.time_window_end.state,
        brandId=options.brand_id.state,
        durationMinutes=options.duration_minutes.state,
        tripDate=lib.fdatetime(
            options.shipment_date.state,
            current_format="%Y-%m-%d",
            output_format="%Y-%m-%dT%H:%M:%S.%zZ",
        ),
        customFields=None,
        assignedTeamMemberId=None,
        source=settings.connection_config.source,
        sourceReference=payload.reference,
        load=locate2u.Load(
            quantity=package.items.quantity,
            volume=package.volume.value,
            weight=package.weight.value,
            length=package.length.value,
            width=package.width.value,
            height=package.height.value,
        ),
        customerId=options.customer_id.state,
        runNumber=options.run_number.state,
        teamRegionId=options.team_region_id.state,
        driverInstructions=options.driver_instructions.state,
        notes=options.notes.state,
        lines=[
            locate2u.Line(
                barcode=item.hs_code or item.sku,
                description=item.title or item.description,
                currentLocation=item.origin_country,
                serviceId=service,
                productVariantId=None,
                quantity=item.quantity,
            )
            for item in package.items
        ],
    )

    return lib.Serializable(request, lib.to_dict)
