from typing import List, Tuple
from datetime import datetime
from functools import reduce
from purplship.domain import entities as E
from purplship.domain.mapper import Mapper
from pyfedex import ship_service_v21 as Ship
from pyfedex import rate_v22 as Rate
from pyfedex import track_service_v14 as Track


def create_rate_request(mapper: Mapper, payload: E.quote_request) -> Rate.RateRequest:
    transactionDetail = Rate.TransactionDetail(CustomerTransactionId="FTC")
    version = Rate.VersionId(ServiceId="crs", Major=22, Intermediate=0, Minor=0)

    shipper = Rate.Party(
        Contact=None if not payload.shipper.company_name and not payload.shipper.phone_number else Rate.Contact(
            CompanyName=payload.shipper.company_name, 
            PhoneNumber=payload.shipper.phone_number
        ),
        Address=Rate.Address(
            City=payload.shipper.city,
            StateOrProvinceCode=payload.shipper.state_code,
            PostalCode=payload.shipper.postal_code,
            CountryCode=payload.shipper.country_code
        )
    )
    for line in payload.shipper.address_lines:
        shipper.Address.StreetLines.append(line)

    recipient = Rate.Party(
        Contact=None if not payload.recipient.company_name and not payload.recipient.phone_number else Rate.Contact(
            CompanyName=payload.recipient.company_name, 
            PhoneNumber=payload.recipient.phone_number
        ),
        Address=Rate.Address(
            City=payload.recipient.city,
            StateOrProvinceCode=payload.recipient.state_code,
            PostalCode=payload.recipient.postal_code,
            CountryCode=payload.recipient.country_code
        )
    )
    for line in payload.recipient.address_lines:
        recipient.Address.StreetLines.append(line)

    totalWeight = reduce(lambda r, p: r + p.weight, payload.shipment.packages, 0)

    packaging_type = payload.shipment.packaging_type or "YOUR_PACKAGING" 

    currency = payload.shipment.currency or "USD" 

    shipment = Rate.RequestedShipment(
        ShipTimestamp=datetime.now(),
        PackagingType=packaging_type,
        TotalWeight=Rate.Weight(
            Units=payload.shipment.weight_unit, 
            Value=totalWeight
        ),
        PreferredCurrency=currency,
        Shipper=shipper,
        Recipient=recipient,
        ShippingChargesPayment=Rate.Payment(
            PaymentType=payload.shipment.paid_by or "SENDER",
            Payor=Rate.Payor(ResponsibleParty=Rate.Party(
                AccountNumber=payload.shipment.shipper_account_number or payload.shipment.payment_account_number or mapper.client.account_number
            ))
        ),
        PackageCount=len(payload.shipment.packages)
    )

    for p in payload.shipment.packages:
        shipment.RequestedPackageLineItems.append(Rate.RequestedPackageLineItem(
            GroupPackageCount=1,
            Weight=Rate.Weight(
                Units=payload.shipment.weight_unit, 
                Value=p.weight
            ),
            Dimensions=Rate.Dimensions(
                Length=p.length, Width=p.width, Height=p.height, 
                Units=payload.shipment.dimension_unit
            )
        ))

    shipment.RateRequestTypes.append("LIST")
    return Rate.RateRequest(
        WebAuthenticationDetail=mapper.webAuthenticationDetail,
        ClientDetail=mapper.clientDetail,
        TransactionDetail=transactionDetail,
        Version=version,
        RequestedShipment=shipment
    )



def create_track_request(mapper: Mapper, payload: E.tracking_request) -> Track.TrackRequest:
    version = Track.VersionId(ServiceId="trck", Major=14, Intermediate=0, Minor=0)
    transactionDetail = Track.TransactionDetail(
        CustomerTransactionId="Track By Number_v14",
        Localization=Track.Localization(LanguageCode=payload.language_code or "en")
    )
    track_request = Track.TrackRequest(
        WebAuthenticationDetail=mapper.webAuthenticationDetail,
        ClientDetail=mapper.clientDetail,
        TransactionDetail=transactionDetail,
        Version=version,
    )
    for tracking_number in payload.tracking_numbers:
        track_request.add_SelectionDetails(Track.TrackSelectionDetail(
            CarrierCode="FDXE",
            PackageIdentifier=Track.TrackPackageIdentifier(
                Type="TRACKING_NUMBER_OR_DOORTAG",
                Value=tracking_number
            )
        ))
    return track_request



def create_shipment_request(mapper: Mapper, payload: E.shipment_request) -> Ship.ProcessShipmentRequest:
    ShipmentAuthorizationDetail_ = Ship.ShipmentAuthorizationDetail(
        AccountNumber=payload.shipment.shipper_account_number or payload.shipment.shipper_account_number or mapper.client.account_number
    )

    def _create_party(data: E.party, account_number: str) -> Ship.Party:
        Party_ = Ship.Party(
            AccountNumber=account_number,
            Tins=data.extra.get('Tins'),
            Address=Ship.Address(
                StreetLines=data.address_lines,
                City=data.city,
                StateOrProvinceCode=data.state_code,
                PostalCode=data.postal_code,
                UrbanizationCode=data.extra.get('UrbanizationCode'),
                CountryCode=data.country_code,
                CountryName=data.country_name,
                Residential=data.extra.get('Residential'),
                GeographicCoordinates=data.extra.get('GeographicCoordinates')
            ),
        )

        if any([
            data.company_name, data.phone_number, 
            data.email_address, data.person_name
        ]):
            Party_.Contact = Ship.Contact(
                ContactId=data.extra.get('ContactId'),
                PersonName=data.person_name,
                Title=data.extra.get('Title'),
                CompanyName=data.company_name,
                PhoneNumber=data.phone_number,
                PhoneExtension=data.extra.get('PhoneExtension'),
                TollFreePhoneNumber=data.extra.get('TollFreePhoneNumber'),
                PagerNumber=data.extra.get('PagerNumber'),
                FaxNumber=data.extra.get('FaxNumber'),
                EMailAddress=data.email_address
            )
        return Party_

    Shipper_ = _create_party(payload.shipper, payload.shipment.shipper_account_number)

    Recipient_ = _create_party(payload.recipient, payload.recipient.extra.get('AccountNumber'))

    FreightShipmentDetail_ = Ship.FreightShipmentDetail(
        FedExFreightAccountNumber=payload.shipment.shipper_account_number or mapper.client.account_number,
        FedExFreightBillingContactAndAddress=payload.shipment.extra.get("FedExFreightBillingContactAndAddress"),
        AlternateBilling=payload.shipment.extra.get("AlternateBilling"),
        Role=payload.shipment.extra.get("Role"),
        CollectTermsType=payload.shipment.extra.get("CollectTermsType"),
        DeclaredValuePerUnit=payload.shipment.extra.get("DeclaredValuePerUnit"),
        DeclaredValueUnits=payload.shipment.extra.get("DeclaredValueUnits"),
        TotalHandlingUnits=payload.shipment.extra.get("TotalHandlingUnits"),
        ClientDiscountPercent=payload.shipment.extra.get("ClientDiscountPercent"),
        PalletWeight=payload.shipment.total_weight,
        ShipmentDimensions=payload.shipment.extra.get("ShipmentDimensions"),
        Comment=payload.shipment.extra.get("Comment"),
        HazardousMaterialsEmergencyContactNumber=payload.shipment.extra.get("HazardousMaterialsEmergencyContactNumber"),
        HazardousMaterialsOfferor=payload.shipment.extra.get("HazardousMaterialsOfferor")
    )

    if 'SpecialServicePayments' in payload.shipment.extra:
        FreightShipmentDetail_.SpecialServicePayments = Ship.FreightSpecialServicePayment(
            SpecialService=payload.shipment.extra.get("SpecialServicePayments").get("SpecialService"),
            PaymentType=payload.shipment.extra.get("SpecialServicePayments").get("PaymentType")
        )

    if 'Coupons' in payload.shipment.extra:
        for coupon in payload.shipment.extra.get("Coupons"):
            FreightShipmentDetail_.add_Coupons(coupon)

    if 'LiabilityCoverageDetail' in payload.shipment.extra:
        FreightShipmentDetail_.LiabilityCoverageDetail = Ship.LiabilityCoverageDetail(
            CoverageType=payload.shipment.extra.get("LiabilityCoverageDetail").get("CoverageType"),
            CoverageAmount=payload.shipment.extra.get("LiabilityCoverageDetail").get("CoverageType")
        )

    for ref in payload.shipment.references:
        FreightShipmentDetail_.add_PrintedReferences(Ship.PrintedReference(Value=ref))

    RequestedShipment_ = Ship.RequestedShipment(
        ShipTimestamp=datetime.now(),
        DropoffType=payload.shipment.extra.get("DropoffType") or "REGULAR_PICKUP",
        ServiceType=payload.shipment.extra.get("ServiceType") or "INTERNATIONAL_PRIORITY",
        PackagingType=payload.shipment.extra.get("PackagingType"),
        TotalWeight=payload.shipment.total_weight or reduce(lambda t, p: t + p.weight, payload.shipment.packages,0),
        TotalInsuredValue=payload.shipment.insured_amount,
        PreferredCurrency=payload.shipment.currency or "USD",
        ShipmentAuthorizationDetail=ShipmentAuthorizationDetail_,
        Shipper=Shipper_,
        Recipient=Recipient_,
        RecipientLocationNumber=payload.shipment.extra.get("RecipientLocationNumber"),
        Origin=payload.shipment.extra.get("Origin"),
        SoldTo=payload.shipment.paid_by,
        FreightShipmentDetail=FreightShipmentDetail_,
        DeliveryInstructions=payload.shipment.extra.get("DeliveryInstructions"),
        BlockInsightVisibility=payload.shipment.extra.get("BlockInsightVisibility"),
        RateRequestTypes=payload.shipment.extra.get('RateRequestTypes') or 'LIST',
        EdtRequestType=payload.shipment.extra.get('EdtRequestType'),
        MasterTrackingId=payload.shipment.extra.get('MasterTrackingId'),
        PackageCount=len(payload.shipment.packages),
        # ShippingDocumentSpecification=,           TODO: Implement this when required 
        # ConfigurationData=,                       TODO: Implement this when required
    )

    for id, pkg in enumerate(payload.shipment.packages):
        RequestedShipment_.RequestedPackageLineItems.append(
            Ship.RequestedPackageLineItem(
                SequenceNumber=id,
                GroupNumber=1,
                GroupPackageCount=len(payload.shipment.packages),
                VariableHandlingChargeDetail=pkg.extra.get("VariableHandlingChargeDetail"),
                InsuredValue=pkg.extra.get("InsuredValue"),
                Weight=Ship.Weight(
                    Value=pkg.weight,
                    Units=payload.shipment.weight_unit
                ),
                Dimensions=Ship.Dimensions(
                    Length=pkg.length,
                    Width=pkg.width,
                    Height=pkg.height,
                    Units=payload.shipment.dimension_unit
                ),
                PhysicalPackaging=pkg.extra.get("PhysicalPackaging"),
                ItemDescription=pkg.description,
                ItemDescriptionForClearance=pkg.extra.get("ItemDescriptionForClearance"),
                CustomerReferences=pkg.extra.get("CustomerReferences"),
                SpecialServicesRequested=pkg.extra.get("SpecialServicesRequested"),
                ContentRecords=pkg.extra.get("ContentRecords")
            )
        )

    if 'Payor' in payload.shipment.extra or payload.shipment.paid_by is not None:
        if payload.shipment.paid_by == 'THIRD_PARTY':
            ResponsibleParty_ = _create_party(E.party(**payload.shipment.extra('Payor')), payload.shipment.billing_account_number)  
        else:
            ResponsibleParty_ = Shipper_
        RequestedShipment_.ShippingChargesPayment=Ship.Payment(
            PaymentType=payload.shipment.paid_by,
            Payor=Ship.Payor(ResponsibleParty=ResponsibleParty_) if ResponsibleParty_ is not None else None
        )

    if payload.shipment.label is not None:
        RequestedShipment_.LabelSpecification = Ship.LabelSpecification(
            Dispositions=payload.shipment.label.extra.get('Dispositions'),
            LabelFormatType=payload.shipment.label.format,
            ImageType=payload.shipment.label.type,
            LabelStockType=payload.shipment.label.extra.get('LabelStockType'),
            LabelPrintingOrientation=payload.shipment.label.extra.get('LabelPrintingOrientation'),
            LabelOrder=payload.shipment.label.extra.get('LabelOrder'),
            PrintedLabelOrigin=payload.shipment.label.extra.get('PrintedLabelOrigin'),
            CustomerSpecifiedDetail=payload.shipment.label.extra.get('CustomerSpecifiedDetail')
        )

    if 'SmartPostDetail' in payload.shipment.extra: 
        smartP = payload.shipment.extra.get('SmartPostDetail')
        RequestedShipment_.SmartPostDetail = Ship.SmartPostShipmentDetail(
            ProcessingOptionsRequested=smartP.get('ProcessingOptionsRequested'),
            Indicia=smartP.get('Indicia'),
            AncillaryEndorsement=smartP.get('AncillaryEndorsement'),
            HubId=smartP.get('HubId'),
            CustomerManifestId=smartP.get('CustomerManifestId')
        )

    if 'PickupDetail' in payload.shipment.extra:
        """
        Pickup detail is a json of pickup request type ofr consistency
        """
        pickup = E.Pickup.request(**payload.shipment.extra.get("PickupDetail"))
        RequestedShipment_.PickupDetail = Ship.PickupDetail(
            ReadyDateTime=pickup.ready_time,
            LatestPickupDateTime=pickup.closing_time,
            CourierInstructions=pickup.instruction,
            RequestType=pickup.extra.get('RequestType'),
            RequestSource=pickup.extra.get('RequestSource'),
        )

    if payload.shipment.customs is not None:
        RequestedShipment_.CustomsClearanceDetail = Ship.CustomsClearanceDetail(
            Brokers=payload.shipment.customs.extra.get("Brokers"),
            ClearanceBrokerage=payload.shipment.customs.extra.get("ClearanceBrokerage"),
            CustomsOptions=payload.shipment.customs.extra.get("CustomsOptions"),
            ImporterOfRecord=payload.shipment.customs.extra.get("ImporterOfRecord"),
            RecipientCustomsId=payload.shipment.customs.extra.get('RecipientCustomsId'),
            DutiesPayment=payload.shipment.duty_payment_account,
            DocumentContent=payload.shipment.customs.description,
            CustomsValue=payload.shipment.customs.extra.get('CustomsValue'),
            FreightOnValue=payload.shipment.customs.extra.get('FreightOnValue'),
            InsuranceCharges=payload.shipment.insured_amount,
            PartiesToTransactionAreRelated=payload.shipment.customs.extra.get('PartiesToTransactionAreRelated'),
            
            # Commodities=,                         #TODO integrate when possible 
            # ExportDetail=,                        #TODO integrate when possible
            # RegulatoryControls=,                  #TODO integrate when possible
            # DeclarationStatementDetail=           #TODO integrate when possible
        )   

        if 'CommercialInvoice' in payload.shipment.customs.extra:
            CommercialInvoice = payload.shipment.customs.extra.get('CommercialInvoice')
            RequestedShipment_.CustomsClearanceDetail.CommercialInvoice = Ship.CommercialInvoice(
                Comments=CommercialInvoice.get('Comments'),
                FreightCharge=CommercialInvoice.get('Freightcharge'),
                TaxesOrMiscellaneousCharge=CommercialInvoice.get('TaxesOrMiscellaneousCharge'),
                TaxesOrMiscellaneousChargeType=CommercialInvoice.get('TaxesOrMiscellaneousChargeType'),
                PackingCosts=CommercialInvoice.get('PackingCosts'),
                HandlingCosts=CommercialInvoice.get('HandlingCosts'),
                SpecialInstructions=CommercialInvoice.get('SpecialInstructions'),
                DeclarationStatement=CommercialInvoice.get('DeclarationStatement'),
                PaymentTerms=CommercialInvoice.get('PaymentTerms'),
                Purpose=CommercialInvoice.get('Purpose'),
                CustomerReferences=CommercialInvoice.get('CustomerReferences'),
                OriginatorName=CommercialInvoice.get('OriginatorName'),
                TermsOfSale=CommercialInvoice.get('TermsOfSale')
            )

    if 'VariableHandlingChargeDetail' in payload.shipment.extra:
        RequestedShipment_.VariableHandlingChargeDetail = Ship.VariableHandlingChargeDetail(
            FixedValue=payload.shipment.extra.get("VariableHandlingChargeDetail").get("FixedValue"),
            PercentValue=payload.shipment.extra.get("VariableHandlingChargeDetail").get("PercentValue"),
            RateElementBasis=payload.shipment.extra.get("VariableHandlingChargeDetail").get("RateElementBasis")
        )

    if 'ExpressFreightDetail' in payload.shipment.extra:
        RequestedShipment_.ExpressFreightDetail = Ship.ExpressFreightDetail(
            PackingListEnclosed=payload.shipment.extra.get("ExpressFreightDetail").get("PackingListEnclosed"),
            ShippersLoadAndCount=payload.shipment.extra.get("ExpressFreightDetail").get("ShippersLoadAndCount"),
            BookingConfirmationNumber=payload.shipment.extra.get("ExpressFreightDetail").get("BookingConfirmationNumber")
        )

    if 'SpecialServicesRequested' in payload.shipment.extra:

        RequestedShipment_.SpecialServicesRequested = Ship.ShipmentSpecialServicesRequested(
            # SpecialServiceTypes=,
            # CodDetail=,
            # DeliveryOnInvoiceAcceptanceDetail=,
            # HoldAtLocationDetail=,
            # EventNotificationDetail=,
            # ReturnShipmentDetail=,
            # PendingShipmentDetail=,
            # InternationalControlledExportDetail=,
            # InternationalTrafficInArmsRegulationsDetail=,
            # ShipmentDryIceDetail=,
            # HomeDeliveryPremiumDetail=,
            # FreightGuaranteeDetail=,
            # EtdDetail=,
            # CustomDeliveryWindowDetail=
        )

    if 'ManifestDetail' in payload.shipment.extra:
        RequestedShipment_.ManifestDetail=Ship.ShipmentManifestDetail(
            ManifestReferenceType=payload.shipment.extra.get("ManifestDetail").get('ManifestReferenceType')
        )

    return Ship.ProcessShipmentRequest(
        WebAuthenticationDetail=mapper.webAuthenticationDetail,
        ClientDetail=mapper.clientDetail,
        TransactionDetail=Rate.TransactionDetail(CustomerTransactionId="IE_v18_Ship"),
        Version=Rate.VersionId(ServiceId="ship", Major=21, Intermediate=0, Minor=0),
        RequestedShipment=RequestedShipment_
    )

