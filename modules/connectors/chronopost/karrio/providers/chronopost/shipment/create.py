import karrio.schemas.chronopost.shippingservice as chronopost
import typing
import base64
import datetime
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.chronopost.error as provider_error
import karrio.providers.chronopost.utils as provider_utils
import karrio.providers.chronopost.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    errors = provider_error.parse_error_response(response, settings)
    shipment_node = lib.find_element("resultMultiParcelValue", response, first=True)
    shipment = (
        _extract_details(shipment_node, settings) if shipment_node is not None else None
    )

    return shipment, errors


def _extract_details(
    response: lib.Element, settings: provider_utils.Settings
) -> models.ShipmentDetails:
    shipment = lib.to_object(chronopost.resultMultiParcelValue, response)
    label = base64.b64encode(shipment.pdfEtiquette).decode("utf-8")

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=shipment.skybillNumber,
        shipment_identifier=shipment.skybillNumber,
        docs=models.Documents(label=label),
        meta=dict(
            carrier_tracking_link=settings.tracking_url.format(shipment.skybillNumber),
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest, settings: provider_utils.Settings
) -> lib.Serializable:
    package = lib.to_packages(
        payload.parcels,
        required=["weight"],
        package_option_type=provider_units.ShippingOption,
    ).single
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    customs = lib.to_customs_info(payload.customs)
    options = lib.to_shipping_options(
        payload.options,
        package_options=package.options,
        initializer=provider_units.shipping_options_initializer,
    )
    shipping_date = lib.to_date(options.shipment_date.state) or datetime.datetime.now()
    product_code = provider_units.ShippingService.map(payload.service).value_or_key
    label_type = provider_units.LabelType.map(payload.label_type or "PDF").value

    request = lib.Envelope(
        Body=lib.Body(
            chronopost.shippingMultiParcelV5(
                esdValue=None,
                headerValue=settings.header_value,
                shipperValue=(
                    chronopost.shipperValue(
                        shipperAdress1=shipper.street,
                        shipperAdress2=shipper.address_line2,
                        shipperCity=shipper.city,
                        shipperContactName=shipper.person_name,
                        shipperCountry=shipper.country_code,
                        shipperCountryName=shipper.country_name,
                        shipperEmail=shipper.email,
                        shipperMobilePhone=shipper.phone_number,
                        shipperName=shipper.company_name,
                        shipperName2=shipper.company_name,
                        shipperPreAlert=0,
                        shipperCivility="M",
                        shipperZipCode=shipper.postal_code,
                    ),
                ),
                customerValue=chronopost.customerValue(
                    customerAdress1=recipient.street,
                    customerAdress2=recipient.address_line2,
                    customerCity=recipient.city,
                    customerContactName=recipient.person_name,
                    customerCountry=recipient.country_code,
                    customerCountryName=recipient.country_name,
                    customerEmail=recipient.email,
                    customerMobilePhone=recipient.phone_number,
                    customerName=recipient.company_name,
                    customerName2=recipient.company_name,
                    customerPreAlert=0,
                    customerZipCode=recipient.postal_code,
                    printAsSender=None,
                    customerCivility="M",
                ),
                recipientValue=(
                    chronopost.recipientValue(
                        recipientAdress1=recipient.street,
                        recipientAdress2=recipient.address_line2,
                        recipientCity=recipient.city,
                        recipientContactName=recipient.person_name,
                        recipientCountry=recipient.country_code,
                        recipientCountryName=recipient.country_name,
                        recipientEmail=recipient.email,
                        recipientMobilePhone=recipient.phone_number,
                        recipientName=recipient.company_name,
                        recipientName2=recipient.company_name,
                        recipientPreAlert=0,
                        recipientZipCode=recipient.postal_code,
                    ),
                ),
                refValue=(
                    chronopost.refValue(
                        shipperRef=payload.reference,
                        recipientRef=None,
                        customerSkybillNumber=None,
                        PCardTransactionNumber=None,
                    ),
                ),
                skybillValue=(
                    chronopost.skybillValue(
                        bulkNumber=1,
                        codCurrency=(
                            options.currency.state
                            if options.cash_on_delivery.state is not None
                            else None
                        ),
                        codValue=options.cash_on_delivery.state,
                        customsCurrency=(
                            (customs.duty.currency or options.currency)
                            if payload.customs is not None
                            else None
                        ),
                        customsValue=(
                            (customs.duty.declared_value or options.declared_value)
                            if payload.customs is not None
                            else None
                        ),
                        evtCode="DC",
                        insuredCurrency=(
                            options.currency.state
                            if options.insurance.state is not None
                            else None
                        ),
                        insuredValue=options.insurance.state,
                        latitude=None,
                        longitude=None,
                        masterSkybillNumber=None,
                        objectType=(
                            provider_units.CustomsContentType.map(
                                customs.content_type or "MAR"
                            ).value
                        ),
                        portCurrency=None,
                        portValue=None,
                        productCode=product_code.zfill(2),
                        qualite=None,
                        service="0",
                        shipDate=shipping_date.strftime("%Y-%m-%dT%H:%M:%S"),
                        shipHour="10",
                        skybillRank=None,
                        source=None,
                        weight=package.weight.KG,
                        weightUnit=provider_units.WeightUnit.KG.value,
                    ),
                ),
                skybillParamsValue=chronopost.skybillParamsValue(
                    duplicata=None,
                    mode=label_type,
                ),
                password=settings.password,
                modeRetour=1,
                numberOfParcel=1,
                version="2.0",
                multiParcel="N",
            ),
        )
    )

    return lib.Serializable(
        request,
        lambda envelope: lib.envelope_serializer(
            envelope,
            namespace=(
                'xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" '
                'xmlns:cxf="http://cxf.shipping.soap.chronopost.fr/"'
            ),
            prefixes=dict(Envelope="soapenv"),
        ),
    )
