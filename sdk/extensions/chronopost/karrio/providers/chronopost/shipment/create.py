import time
from typing import List, Tuple, Optional
from chronopost_lib.services import (
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
from karrio.core.models import (
    Documents,
    Message,
    Payment,
    ShipmentRequest,
    ShipmentDetails,
)
from karrio.core.utils import (
    Serializable,
    Element,
    create_envelope,
    XP,
    DF,
)
from karrio.core.units import (
    CompleteAddress,
    CustomsInfo,
    Packages,
    Options,
    WeightUnit,
)
from karrio.providers.chronopost.error import parse_error_response
from karrio.providers.chronopost.utils import Settings
from karrio.providers.chronopost.units import (
    WeightUnit,
    Option,
    Service,
    LabelType,
)


def parse_shipment_response(
    response: Element, settings: Settings
) -> Tuple[ShipmentDetails, List[Message]]:
    errors = parse_error_response(response, settings)
    shipment = (
        _extract_details(response, settings)
        if XP.find("return", response, first=True) is not None
        else None
    )

    return shipment, errors


def _extract_details(response: Element, settings: Settings) -> ShipmentDetails:
    shipment = XP.find("return", response, resultMultiParcelExpeditionValue, first=True)

    return ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        docs=Documents(
            label=shipment.pdfEtiquette,
        ),
    )


def shipment_request(payload: ShipmentRequest, settings: Settings) -> Serializable[str]:
    packages = Packages(payload.parcels, required=["weight"])
    shipper = CompleteAddress.map(payload.shipper)
    recipient = CompleteAddress.map(payload.recipient)
    options = Options(payload.options, Option)
    customs = CustomsInfo(payload.customs)

    shipping_date = DF.fdatetime(
        options.shipment_date or time.strftime("%Y-%m-%d"),
        current_format="%Y-%m-%d",
        output_format="%Y-%m-%dT%H:%M:%SZ",
    )

    is_international = shipper.country_code != recipient.country_code
    service_type = Service.map(payload.service).value_or_key or (
        Service.chronopost_express_international.value
        if is_international
        else Service.chronopost_13.value
    )
    label_type = LabelType.map(payload.label_type or "PDF").value
    payment = payload.payment or Payment()
    quantity = len(customs.commodities or []) if customs.is_defined else 1

    request = create_envelope(
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
                weightUnit=WeightUnit.KG,
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

    return Serializable(
        request,
        lambda req: settings.serialize(
            req, "shippingMultiParcelV5", settings.server_url
        ),
        logged=True,
    )
