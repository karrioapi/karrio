import karrio.schemas.colissimo.label_request as colissimo
import karrio.schemas.colissimo.label_response as shipping
import typing
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
    shipment = _extract_details(response, settings)

    return shipment, messages


def _extract_details(
    data: dict,
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

    request = colissimo.LabelRequestType(
        contractNumber=settings.contract_number,
        password=settings.password,
        outputFormat=colissimo.OutputFormatType(
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
        letter=colissimo.LetterType(
            service=colissimo.ServiceType(
                productCode=service,
                depositDate=lib.fdate(options.shipment_date.state, "%Y-%m-%d"),
                mailBoxPicking=None,
                mailBoxPickingDate=None,
                vatCode=None,
                vatPercentage=None,
                vatAmount=None,
                transportationAmount=None,
                totalAmount=options.declared_value.state,
                orderNumber=None,
                commercialName=shipper.company_name,
                returnTypeChoice=None,
                reseauPostal=0,
            ),
            parcel=colissimo.ParcelType(
                parcelNumber=package.parcel.reference_number,
                insuranceAmount=None,
                insuranceValue=options.insurance.state,
                recommendationLevel=None,
                weight=package.weight.KG,
                nonMachinable=options.colissimo_non_machinable.state,
                returnReceipt=options.retun_receipt.state,
                instructions=None,
                pickupLocationId=None,
                ftd=options.colissimo_ftd.state,
                ddp=options.colissimo_ddp.state,
                codamount=options.cash_on_delivery.state,
                codcurrency=options.currency.state,
                cod=options.cash_on_delivery.state is not None,
            ),
            customsDeclarations=(
                colissimo.CustomsDeclarationsType(
                    includeCustomsDeclarations=True,
                    numberOfCopies=None,
                    contents=colissimo.ContentsType(
                        article=[
                            colissimo.ArticleType(
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
                    importerAddress=colissimo.AddressType(
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
            sender=colissimo.SenderType(
                senderParcelRef=payload.reference or package.parcel.reference_number,
                address=colissimo.AddressType(
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
                    phoneNumber=None,
                    mobileNumber=shipper.phone_number,
                    doorCode1=None,
                    doorCode2=None,
                    intercom=None,
                    email=shipper.email,
                    language=None,
                    stateOrProvinceCode=shipper.state_code,
                ),
            ),
            addressee=colissimo.AddresseeType(
                addresseeParcelRef=payload.reference or package.parcel.reference_number,
                codeBarForReference=None,
                serviceInfo=None,
                promotionCode=None,
                address=colissimo.AddressType(
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
                    phoneNumber=None,
                    mobileNumber=recipient.phone_number,
                    doorCode1=None,
                    doorCode2=None,
                    intercom=None,
                    email=recipient.email,
                    language=None,
                    stateOrProvinceCode=recipient.state_code,
                ),
            ),
            codSenderAddress=(
                colissimo.AddressType(
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
                    phoneNumber=None,
                    mobileNumber=recipient.phone_number,
                    doorCode1=None,
                    doorCode2=None,
                    intercom=None,
                    email=recipient.email,
                    language=None,
                    stateOrProvinceCode=recipient.state_code,
                )
                if options.cash_on_delivery.state is not None
                else None
            ),
            uploadDocument=None,
            features=colissimo.FeaturesType(printTrackingBarcode=True),
        ),
        fields=None,
    )

    return lib.Serializable(request, lib.to_dict)
