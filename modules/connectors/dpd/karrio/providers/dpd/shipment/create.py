import karrio.schemas.dpd.ShipmentServiceV33 as dpd
import typing
import base64
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.dpd.error as error
import karrio.providers.dpd.utils as provider_utils
import karrio.providers.dpd.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    response_shipment = lib.find_element("shipmentResponses", response)

    messages = error.parse_error_response(response, settings)
    shipment = (
        _extract_details(response, settings) if len(response_shipment) > 0 else None
    )

    return shipment, messages


def _extract_details(
    data: lib.Element,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    label = getattr(
        lib.find_element("orderResult", data, dpd.StoreOrdersResponseDto33, first=True),
        "parcellabelsPDF",
        None,
    )
    shipments: typing.List[dpd.shipmentResponses] = lib.find_element(
        "shipmentResponses", data, dpd.shipmentResponses
    )
    parcels: typing.List[dpd.parcelInformation] = sum(
        [_.parcelInformation for _ in shipments], start=[]
    )
    tracking_numbers = [_.parcelLabelNumber for _ in parcels]
    shipment_identifiers = [_.mpsId for _ in shipments]

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_numbers[0],
        shipment_identifier=shipment_identifiers[0],
        docs=models.Documents(label=base64.b64encode(label).decode("utf-8")),
        meta=dict(
            carrier_tracking_link=settings.tracking_url.format(tracking_numbers[0]),
            shipment_identifiers=shipment_identifiers,
            tracking_numbers=tracking_numbers,
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    service = provider_units.ShippingService.map(payload.service).value_or_key
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )
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
                order=[
                    dpd.order(
                        generalShipmentData=dpd.generalShipmentData(
                            mpsId=None,
                            cUser=None,
                            mpsCustomerReferenceNumber1=(
                                payload.reference
                                if any(payload.reference or "")
                                else None
                            ),
                            mpsCustomerReferenceNumber2=None,
                            mpsCustomerReferenceNumber3=None,
                            mpsCustomerReferenceNumber4=None,
                            identificationNumber=None,
                            sendingDepot=settings.depot,
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
                                type_=("P" if shipper.residential else "B"),
                                contact=shipper.person_name,
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
                                contact=recipient.person_name,
                                phone=recipient.phone_number,
                                fax=None,
                                email=recipient.email,
                                comment=None,
                                iaccount=None,
                                eoriNumber=None,
                                vatNumber=recipient.tax_id,
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
                                volume=pkg.volume.m3,
                                weight=pkg.weight.KG,
                                hazardousLimitedQuantities=None,
                                higherInsurance=None,
                                content=pkg.parcel.content,
                                addService=None,
                                messageNumber=None,
                                function=None,
                                parameter=None,
                                cod=None,
                                international=(
                                    dpd.international(
                                        parcelType=False,
                                        customsAmount=(
                                            customs.duty.declared_value
                                            or options.declared_value.state
                                        ),
                                        customsCurrency=(
                                            customs.duty.currency
                                            or options.currency.state
                                        ),
                                        customsAmountEx=(
                                            customs.duty.declared_value
                                            or options.declared_value.state
                                        ),
                                        customsCurrencyEx=(
                                            customs.duty.currency
                                            or options.currency.state
                                        ),
                                        clearanceCleared="N",
                                        prealertStatus="S03",
                                        exportReason=provider_units.CustomsContentType.map(
                                            customs.incoterm
                                        ).value,
                                        customsTerms=(
                                            provider_units.Incoterm.map(
                                                customs.incoterm
                                            ).value
                                            or "DAP"
                                        ),
                                        customsContent=customs.content_description,
                                        customsPaper="A",
                                        customsEnclosure=None,
                                        customsInvoice=customs.invoice,
                                        customsInvoiceDate=lib.fdatetime(
                                            customs.invoice_date,
                                            current_format="%Y-%m-%d",
                                            output_format="%Y%m%d",
                                        ),
                                        customsAmountParcel=None,
                                        linehaul=None,
                                        shipMrn=None,
                                        collectiveCustomsClearance=None,
                                        comment1=None,
                                        comment2=None,
                                        commercialInvoiceConsigneeVatNumber=(
                                            customs.duty_billing_address.tax_id
                                        ),
                                        commercialInvoiceConsignee=dpd.address(
                                            name1=(
                                                customs.duty_billing_address.person_name
                                                or customs.duty_billing_address.company_name
                                            ),
                                            name2=customs.duty_billing_address.company_name,
                                            street=customs.duty_billing_address.address_line1,
                                            houseNo=customs.duty_billing_address.street_number,
                                            street2=customs.duty_billing_address.address_line2,
                                            state=customs.duty_billing_address.state_code,
                                            country=customs.duty_billing_address.country_code,
                                            zipCode=customs.duty_billing_address.postal_code,
                                            city=customs.duty_billing_address.city,
                                            gln=None,
                                            customerNumber=None,
                                            type_=(
                                                "P"
                                                if customs.duty_billing_address.residential
                                                else "B"
                                            ),
                                            contact=customs.duty_billing_address.person_name,
                                            phone=customs.duty_billing_address.phone_number,
                                            fax=None,
                                            email=customs.duty_billing_address.email,
                                            comment=None,
                                            iaccount=None,
                                            eoriNumber=customs.options.eoriNumber.state,
                                            vatNumber=(
                                                customs.options.vatNumber.state
                                                or customs.duty_billing_address.tax_id
                                            ),
                                            idDocType=None,
                                            idDocNumber=None,
                                            webSite=None,
                                            referenceNumber=None,
                                            destinationCountryRegistration=None,
                                        ),
                                        commercialInvoiceConsignor=dpd.address(
                                            name1=shipper.contact,
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
                                            type_=("P" if shipper.residential else "B"),
                                            contact=shipper.person_name,
                                            phone=shipper.phone_number,
                                            fax=None,
                                            email=shipper.email,
                                            comment=None,
                                            iaccount=None,
                                            eoriNumber=None,
                                            vatNumber=shipper.tax_id,
                                            idDocType=None,
                                            idDocNumber=None,
                                            webSite=None,
                                            referenceNumber=None,
                                            destinationCountryRegistration=None,
                                        ),
                                        commercialInvoiceLine=[
                                            dpd.internationalLine(
                                                customsTarif=(item.hs_code or item.sku),
                                                receiverCustomsTarif=(
                                                    item.hs_code or item.sku
                                                ),
                                                productCode=item.sku,
                                                content=(
                                                    item.title or item.description
                                                ),
                                                grossWeight=units.Weight(
                                                    item.weight,
                                                    item.weight_unit or "KG",
                                                ).KG,
                                                itemsNumber=index,
                                                amountLine=item.value_amount,
                                                customsOrigin=item.origin_country,
                                                invoicePosition=None,
                                            )
                                            for index, item in enumerate(
                                                pkg.items
                                                if any(pkg.items)
                                                else customs.commodities,
                                                start=1,
                                            )
                                        ],
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
                            for index, pkg in enumerate(packages)
                        ],
                        productAndServiceData=dpd.productAndServiceData(
                            orderType=options.dpd_order_type.state or "consignment",
                            saturdayDelivery=options.saturday_delivery.state,
                            exWorksDelivery=options.dpd_ex_works_delivery.state,
                            guarantee=None,
                            tyres=options.dpd_tyres.state,
                            personalDelivery=None,
                            pickup=None,
                            parcelShopDelivery=(
                                dpd.parcelShopDelivery(
                                    parcelShopId=options.parcel_shop_delivery.state,
                                    parcelShopNotification=(
                                        dpd.notification(
                                            channel=(
                                                "3"
                                                if (
                                                    options.email_notification_to.state
                                                    is None
                                                    and recipient.email is None
                                                )
                                                else "1"
                                            ),
                                            value=(
                                                options.email_notification_to.state
                                                or recipient.email
                                                or recipient.phone_number
                                            ),
                                            language="EN",
                                        )
                                        if any(
                                            [
                                                options.email_notification_to.state,
                                                recipient.email,
                                                recipient.phone_number,
                                            ]
                                        )
                                        else None
                                    ),
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
                    )
                ],
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
                delisId="",
                authToken="",
                messageLanguage="",
                storeOrders="ns1",
                storeOrders_children="",
                printOptions="",
                order="",
            ),
        ),
    )
