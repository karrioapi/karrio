from dhl_express_lib.ship_val_global_req_10_0 import (
    ShipmentRequest as DHLShipmentRequest,
    Billing,
    Consignee,
    Contact,
    Commodity,
    Shipper,
    ShipmentDetails as DHLShipmentDetails,
    Reference,
    Dutiable,
    MetaData,
    Notification,
    SpecialService,
    WeightType,
    Label,
    ExportDeclaration,
    ExportLineItem,
    AdditionalInformation,
)
from dhl_express_lib.ship_val_global_res_10_0 import LabelImage, MultiLabelType
from dhl_express_lib.datatypes_global_v10 import Pieces, Piece

import time
import typing
import base64
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.core.errors as errors
import karrio.providers.dhl_express.error as provider_error
import karrio.providers.dhl_express.units as provider_units
import karrio.providers.dhl_express.utils as provider_utils


def parse_shipment_response(
    response: lib.Element, settings: provider_utils.Settings
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    air_way_bill = lib.find_element("AirwayBillNumber", response, first=True)

    return (
        _extract_shipment(response, settings) if air_way_bill is not None else None,
        provider_error.parse_error_response(response, settings),
    )


def _extract_shipment(
    shipment_node, settings: provider_utils.Settings
) -> typing.Optional[models.ShipmentDetails]:
    tracking_number = lib.find_element(
        "AirwayBillNumber", shipment_node, first=True
    ).text
    label_image = lib.find_element("LabelImage", shipment_node, LabelImage, first=True)
    multilabels: typing.List[MultiLabelType] = lib.find_element(
        "MultiLabel", shipment_node, MultiLabelType
    )
    invoice = next(
        (item for item in multilabels if item.DocName == "CustomInvoiceImage"), None
    )

    label = base64.encodebytes(label_image.OutputImage).decode("utf-8")
    invoice_data = (
        dict(invoice=base64.encodebytes(invoice.DocImageVal).decode("utf-8"))
        if invoice is not None
        else {}
    )

    return models.ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=tracking_number,
        shipment_identifier=tracking_number,
        docs=models.Documents(label=label, **invoice_data),
    )


def shipment_request(
    payload: models.ShipmentRequest, settings: provider_utils.Settings
) -> lib.Serializable[DHLShipmentRequest]:
    if any(settings.account_country_code or "") and (
        payload.shipper.country_code != settings.account_country_code
    ):
        raise errors.OriginNotServicedError(payload.shipper.country_code)

    packages = lib.to_packages(
        payload.parcels,
        provider_units.PackagePresets,
        required=["weight"],
        package_option_type=provider_units.ShippingOption,
    )
    product = provider_units.ProductCode.map(payload.service).value_or_key
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)

    weight_unit, dim_unit = (
        provider_units.COUNTRY_PREFERED_UNITS.get(payload.shipper.country_code)
        or packages.compatible_units
    )

    package_type = provider_units.PackageType.map(packages.package_type).value
    label_format, label_template = provider_units.LabelType[
        payload.label_type or "PDF_6x4"
    ].value
    payment = payload.payment or models.Payment(
        paid_by="sender", account_number=settings.account_number
    )
    customs = lib.to_customs_info(
        payload.customs,
        shipper=payload.shipper,
        recipient=payload.recipient,
        weight_unit=weight_unit.value,
    )
    is_document = all(p.parcel.is_document for p in packages)
    is_dutiable = is_document is False and customs.duty is not None
    options = lib.to_shipping_options(
        payload.options,
        is_dutiable=is_dutiable,
        package_options=packages.options,
        shipper_country=payload.shipper.country_code,
        initializer=provider_units.shipping_options_initializer,
    )

    duty = customs.duty or models.Duty(paid_by="sender")
    content = packages[0].parcel.content or customs.content_description or "N/A"
    reference = payload.reference or getattr(payload, "id", None)

    request = DHLShipmentRequest(
        schemaVersion="10.0",
        Request=settings.Request(
            MetaData=MetaData(SoftwareName="3PV", SoftwareVersion="10.0")
        ),
        RegionCode=provider_units.CountryRegion[shipper.country_code].value,
        LanguageCode="en",
        LatinResponseInd=None,
        Billing=Billing(
            ShipperAccountNumber=settings.account_number,
            ShippingPaymentType=provider_units.PaymentType[payment.paid_by].value,
            BillingAccountNumber=payment.account_number,
            DutyAccountNumber=duty.account_number,
        ),
        Consignee=Consignee(
            CompanyName=recipient.company_name or "N/A",
            SuiteDepartmentName=recipient.suite,
            AddressLine1=recipient.address_line1 or recipient.address_line,
            AddressLine2=lib.join(recipient.address_line2, join=True),
            AddressLine3=None,
            City=recipient.city,
            Division=None,
            DivisionCode=recipient.state_code,
            PostalCode=recipient.postal_code,
            CountryCode=recipient.country_code,
            CountryName=recipient.country_name,
            Contact=Contact(
                PersonName=recipient.person_name,
                PhoneNumber=recipient.phone_number or "0000",
                Email=recipient.email,
            ),
            Suburb=recipient.suburb,
            StreetName=recipient.street_name,
            BuildingName=None,
            StreetNumber=recipient.street_number,
            RegistrationNumbers=None,
            BusinessPartyTypeCode=None,
        ),
        Commodity=(
            [
                Commodity(CommodityCode=c.sku or "N/A", CommodityName=c.description)
                for c in customs.commodities
            ]
            if any(customs.commodities)
            else None
        ),
        Dutiable=(
            Dutiable(
                DeclaredValue=(
                    duty.declared_value or options.declared_value.state or 1.0
                ),
                DeclaredCurrency=(duty.currency or options.currency.state or "USD"),
                ScheduleB=None,
                ExportLicense=customs.options.license_number.state,
                ShipperEIN=None,
                ShipperIDType=None,
                TermsOfTrade=customs.incoterm,
                CommerceLicensed=None,
                Filing=None,
            )
            if is_dutiable
            else None
        ),
        UseDHLInvoice=("Y" if is_dutiable else None),
        DHLInvoiceLanguageCode=("en" if is_dutiable else None),
        DHLInvoiceType=(
            ("CMI" if customs.commercial_invoice else "PFI") if is_dutiable else None
        ),
        ExportDeclaration=(
            ExportDeclaration(
                InterConsignee=None,
                IsPartiesRelation=None,
                ECCN=None,
                SignatureName=customs.signer,
                SignatureTitle=None,
                ExportReason=customs.content_type,
                ExportReasonCode=provider_units.ExportReasonCode[
                    customs.content_type or "other"
                ].value,
                SedNumber=None,
                SedNumberType=None,
                MxStateCode=None,
                InvoiceNumber=(customs.invoice or "N/A"),
                InvoiceDate=(customs.invoice_date or time.strftime("%Y-%m-%d")),
                BillToCompanyName=customs.duty_billing_address.company_name,
                BillToContactName=customs.duty_billing_address.person_name,
                BillToAddressLine=customs.duty_billing_address.address_line,
                BillToCity=customs.duty_billing_address.city,
                BillToPostcode=customs.duty_billing_address.postal_code,
                BillToSuburb=customs.duty_billing_address.extra,
                BillToCountryName=customs.duty_billing_address.country_name,
                BillToPhoneNumber=customs.duty_billing_address.phone_number,
                BillToPhoneNumberExtn=None,
                BillToFaxNumber=None,
                BillToFederalTaxID=customs.duty_billing_address.federal_tax_id,
                Remarks=customs.content_description,
                DestinationPort=None,
                TermsOfPayment=None,
                PayerGSTVAT=customs.duty_billing_address.state_tax_id,
                SignatureImage=None,
                ReceiverReference=None,
                ExporterId=None,
                ExporterCode=None,
                ExportLineItem=[
                    ExportLineItem(
                        LineNumber=index,
                        Quantity=item.quantity,
                        QuantityUnit="PCS",
                        Description=item.description or "N/A",
                        Value=item.value_amount or 0.0,
                        IsDomestic=None,
                        CommodityCode=item.sku or "N/A",
                        ScheduleB=None,
                        ECCN=None,
                        Weight=WeightType(
                            Weight=item.weight,
                            WeightUnit=provider_units.WeightUnit[
                                item.weight_unit
                            ].value,
                        ),
                        GrossWeight=WeightType(
                            Weight=item.weight,
                            WeightUnit=provider_units.WeightUnit[
                                item.weight_unit
                            ].value,
                        ),
                        License=None,
                        LicenseSymbol=None,
                        ManufactureCountryCode=(
                            item.origin_country or shipper.country_code
                        ),
                        ManufactureCountryName=lib.to_country_name(item.origin_country),
                        ImportTaxManagedOutsideDhlExpress=None,
                        AdditionalInformation=None,
                        ImportCommodityCode=item.hs_code,
                        ItemReferences=None,
                        CustomsPaperworks=None,
                    )
                    for (index, item) in enumerate(customs.commodities, start=1)
                ],
                ShipmentDocument=None,
                InvoiceInstructions=None,
                CustomerDataTextEntries=None,
                PlaceOfIncoterm="N/A",
                ShipmentPurpose=(
                    "COMMERCIAL" if customs.commercial_invoice else "PERSONAL"
                ),
                DocumentFunction=None,
                CustomsDocuments=None,
                InvoiceTotalNetWeight=None,
                InvoiceTotalGrossWeight=None,
                InvoiceReferences=None,
            )
            if is_dutiable
            else None
        ),
        Reference=(
            [Reference(ReferenceID=reference[:30])] if any([reference]) else None
        ),
        ShipmentDetails=DHLShipmentDetails(
            Pieces=Pieces(
                Piece=[
                    Piece(
                        PieceID=index,
                        PackageType=(
                            package_type
                            or provider_units.PackageType[
                                package.packaging_type or "your_packaging"
                            ].value
                        ),
                        Depth=package.length.map(provider_units.MeasurementOptions)[
                            dim_unit.name
                        ],
                        Width=package.width.map(provider_units.MeasurementOptions)[
                            dim_unit.name
                        ],
                        Height=package.height.map(provider_units.MeasurementOptions)[
                            dim_unit.name
                        ],
                        Weight=package.weight[weight_unit.name],
                        PieceContents=(
                            package.parcel.content or package.parcel.description
                        ),
                        PieceReference=(
                            [Reference(ReferenceID=package.parcel.id[:30])]
                            if package.parcel.id is not None
                            else None
                        ),
                        AdditionalInformation=(
                            AdditionalInformation(
                                CustomerDescription=package.parcel.description
                            )
                            if package.parcel.description is not None
                            else None
                        ),
                    )
                    for (index, package) in enumerate(packages, start=1)
                ]
            ),
            WeightUnit=provider_units.WeightUnit[weight_unit.name].value,
            GlobalProductCode=product,
            LocalProductCode=product,
            Date=(options.shipment_date.state or time.strftime("%Y-%m-%d")),
            Contents=content,
            DimensionUnit=provider_units.DimensionUnit[dim_unit.name].value,
            PackageType=package_type,
            IsDutiable=("Y" if is_dutiable else "N"),
            CurrencyCode=options.currency.state or "USD",
            CustData=getattr(payload, "id", None),
            ShipmentCharges=(
                options.cash_on_delivery.state
                if options.cash_on_delivery.state
                else None
            ),
            ParentShipmentIdentificationNumber=None,
            ParentShipmentGlobalProductCode=None,
            ParentShipmentPackagesCount=None,
        ),
        Shipper=Shipper(
            ShipperID=settings.account_number or "N/A",
            CompanyName=shipper.company_name or "N/A",
            SuiteDepartmentName=shipper.suite,
            RegisteredAccount=settings.account_number,
            AddressLine1=shipper.address_line1 or shipper.address_line,
            AddressLine2=lib.join(shipper.address_line2, join=True),
            AddressLine3=None,
            City=shipper.city,
            Division=None,
            DivisionCode=shipper.state_code,
            PostalCode=shipper.postal_code,
            OriginServiceAreaCode=None,
            OriginFacilityCode=None,
            CountryCode=shipper.country_code,
            CountryName=shipper.country_name,
            Contact=Contact(
                PersonName=shipper.person_name,
                PhoneNumber=shipper.phone_number or "0000",
                Email=shipper.email,
            ),
            Suburb=shipper.suburb,
            StreetName=shipper.street_name,
            BuildingName=None,
            StreetNumber=shipper.street_number,
            RegistrationNumbers=None,
            BusinessPartyTypeCode=None,
        ),
        SpecialService=[
            SpecialService(
                SpecialServiceType=option.code,
                ChargeValue=lib.to_money(option.state),
                CurrencyCode=(
                    options.currency.state or "USD"
                    if lib.to_money(option.state) is not None
                    else None
                ),
            )
            for _, option in options.items()
        ],
        Notification=(
            Notification(
                EmailAddress=options.email_notification_to.state or recipient.email
            )
            if options.email_notification.state
            and any([options.email_notification_to.state, recipient.email])
            else None
        ),
        Place=None,
        EProcShip=None,
        Airwaybill=None,
        DocImages=None,
        LabelImageFormat=label_format,
        RequestArchiveDoc=None,
        NumberOfArchiveDoc=None,
        RequestQRCode="N",
        RequestTransportLabel=None,
        Label=Label(LabelTemplate=label_template),
        ODDLinkReq=None,
        DGs=None,
        GetPriceEstimate="Y",
        SinglePieceImage="N",
        ShipmentIdentificationNumber=None,
        UseOwnShipmentIdentificationNumber="N",
        Importer=None,
    )

    return lib.Serializable(request, _request_serializer)


def _request_serializer(request: DHLShipmentRequest) -> str:
    xml_str = lib.to_xml(
        request,
        name_="req:ShipmentRequest",
        namespacedef_='xsi:schemaLocation="http://www.dhl.com ship-val-global-req.xsd" xmlns:req="http://www.dhl.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
    ).replace('schemaVersion="10"', 'schemaVersion="10.0"')

    return xml_str
