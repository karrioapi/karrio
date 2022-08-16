import time
import typing
from chronopost_lib.shippingservice import (
    customerValue,
    esdValue,
    headerValue,
    recipientValue,
    refValue,
    resultMultiParcelExpeditionValue,
    shippingMultiParcelV5,
    shipperValue,
    skybillParamsValue,
    skybillValue,
)
import time
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.chronopost.error as provider_error
import karrio.providers.chronopost.utils as provider_utils
import karrio.providers.chronopost.units as provider_units


def parse_shipment_response(
    response: lib.lib.Element, settings: provider_utils.provider_utils.Settings
) -> typing.Tuple[models.models.ShipmentDetails, typing.List[models.Message]]:
    errors = provider_error.parse_error_response(response, settings)
    shipment = (
        _extract_details(response, settings)
        if lib.find_element("return", response, first=True) is not None
        else None
    )

    return shipment, errors


def _extract_details(response: lib.Element, settings: provider_utils.Settings) -> models.ShipmentDetails:
    shipment = lib.find_element("return", response, resultMultiParcelExpeditionValue, first=True)

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        docs=models.Documents(
            label=shipment.pdfEtiquette,
        ),
    )


def shipment_request(payload: models.ShipmentRequest, settings: provider_utils.Settings) -> lib.Serializable[str]:
    packages = lib.to_packages(
        payload.parcels,
        required=["weight"],
        package_option_type=provider_units.ShippingOption,
    )
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    customs = lib.to_customs_info(payload.customs)
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    shipping_date = lib.fdatetime(
        options.shipment_date or time.strftime("%Y-%m-%d"),
        current_format="%Y-%m-%d",
        output_format="%Y-%m-%dT%H:%M:%SZ",
    )

    is_international = shipper.country_code != recipient.country_code
    service_type = provider_units.Service.map(payload.service).value_or_key or (
        provider_units.chronopost_express_international.value
        if is_international
        else provider_units.Service.chronopost_13.value
    )
    label_type = provider_units.LabelType.map(payload.label_type or "PDF").value
    payment = payload.payment or models.Payment()
    quantity = len(customs.commodities or []) if customs.is_defined else 1

    request = lib.create_envelope(
        body_content=shippingMultiParcelV5(
            esdValue=esdValue(),
            headerValue=settings.header_value(),
            shipperValue=shipperValue(
                shipperAdress1=shipper.address_line1,
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
            customerValue=customerValue(),
            recipientValue=recipientValue(
                recipientAdress1=recipient.address_line1,
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
            refValue=refValue(),
            skybillValue=skybillValue(
                bulkNumber=len(packages),
                codCurrency=None,
                codValue=None,
                customsCurrency=None,
                customsValue=None,
                evtCode="DC",
                insuredCurrency=None,
                insuredValue=None,
                latitude=None,
                longitude=None,
                masterSkybillNumber=None,
                objectType="MAR",
                portCurrency=None,
                portValue=None,
                productCode=service_type,
                qualite=None,
                service="0",
                shipDate=shipping_date,
                shipHour="10",
                skybillRank=None,
                source=None,
                weight=packages.weight.KG,
                weightUnit=provider_units.WeightUnit.KG,
            ),
            skybillParamsValue=skybillParamsValue(
                duplicata=None,
                mode=label_type,
            ),
            password=settings.password,
            modeRetour=1,
            numberOfParcel=len(packages),
            version="2.0",
            multiParcel="Y" if len(packages) > 1 else "N",
        ),
    )

    return lib.Serializable(
        request,
        lambda req: settings.serialize(req, "shippingMultiParcelV5", settings.server_url),
    )
