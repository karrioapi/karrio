import karrio.schemas.mydhl.shipping_requests as mydhl
import karrio.schemas.mydhl.shipping_response as shipping
import typing
import datetime
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.mydhl.error as error
import karrio.providers.mydhl.utils as provider_utils
import karrio.providers.mydhl.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    shipment = (
        _extract_details(response, settings)
        if "shipmentTrackingNumber" in response
        else None
    )

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    shipment = lib.to_object(shipping.ShippingResponseType, data)
    label_type = next(
        (_.imageFormat for _ in shipment.documents if _.typeCode == "label"), "PDF"
    )
    label = lib.bundle_base64(
        [_.content for _ in shipment.documents if _.typeCode == "label"],
        format=label_type,
    )

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=shipment.shipmentTrackingNumber,
        shipment_identifier=shipment.shipmentTrackingNumber,
        label_type=label_type,
        docs=models.Documents(label=label),
        meta=dict(
            localCutoffDateAndTime=lib.failsafe(
                lambda: shipment.shipmentDetails[0].pickupDetails.localCutoffDateAndTime
            ),
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    billing_address = lib.to_address(payload.billing_address or shipper)
    packages = lib.to_packages(payload.parcels)
    service = provider_units.ShippingService.map(payload.service).value_or_key
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
    )
    shipping_options = [
        option for _, option in options.items() if option.state is not False
    ]

    payment = payload.payment or models.Payment(
        paid_by="sender",
        account_number=settings.account_number,
    )
    customs = lib.to_customs_info(
        payload.customs,
        shipper=payload.shipper,
        recipient=payload.recipient,
        weight_unit=units.WeightUnit.KG.value,
    )
    reference = payload.reference or getattr(payload, "id", None)
    currency = lib.identity(
        options.currency.state
        or units.CountryCurrency.map(payload.shipper.country_code).value
        or settings.default_currency
    )

    # map data to convert karrio model to mydhl specific type
    request = mydhl.ShippingRequestType(
        plannedShippingDateAndTime=lib.fdatetime(
            options.shipment_date.state or datetime.datetime.now(),
            current_format="%Y-%m-%d",
            output_format="%Y-%m-%dT%H:%M:%S GMT%z",
        ),
        pickup=None,
        productCode=service,
        localProductCode=service,
        getRateEstimates=True,
        accounts=[
            mydhl.AccountType(
                typeCode=payment.paid_by,
                number=payment.account_number,
            )
        ],
        valueAddedServices=[
            mydhl.ValueAddedServiceType(
                serviceCode=option.code,
                value=lib.to_money(option.value),
                currency=currency if lib.to_money(option.state) is not None else None,
                method=None,
            )
            for option in shipping_options
        ],
        outputImageProperties=mydhl.OutputImagePropertiesType(
            printerDPI=300,
            encodingFormat=provider_units.LabelFormat.map(
                payload.labbel_type or "PDF"
            ).value,
            imageOptions=[],
            splitTransportAndWaybillDocLabels=True,
            allDocumentsInOneImage=False,
            splitDocumentsByPages=False,
            splitInvoiceAndReceipt=True,
            receiptAndLabelsInOneImage=False,
        ),
        customerDetails=mydhl.CustomerDetailsType(
            shipperDetails=mydhl.ReceiverDetailsClassType(
                postalAddress=mydhl.PostalAddressType(
                    cityName=shipper.city,
                    countryCode=shipper.country_code,
                    postalCode=shipper.postal_code,
                    addressLine1=shipper.address_line1,
                    addressLine2=shipper.address_line2,
                    countyName=None,
                    addressLine3=None,
                    countryName=None,
                    provinceCode=shipper.state_code,
                ),
                contactInformation=mydhl.ContactInformationType(
                    phone=shipper.phone_number or "+000000000000",
                    mobilePhone=None,
                    companyName=shipper.company_name or "N/A",
                    fullName=shipper.contact,
                    email=shipper.email,
                ),
                registrationNumbers=[],
                bankDetails=[],
                typeCode=("business" if shipper.company_name else None),
            ),
            receiverDetails=mydhl.ReceiverDetailsClassType(
                postalAddress=mydhl.PostalAddressType(
                    cityName=recipient.city,
                    countryCode=recipient.country_code,
                    postalCode=recipient.postal_code,
                    addressLine1=recipient.address_line1,
                    addressLine2=recipient.address_line2,
                    countyName=None,
                    addressLine3=None,
                    countryName=None,
                    provinceCode=recipient.state_code,
                ),
                contactInformation=mydhl.ContactInformationType(
                    phone=recipient.phone_number or "+000000000000",
                    mobilePhone=None,
                    companyName=recipient.company_name or "N/A",
                    fullName=recipient.contact,
                    email=recipient.email,
                ),
                registrationNumbers=[],
                bankDetails=[],
                typeCode=("business" if recipient.company_name else None),
            ),
            buyerDetails=None,
            importerDetails=None,
            exporterDetails=None,
            sellerDetails=None,
        ),
        content=mydhl.ContentType(
            packages=[
                mydhl.PackageType(
                    typeCode=None,
                    weight=package.weight.KG,
                    dimensions=mydhl.DimensionsType(
                        length=package.length.CM,
                        width=package.width.CM,
                        height=package.height.CM,
                    ),
                    customerReferences=[],
                    description=package.description,
                    labelDescription=None,
                )
                for package in packages
            ],
            isCustomsDeclarable=not packages.is_document,
            declaredValue=options.declared_value.state,
            declaredValueCurrency=currency,
            exportDeclaration=lib.identity(
                mydhl.ExportDeclarationType(
                    lineItems=[
                        mydhl.LineItemType(
                            number=item.hs_code or item.sku,
                            description=item.title or item.description,
                            price=item.value_amount,
                            quantity=mydhl.QuantityType(
                                value=item.quantity,
                                unitOfMeasurement=None,
                            ),
                            commodityCodes=[
                                mydhl.CustomerReferenceType(
                                    value=None,
                                    typeCode=None,
                                )
                            ],
                            exportReasonType=None,
                            manufacturerCountry=item.origin_country,
                            exportControlClassificationNumber=None,
                            weight=mydhl.WeightType(
                                netValue=None,
                                grossValue=item.weight,
                            ),
                            isTaxesPaid=None,
                            additionalInformation=[],
                            customerReferences=[],
                            customsDocuments=[],
                        )
                        for item in customs.commodities
                    ],
                    invoice=lib.identity(
                        mydhl.InvoiceType(
                            number=customs.invoice,
                            date=lib.fdatetime(
                                customs.invoice_date or datetime.datetime.now(),
                                current_format="%Y-%m-%d",
                                output_format="%Y-%m-%dT%H:%M:%S GMT%z",
                            ),
                            instructions=[],
                            totalNetWeight=packages.weight.KG,
                            totalGrossWeight=packages.items.weight.KG,
                            customerReferences=[
                                mydhl.CustomerReferenceType(
                                    value=_,
                                    typeCode="CU",
                                )
                                for _ in [reference]
                                if _ is not None
                            ],
                            termsOfPayment=None,
                            indicativeCustomsValues=None,
                            customerDataTextEntries=[],
                        )
                        if customs.invoice is not None
                        else None
                    ),
                    remarks=[],
                    additionalCharges=[],
                    destinationPortName=None,
                    placeOfIncoterm=None,
                    payerVATNumber=customs.options.vat_registration_number.state,
                    recipientReference=None,
                    exporter=None,
                    packageMarks=None,
                    declarationNotes=[],
                    exportReference=None,
                    exportReason=None,
                    exportReasonType=None,
                    licenses=[],
                    shipmentType=None,
                    customsDocuments=[],
                )
                if (payload.customs is not None and not packages.is_document)
                else None
            ),
            description=packages.description,
            USFilingTypeValue=None,
            incoterm=customs.incoterm,
            unitOfMeasurement="metric",
        ),
        shipmentNotification=[
            mydhl.ShipmentNotificationType(
                typeCode="email",
                receiverId=email,
                languageCode=None,
                languageCountryCode=None,
                bespokeMessage=None,
            )
            for email in lib.identity(
                []
                if options.email_notification.state is False
                else [options.email_notification_to.state or recipient.email]
            )
            if email is not None
        ],
        getTransliteratedResponse=None,
        estimatedDeliveryDate=None,
        getAdditionalInformation=[],
        customerReferences=[
            mydhl.CustomerReferenceType(
                value=reference,
                typeCode="CU",
            )
            for _ in [reference]
            if _ is not None
        ],
        documentImages=[
            mydhl.DocumentImageType(
                typeCode=lib.identity(
                    provider_units.UploadDocumentType.map(doc.get("doc_type")).value
                    or "INV"
                ),
                imageFormat=doc.get("doc_format") or "PDF",
                content=doc["doc_file"],
            )
            for doc in lib.identity(
                options.doc_files.state
                if options.dhl_paperless_trade.state == True
                and any(options.doc_files.state or [])
                else []
            )
        ],
        identifiers=[],
    )

    return lib.Serializable(request, lib.to_dict)
