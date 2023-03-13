import dpd_lib.ShipmentServiceV33 as dpd
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.dpd.error as error
import karrio.providers.dpd.utils as provider_utils
import karrio.providers.dpd.units as provider_units


def parse_shipment_response(
    response: lib.Element,
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response_messages = []  # extract carrier response errors
    response_shipment = None  # extract carrier response shipment

    messages = error.parse_error_response(response_messages, settings)
    shipment = _extract_details(response_shipment, settings)

    return shipment, messages


def _extract_details(
    data: lib.Element,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    shipment = None  # parse carrier shipment type from "data"
    label = ""  # extract and process the shipment label to a valid base64 text
    # invoice = ""  # extract and process the shipment invoice to a valid base64 text if applies

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number="",  # extract tracking number from shipment
        shipment_identifier="",  # extract shipment identifier from shipment
        label_type="PDF",  # extract shipment label file format
        docs=models.Documents(
            label=label,  # pass label base64 text
            # invoice=invoice,  # pass invoice base64 text if applies
        ),
        meta=dict(
            # any relevent meta
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    options = lib.to_shipping_options(payload.options, provider_units.ShippingOption)
    service = provider_units.Services.map(payload.service).value_or_key
    is_intl = shipper.country_code != recipient.country_code
    customs = lib.to_customs_info(
        payload.customs,
        shipper=payload.shipper,
        recipient=payload.recipient,
        weight_unit=units.WeightUnit.KG.value,
    )

    request = lib.Envelope(
        Header=lib.Header(
            settings.authentication,
        ),
        Body=lib.Body(
            dpd.storeOrders(
                printOptions=dpd.printOptions(
                    printerLanguage=units.LabelType.map(
                        payload.label_type or "PDF"
                    ).value,
                    paperFormat="A6",
                    printer=None,
                    startPosition=None,
                    printerResolution=None,
                ),
                order=dpd.order(
                    generalShipmentData=dpd.generalShipmentData(
                        mpsId=None,
                        cUser=None,
                        mpsCustomerReferenceNumber1=payload.reference,
                        mpsCustomerReferenceNumber2=None,
                        mpsCustomerReferenceNumber3=None,
                        mpsCustomerReferenceNumber4=None,
                        identificationNumber=None,
                        sendingDepot=None,
                        product=service,
                        mpsCompleteDelivery=None,
                        mpsCompleteDeliveryLabel=None,
                        mpsVolume=None,
                        mpsExpectedSendingDate=None,
                        mpsExpectedSendingTime=None,
                        sender=dpd.address(
                            name1=(shipper.person_name or shipper.company_name),
                            name2=shipper.company_name,
                            street=shipper.address_line1,
                            houseNo=shipper.street_number,
                            street2=shipper.address_line2,
                            state=shipper.state_code,
                            country=shipper.country_code,
                            zipCode=shipper.postal_code,
                            city=shipper.city,
                            gln=None,
                            customerNumber=None,
                            type_=("P" if payload.residential else "B"),
                            contact=None,
                            phone=shipper.phone_number,
                            fax=None,
                            email=shipper.email,
                            comment=None,
                            iaccount=None,
                            eoriNumber=None,
                            vatNumber=None,
                            idDocType=None,
                            idDocNumber=None,
                            webSite=None,
                            referenceNumber=None,
                            destinationCountryRegistration=None,
                        ),
                        recipient=dpd.address(
                            name1=(recipient.person_name or recipient.company_name),
                            name2=recipient.company_name,
                            street=recipient.address_line1,
                            houseNo=recipient.street_number,
                            street2=recipient.address_line2,
                            state=recipient.state_code,
                            country=recipient.country_code,
                            zipCode=recipient.postal_code,
                            city=recipient.city,
                            gln=None,
                            customerNumber=None,
                            type_=("P" if recipient.residential else "B"),
                            contact=None,
                            phone=None,
                            fax=None,
                            email=recipient.email,
                            comment=None,
                            iaccount=None,
                            eoriNumber=None,
                            vatNumber=None,
                            idDocType=None,
                            idDocNumber=None,
                            webSite=None,
                            referenceNumber=None,
                            destinationCountryRegistration=None,
                        ),
                    ),
                    parcels=[
                        dpd.parcels(
                            parcelLabelNumber=None,
                            customerReferenceNumber1=pkg.parcel.reference_number,
                            customerReferenceNumber2=None,
                            customerReferenceNumber3=None,
                            customerReferenceNumber4=None,
                            swap=None,
                            volume=None,
                            weight=pkg.weight.KG,
                            hazardousLimitedQuantities=None,
                            higherInsurance=None,
                            content=None,
                            addService=None,
                            messageNumber=None,
                            function=None,
                            parameter=None,
                            cod=None,
                            international=(
                                dpd.international(
                                    parcelType=None,
                                    customsAmount=None,
                                    customsCurrency=None,
                                    customsAmountEx=None,
                                    customsCurrencyEx=None,
                                    clearanceCleared=None,
                                    prealertStatus=None,
                                    exportReason=None,
                                    customsTerms=None,
                                    customsContent=None,
                                    customsPaper=None,
                                    customsEnclosure=None,
                                    customsInvoice=customs.invoice,
                                    customsInvoiceDate=customs.invoice_date,
                                    customsAmountParcel=None,
                                    linehaul=None,
                                    shipMrn=None,
                                    collectiveCustomsClearance=None,
                                    comment1=None,
                                    comment2=None,
                                    commercialInvoiceConsigneeVatNumber=None,
                                    commercialInvoiceConsignee=None,
                                    commercialInvoiceConsignor=None,
                                    commercialInvoiceLine=None,
                                )
                                if is_intl
                                else None
                            ),
                            hazardous=None,
                            printInfo1OnParcelLabel=None,
                            info1=None,
                            info2=None,
                            returns=None,
                            customsTransportCost=None,
                            customsTransportCostCurrency=None,
                        )
                        for pkg in packages
                    ],
                    productAndServiceData=dpd.productAndServiceData(
                        orderType="consignment",
                        saturdayDelivery=options.saturday_delivery.state,
                        exWorksDelivery=options.dpd_ex_works_delivery.state,
                        guarantee=None,
                        tyres=None,
                        personalDelivery=None,
                        pickup=None,
                        parcelShopDelivery=(
                            dpd.parcelShopDelivery(
                                parcelShopId=None,
                                parcelShopNotification=None,
                            )
                            if options.parcel_shop_delivery.state
                            else None
                        ),
                        predict=None,
                        personalDeliveryNotification=None,
                        proactiveNotification=None,
                        delivery=None,
                        invoiceAddress=None,
                        countrySpecificService=None,
                    ),
                ),
            )
        ),
    )

    return lib.Serializable(
        request,
        lambda envelope: lib.envelope_serializer(
            envelope,
            namespace=(
                'xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" '
                'xmlns:ns="http://dpd.com/common/service/types/Authentication/2.0" '
                'xmlns:ns1="http://dpd.com/common/service/types/ShipmentService/3.3"'
            ),
            prefixes=dict(
                Envelope="soapenv",
                authentication="ns",
                storeOrders="ns1",
                storeOrders_children="",
            ),
        ),
    )
