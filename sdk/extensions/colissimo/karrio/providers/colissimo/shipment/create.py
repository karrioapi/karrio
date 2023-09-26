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
    packages = lib.to_packages(payload.parcels)
    service = provider_units.ShippingService.map(payload.service).value_or_key
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        option_type=provider_units.ShippingOption,
    )

    request = colissimo.LabelRequestType(
        contractNumber=settings.contract_number,
        password=settings.password,
        outputFormat=colissimo.OutputFormatType(
            x=None,
            y=None,
            outputPrintingType=None,
            dematerialized=None,
            returnType=None,
            printCODDocument=None,
        ),
        letter=colissimo.LetterType(
            service=colissimo.ServiceType(
                productCode=service,
                depositDate=None,
                mailBoxPicking=None,
                mailBoxPickingDate=None,
                vatCode=None,
                vatPercentage=None,
                vatAmount=None,
                transportationAmount=None,
                totalAmount=None,
                orderNumber=None,
                commercialName=None,
                returnTypeChoice=None,
                reseauPostal=None,
            ),
            parcel=colissimo.ParcelType(
                parcelNumber=None,
                insuranceAmount=None,
                insuranceValue=None,
                recommendationLevel=None,
                weight=None,
                nonMachinable=None,
                returnReceipt=None,
                instructions=None,
                pickupLocationId=None,
                ftd=None,
                ddp=None,
                codamount=None,
                codcurrency=None,
                cod=None,
            ),
            customsDeclarations=colissimo.CustomsDeclarationsType(
                includeCustomsDeclarations=None,
                numberOfCopies=None,
                contents=colissimo.ContentsType(
                    article=None,
                    category=None,
                    original=None,
                    explanations=None,
                ),
                importersReference=None,
                importersContact=None,
                officeOrigin=None,
                comments=None,
                description=None,
                invoiceNumber=None,
                licenseNumber=None,
                certificatNumber=None,
                importerAddress=colissimo.AddressType(
                    companyName=None,
                    lastName=None,
                    firstName=None,
                    line0=None,
                    line1=None,
                    line2=None,
                    line3=None,
                    countryCode=None,
                    countryLabel=None,
                    city=None,
                    zipCode=None,
                    phoneNumber=None,
                    mobileNumber=None,
                    doorCode1=None,
                    doorCode2=None,
                    intercom=None,
                    email=None,
                    language=None,
                    stateOrProvinceCode=None,
                ),
            ),
            sender=colissimo.SenderType(
                senderParcelRef=None,
                address=colissimo.AddressType(
                    companyName=None,
                    lastName=None,
                    firstName=None,
                    line0=None,
                    line1=None,
                    line2=None,
                    line3=None,
                    countryCode=None,
                    countryLabel=None,
                    city=None,
                    zipCode=None,
                    phoneNumber=None,
                    mobileNumber=None,
                    doorCode1=None,
                    doorCode2=None,
                    intercom=None,
                    email=None,
                    language=None,
                    stateOrProvinceCode=None,
                ),
            ),
            addressee=colissimo.AddresseeType(
                companyName=None,
                lastName=None,
                firstName=None,
                line0=None,
                line1=None,
                line2=None,
                line3=None,
                countryCode=None,
                countryLabel=None,
                city=None,
                zipCode=None,
                phoneNumber=None,
                mobileNumber=None,
                doorCode1=None,
                doorCode2=None,
                intercom=None,
                email=None,
                language=None,
                stateOrProvinceCode=None,
            ),
            codSenderAddress=colissimo.AddressType(
                companyName=None,
                lastName=None,
                firstName=None,
                line0=None,
                line1=None,
                line2=None,
                line3=None,
                countryCode=None,
                countryLabel=None,
                city=None,
                zipCode=None,
                phoneNumber=None,
                mobileNumber=None,
                doorCode1=None,
                doorCode2=None,
                intercom=None,
                email=None,
                language=None,
                stateOrProvinceCode=None,
            ),
            uploadDocument=colissimo.UploadDocumentType(
                documentContent=None,
            ),
            features=colissimo.FeaturesType(
                printTrackingBarcode=None,
            ),
        ),
        fields=colissimo.FieldsType(
            field=None,
            customField=None,
        ),
    )

    return lib.Serializable(request, lib.to_dict)
