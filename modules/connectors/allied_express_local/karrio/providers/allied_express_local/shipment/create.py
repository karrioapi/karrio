import karrio.schemas.allied_express_local.label_request as allied
import karrio.schemas.allied_express_local.label_response as shipping
import typing
import datetime
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.allied_express_local.error as error
import karrio.providers.allied_express_local.utils as provider_utils
import karrio.providers.allied_express_local.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[provider_utils.AlliedResponse],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    shipment = (
        _extract_details(response, settings, ctx=_response.ctx)
        if not response.is_error and "result" in (response.response or {})
        else None
    )

    return shipment, messages


def _extract_details(
    data: provider_utils.AlliedResponse,
    settings: provider_utils.Settings,
    ctx: dict = {},
) -> models.ShipmentDetails:
    shipment: shipping.LabelResponseType = lib.to_object(
        shipping.LabelResponseType, data.response
    )
    label = shipment.result or shipment.soapenvBody.ns1getLabelResponse.result

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=shipment.Tracking,
        shipment_identifier=shipment.Tracking,
        label_type="PDF",
        docs=models.Documents(label=label),
        meta=dict(
            postal_code=ctx.get("postal_code", ""),
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    service = provider_units.ShippingService.map(payload.service).value_or_key
    options = lib.to_shipping_options(
        payload.options,
        option_type=provider_units.ShippingOption,
    )
    packages = lib.to_packages(
        payload.parcels,
        options=options,
        package_option_type=provider_units.ShippingOption,
        shipping_options_initializer=provider_units.shipping_options_initializer,
    )

    request = allied.LabelRequestType(
        bookedBy=shipper.contact,
        account=settings.account,
        readyDate=lib.fdatetime(
            options.shipment_date.state or datetime.datetime.now(),
            current_format="%Y-%m-%d",
            output_format="%Y-%m-%dT%H:%M:%S.%f",
        ),
        instructions=options.instructions.state or "N/A",
        itemCount=len(packages),
        items=[
            allied.ItemType(
                dangerous=(True if pkg.options.dangerous_good.state else False),
                height=pkg.height.map(provider_units.MeasurementOptions).CM,
                length=pkg.length.map(provider_units.MeasurementOptions).CM,
                width=pkg.width.map(provider_units.MeasurementOptions).CM,
                weight=pkg.weight.map(provider_units.MeasurementOptions).KG,
                volume=pkg.volume.map(provider_units.MeasurementOptions).m3,
                itemCount=(pkg.items.quantity if any(pkg.items) else 1),
            )
            for pkg in packages
        ],
        jobStopsP=allied.JobStopsType(
            companyName=(shipper.company_name or shipper.contact),
            contact=shipper.contact,
            emailAddress=shipper.email or " ",
            geographicAddress=allied.GeographicAddressType(
                address1=shipper.address_line1,
                address2=shipper.address_line2 or " ",
                country=shipper.country_code,
                postCode=shipper.postal_code,
                state=shipper.state_code,
                suburb=shipper.city,
            ),
            phoneNumber=shipper.phone_number or "(00) 0000 0000",
        ),
        jobStopsD=allied.JobStopsType(
            companyName=(recipient.company_name or recipient.contact),
            contact=recipient.contact,
            emailAddress=recipient.email or " ",
            geographicAddress=allied.GeographicAddressType(
                address1=recipient.address_line1,
                address2=recipient.address_line2 or " ",
                country=recipient.country_code,
                postCode=recipient.postal_code,
                state=recipient.state_code,
                suburb=recipient.city,
            ),
            phoneNumber=recipient.phone_number or "(00) 0000 0000",
        ),
        referenceNumbers=([payload.reference] if any(payload.reference or "") else []),
        weight=packages.weight.map(provider_units.MeasurementOptions).KG,
        volume=packages.volume.map(provider_units.MeasurementOptions).m3,
        serviceLevel=service,
    )

    return lib.Serializable(
        request,
        lambda _: lib.to_json(_)
        .replace("jobStopsP", "jobStops_P")
        .replace("jobStopsD", "jobStops_D"),
        dict(postal_code=recipient.postal_code),
    )
