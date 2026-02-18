import karrio.schemas.dhl_parcel_de.returns_request as dhl_returns
import karrio.schemas.dhl_parcel_de.returns_response as returns
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.dhl_parcel_de.error as error
import karrio.providers.dhl_parcel_de.utils as provider_utils
import karrio.providers.dhl_parcel_de.units as provider_units


def parse_return_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    shipment = (
        _extract_details(response, settings)
        if response.get("shipmentNo")
        else None
    )

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    confirmation = lib.to_object(returns.ReturnOrderConfirmationType, data)
    tracking_number = str(confirmation.shipmentNo)
    label = lib.failsafe(lambda: confirmation.label.b64)
    qr_label = lib.failsafe(lambda: confirmation.qrLabel.b64)

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        shipment_identifier=tracking_number,
        label_type="PDF",
        docs=models.Documents(
            label=label,
            extra_documents=[
                models.ShippingDocument(
                    category="qr_label",
                    format="PDF",
                    base64=qr_label,
                )
            ] if qr_label else [],
        ),
        meta=dict(
            carrier_tracking_link=settings.tracking_url.format(tracking_number),
            shipmentNo=confirmation.shipmentNo,
            internationalShipmentNo=confirmation.internationalShipmentNo,
            routingCode=confirmation.routingCode,
            qrLink=confirmation.qrLink,
            tracking_numbers=[tracking_number],
            shipment_identifiers=[tracking_number],
        ),
    )


def return_shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    packages = lib.to_packages(
        payload.parcels,
        options=payload.options,
        shipping_options_initializer=provider_units.shipping_options_initializer,
    )
    package = packages[0]
    customs = lib.to_customs_info(
        payload.customs,
        weight_unit=units.WeightUnit.KG.name,
    )
    options = lib.to_shipping_options(
        payload.options,
        initializer=provider_units.shipping_options_initializer,
    )

    # Resolve receiver_id: from options, or derive from shipper country (ISO 3166-1 alpha-3 lowercase)
    receiver_id = (
        options["dhl_parcel_de_return_receiver_id"].state
        or units.CountryCode.map(shipper.country_code or "DE").value_or_key.lower()
    )

    request = dhl_returns.ReturnOrderType(
        receiverId=receiver_id,
        customerReference=payload.reference or None,
        shipmentReference=payload.metadata.get("shipment_reference") if payload.metadata else None,
        shipper=dhl_returns.ContactAddressType(
            name1=shipper.company_name or shipper.person_name,
            name2=(shipper.person_name if shipper.company_name else None),
            name3=None,
            addressStreet=lib.identity(
                shipper.street_name
                if shipper.street_number
                else shipper.address_line1
            ),
            addressHouse=lib.text(
                (
                    shipper.street_number
                    if shipper.street_number
                    else shipper.address_line2
                ),
                max=10,
            ),
            postalCode=shipper.postal_code,
            city=shipper.city,
            state=shipper.state_code,
            email=shipper.email,
            phone=shipper.phone_number,
        ),
        itemWeight=dhl_returns.WeightType(
            uom=units.WeightUnit.KG.name.lower(),
            value=package.weight.KG,
        ),
        itemValue=(
            dhl_returns.ValueType(
                currency=options.currency.state or "EUR",
                value=options.declared_value.state,
            )
            if options.declared_value.state
            else None
        ),
        customsDetails=(
            dhl_returns.CustomsDetailsType(
                items=[
                    dhl_returns.CommodityType(
                        itemDescription=item.description or item.title,
                        packagedQuantity=item.quantity,
                        countryOfOrigin=units.CountryCode.map(
                            item.origin_country or ""
                        ).value_or_key,
                        hsCode=item.hs_code,
                        itemWeight=dhl_returns.WeightType(
                            uom=units.WeightUnit.KG.name.lower(),
                            value=item.weight,
                        ),
                        itemValue=dhl_returns.ValueType(
                            currency=lib.identity(
                                item.value_currency
                                or options.currency.state
                                or "EUR"
                            ),
                            value=item.value_amount or 0.0,
                        ),
                    )
                    for item in customs.commodities
                ],
            )
            if payload.customs is not None and customs.commodities
            else None
        ),
    )

    return lib.Serializable(
        request,
        lib.to_dict,
        dict(
            labelType=lib.identity(
                "BOTH"
                if not payload.label_type
                else "SHIPMENT_LABEL"
            ),
        ),
    )
