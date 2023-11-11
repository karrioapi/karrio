import karrio.schemas.colissimo.label_request as colissimo
import karrio.schemas.colissimo.label_response as shipping
import typing
import base64
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.colissimo.error as error
import karrio.providers.colissimo.utils as provider_utils
import karrio.providers.colissimo.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    shipment = (
        _extract_details(response, settings, _response.ctx)
        if response.get("json_info", {}).get("labelV2Response") is not None
        else None
    )

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
    ctx: dict = {},
) -> models.ShipmentDetails:
    shipment = lib.to_object(shipping.LabelResponse, data.get("json_info"))
    label_type = ctx.get("label_type") or "PDF"
    label = data.get("label")

    if label_type != "ZPL":
        label = base64.b64encode(bytes(label, encoding="raw_unicode_escape")).decode(
            "utf-8"
        )

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=shipment.labelV2Response.parcelNumber,
        shipment_identifier=shipment.labelV2Response.parcelNumber,
        label_type="ZPL" if "ZPL" in label_type else "PDF",
        docs=models.Documents(label=label),
        meta=dict(
            carrier_tracking_link=settings.tracking_url.format(
                shipment.labelV2Response.parcelNumber
            ),
            request_uuid=data.get("uuid"),
            pdfUrl=shipment.labelV2Response.pdfUrl,
            parcelNumber=shipment.labelV2Response.parcelNumber,
            parcelNumberPartner=shipment.labelV2Response.parcelNumberPartner,
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    package = lib.to_packages(payload.parcels).single
    service = provider_units.ShippingService.map(payload.service).value_or_key
    options = lib.to_shipping_options(
        payload.options,
        package_options=package.options,
        option_type=provider_units.ShippingOption,
    )
    customs = lib.to_customs_info(
        payload.customs,
        option_type=provider_units.ShippingOption,
        shipper=shipper,
        recipient=recipient,
    )

    request = colissimo.LabelRequest(
        contractNumber=settings.contract_number,
        password=settings.password,
        outputFormat=colissimo.OutputFormat(
            x=0,
            y=0,
            outputPrintingType=(
                provider_units.LabelType.map(payload.label_type).value
                or provider_utils.LabelType.PDF.value
            ),
            dematerialized=None,
            returnType=None,
            printCODDocument=None,
        ),
        letter=colissimo.Letter(
            service=colissimo.Service(
                productCode=service,
                depositDate=lib.fdate(options.shipment_date.state, "%Y-%m-%d"),
                mailBoxPicking=None,
                mailBoxPickingDate=None,
                vatCode=None,
                vatPercentage=None,
                vatAmount=None,
                transportationAmount=options.declared_value.state,
                totalAmount=options.declared_value.state,
                orderNumber=None,
                commercialName=shipper.company_name,
                returnTypeChoice=None,
                reseauPostal=0,
            ),
            parcel=colissimo.Parcel(
                parcelNumber=package.parcel.reference_number,
                insuranceAmount=None,
                insuranceValue=options.insurance.state,
                recommendationLevel=None,
                weight=package.weight.KG,
                nonMachinable=options.colissimo_non_machinable.state,
                returnReceipt=options.colissimo_retun_receipt.state,
                instructions=None,
                pickupLocationId=None,
                ftd=options.colissimo_ftd.state,
                ddp=options.colissimo_ddp.state,
                codamount=options.cash_on_delivery.state,
                codcurrency=options.currency.state,
                cod=options.cash_on_delivery.state is not None,
            ),
            customsDeclarations=(
                colissimo.CustomsDeclarations(
                    includeCustomsDeclarations=True,
                    numberOfCopies=None,
                    contents=colissimo.Contents(
                        article=[
                            colissimo.Article(
                                description=item.description,
                                quantity=item.quantity,
                                weight=item.weight,
                                value=item.value_amount,
                                hsCode=item.hs_code,
                                originCountry=item.origin_country,
                                originCountryLabel=None,
                                currency=options.currency.state,
                                artref=item.metadata.get("artref", None),
                                originalIdent=None,
                                vatAmount=None,
                                customsFees=item.metadata.get("customs_fees", None),
                            )
                            for item in customs.commodities
                        ],
                        category=None,
                        original=None,
                        explanations=None,
                    ),
                    importersReference=None,
                    importersContact=shipper.contact,
                    officeOrigin=None,
                    comments=None,
                    description=customs.content_description,
                    invoiceNumber=customs.invoice,
                    licenceNumber=customs.options.license_number.state,
                    certificatNumber=customs.options.certificate_number.state,
                    importerAddress=colissimo.Address(
                        companyName=customs.duty_billing_address.company_name,
                        lastName=customs.duty_billing_address.person_name,
                        firstName=None,
                        line0=customs.duty_billing_address.suite,
                        line1=customs.duty_billing_address.street_number,
                        line2=customs.duty_billing_address.address_line1,
                        line3=customs.duty_billing_address.address_line2,
                        countryCode=customs.duty_billing_address.country_code,
                        countryLabel=customs.duty_billing_address.country_name,
                        city=customs.duty_billing_address.city,
                        zipCode=customs.duty_billing_address.postal_code,
                        phoneNumber=None,
                        mobileNumber=customs.duty_billing_address.phone_number,
                        doorCode1=None,
                        doorCode2=None,
                        intercom=None,
                        email=customs.duty_billing_address.email,
                        language=None,
                        stateOrProvinceCode=customs.duty_billing_address.state_code,
                    ),
                )
                if payload.customs is not None
                else None
            ),
            sender=colissimo.Sender(
                senderParcelRef=payload.reference or package.parcel.reference_number,
                address=colissimo.Address(
                    companyName=shipper.company_name,
                    lastName=shipper.person_name,
                    firstName=None,
                    line0=shipper.suite,
                    line1=shipper.street_number,
                    line2=shipper.address_line1,
                    line3=shipper.address_line2,
                    countryCode=shipper.country_code,
                    countryLabel=shipper.country_name,
                    city=shipper.city,
                    zipCode=shipper.postal_code,
                    phoneNumber=shipper.phone_number,
                    mobileNumber=None,
                    doorCode1=None,
                    doorCode2=None,
                    intercom=None,
                    email=shipper.email,
                    language="FR",
                    stateOrProvinceCode=shipper.state_code,
                ),
            ),
            addressee=colissimo.Addressee(
                addresseeParcelRef=payload.reference or package.parcel.reference_number,
                codeBarForReference=None,
                serviceInfo=None,
                promotionCode=None,
                address=colissimo.Address(
                    companyName=recipient.company_name,
                    lastName=recipient.person_name,
                    firstName=None,
                    line0=recipient.suite,
                    line1=recipient.street_number,
                    line2=recipient.address_line1,
                    line3=recipient.address_line2,
                    countryCode=recipient.country_code,
                    countryLabel=recipient.country_name,
                    city=recipient.city,
                    zipCode=recipient.postal_code,
                    phoneNumber=recipient.phone_number,
                    mobileNumber=None,
                    doorCode1=None,
                    doorCode2=None,
                    intercom=None,
                    email=recipient.email,
                    language="FR",
                    stateOrProvinceCode=recipient.state_code,
                ),
            ),
            codSenderAddress=(
                colissimo.Address(
                    companyName=recipient.company_name,
                    lastName=recipient.person_name,
                    firstName=None,
                    line0=recipient.suite,
                    line1=recipient.street_number,
                    line2=recipient.address_line1,
                    line3=recipient.address_line2,
                    countryCode=recipient.country_code,
                    countryLabel=recipient.country_name,
                    city=recipient.city,
                    zipCode=recipient.postal_code,
                    phoneNumber=recipient.phone_number,
                    mobileNumber=None,
                    doorCode1=None,
                    doorCode2=None,
                    intercom=None,
                    email=recipient.email,
                    language="FR",
                    stateOrProvinceCode=recipient.state_code,
                )
                if options.cash_on_delivery.state is not None
                else None
            ),
            uploadDocument=None,
            features=colissimo.Features(printTrackingBarcode=True),
        ),
        fields=(
            colissimo.Fields(
                customField=[
                    colissimo.Field(
                        key=key,
                        value=value,
                    )
                    for key, value in [
                        ("LENGTH", package.length.value),
                        ("WIDTH", package.width.value),
                        ("HEIGHT", package.height.value),
                    ]
                ]
            )
            if any(
                [
                    package.length.value,
                    package.width.value,
                    package.height.value,
                ]
            )
            else None
        ),
    )

    return lib.Serializable(
        request,
        lib.to_dict,
        dict(label_type=payload.label_type or "PDF"),
    )
