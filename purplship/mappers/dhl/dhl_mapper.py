from typing import List, Tuple, TypeVar, Union
from functools import reduce
import time
from base64 import b64decode
from purplship.domain import entities as E
from purplship.domain.mapper import Mapper
from purplship.mappers.dhl.dhl_client import DHLClient
from pydhl import DCT_req_global as Req, DCT_Response_global as Res, tracking_request_known as Track, tracking_response as TrackRes
from pydhl.datatypes_global_v61 import ServiceHeader, MetaData, Request
from pydhl import ship_val_global_req_61 as ShipReq
from gds_helpers import jsonify_xml, jsonify
from lxml import etree
from pydhl.book_pickup_global_req_20 import BookPURequest
from pydhl.modify_pickup_global_req_20 import ModifyPURequest
from pydhl.cancel_pickup_global_req_20 import CancelPURequest
from pydhl.book_pickup_global_res_20 import BookPUResponse
from pydhl.modify_pickup_global_res_20 import ModifyPUResponse
from pydhl import pickupdatatypes_global_20 as PickpuDataTypes

class DHLMapper(Mapper):
    def __init__(self, client: DHLClient):
        self.client = client

    """ Shared functions """

    def init_request(self) -> Request:
        ServiceHeader_ = ServiceHeader(
            MessageReference="1234567890123456789012345678901",
            MessageTime=time.strftime('%Y-%m-%dT%H:%M:%S'),
            SiteID=self.client.site_id,
            Password=self.client.password
        )
        return Request(ServiceHeader=ServiceHeader_)

    def parse_error_response(self, response) -> List[E.Error]:
        conditions = response.xpath(
            './/*[local-name() = $name]', name="Condition")
        return reduce(self._extract_error, conditions, [])

    """ Interface functions """

    def create_quote_request(self, payload: E.shipment_request) -> Req.DCTRequest:
        Request_ = self.init_request()
        Request_.MetaData = MetaData(SoftwareName="3PV", SoftwareVersion="1.0")

        From_ = Req.DCTFrom(
            CountryCode=payload.shipper.country_code,
            Postalcode=payload.shipper.postal_code,
            City=payload.shipper.city,
            Suburb=payload.shipper.state_code
        )

        To_ = Req.DCTTo(
            CountryCode=payload.recipient.country_code,
            Postalcode=payload.recipient.postal_code,
            City=payload.recipient.city,
            Suburb=payload.recipient.state_code
        )

        Pieces = Req.PiecesType()
        default_packaging_type = "FLY" if payload.shipment.is_document else "BOX"
        for index, piece in enumerate(payload.shipment.packages):
            Pieces.add_Piece(Req.PieceType(
                PieceID=piece.id or str(index),
                PackageTypeCode=piece.packaging_type or default_packaging_type,
                Height=piece.height, Width=piece.width,
                Weight=piece.weight, Depth=piece.length
            ))

        payment_country_code = "CA" if not payload.shipment.payment_country_code else payload.shipment.payment_country_code

        BkgDetails_ = Req.BkgDetailsType(
            PaymentCountryCode=payment_country_code,
            NetworkTypeCode=payload.shipment.extra.get('NetworkTypeCode') or "AL",
            WeightUnit=payload.shipment.weight_unit or "LB",
            DimensionUnit=payload.shipment.dimension_unit or "IN",
            ReadyTime=time.strftime("PT%HH%MM"),
            Date=time.strftime("%Y-%m-%d"),
            IsDutiable="N" if payload.shipment.is_document else "Y",
            Pieces=Pieces,
            NumberOfPieces=payload.shipment.number_of_packages,
            ShipmentWeight=payload.shipment.total_weight,
            Volume=payload.shipment.extra.get('Volume'),
            PaymentAccountNumber=payload.shipment.payment_account_number or self.client.account_number,
            InsuredCurrency=payload.shipment.currency or "USD",
            InsuredValue=payload.shipment.insured_amount,
            PaymentType=payload.shipment.extra.get('PaymentType'),
            AcctPickupCloseTime=payload.shipment.extra.get('AcctPickupCloseTime'),
        )

        product_code = "P" if payload.shipment.is_document else "D"
        BkgDetails_.add_QtdShp(Req.QtdShpType(
            GlobalProductCode=product_code,
            LocalProductCode=product_code
        ))

        if payload.shipment.insured_amount is not None:
            BkgDetails_.QtdShp[0].add_QtdShpExChrg(
                Req.QtdShpExChrgType(SpecialServiceType="II")
            )

        if not payload.shipment.is_document:
            BkgDetails_.QtdShp[0].add_QtdShpExChrg(
                Req.QtdShpExChrgType(SpecialServiceType="DD")
            )

        GetQuote = Req.GetQuoteType(
            Request=Request_, 
            From=From_, 
            To=To_, 
            BkgDetails=BkgDetails_,
            Dutiable=Req.Dutiable(
                DeclaredValue=payload.shipment.declared_value,
                DeclaredCurrency=payload.shipment.currency,
                ScheduleB=payload.shipment.extra.get('ScheduleB'),
                ExportLicense=payload.shipment.extra.get('ExportLicense'),
                ShipperEIN=payload.shipment.extra.get('ShipperEIN'),
                ShipperIDType=payload.shipment.extra.get('ShipperIDType'),
                ConsigneeIDType=payload.shipment.extra.get('ConsigneeIDType'),
                ImportLicense=payload.shipment.extra.get('ImportLicense'),
                ConsigneeEIN=payload.shipment.extra.get('ConsigneeEIN'),
                TermsOfTrade=payload.shipment.extra.get('TermsOfTrade'),
                CommerceLicensed=payload.shipment.extra.get('CommerceLicensed'),
                Filing=(lambda filing:
                    Req.Filing(
                        FilingType=filing.get('FilingType'),
                        FTSR=filing.get('FTSR'),
                        ITN=filing.get('ITN'),
                        AES4EIN=filing.get('AES4EIN')
                    )
                )(payload.shipment.extra.get('Filing')) if 'Filing' in payload.shipment.extra else None
            ) if payload.shipment.declared_value is not None else None
        )

        return Req.DCTRequest(schemaVersion="1.0", GetQuote=GetQuote)

    def create_shipment_request(self, payload: E.shipment_request) ->ShipReq.ShipmentRequest:
        Request_ = self.init_request()
        Request_.MetaData = MetaData(SoftwareName="3PV", SoftwareVersion="1.0")

        Billing_ = ShipReq.Billing(
            ShipperAccountNumber=payload.shipper.account_number or self.client.account_number,
            BillingAccountNumber=payload.shipment.payment_account_number,
            ShippingPaymentType=payload.shipment.paid_by,
            DutyAccountNumber=payload.shipment.duty_payment_account,
            DutyPaymentType=payload.shipment.duty_paid_by
        )

        Consignee_ = ShipReq.Consignee(
            CompanyName=payload.recipient.company_name,
            PostalCode=payload.recipient.postal_code,
            CountryCode=payload.recipient.country_code,
            City=payload.recipient.city,
            CountryName=payload.recipient.country_name,
            Division=payload.recipient.state,
            DivisionCode=payload.recipient.state_code
        )

        if any([payload.recipient.person_name, payload.recipient.email_address]):
            Consignee_.Contact = ShipReq.Contact(
                PersonName=payload.recipient.person_name,
                PhoneNumber=payload.recipient.phone_number,
                Email=payload.recipient.email_address,
                FaxNumber=payload.recipient.extra.get('FaxNumber'),
                Telex=payload.recipient.extra.get('Telex'),
                PhoneExtension=payload.recipient.extra.get('PhoneExtension'),
                MobilePhoneNumber=payload.recipient.extra.get('MobilePhoneNumber')
            )

        [Consignee_.add_AddressLine(line)
         for line in payload.recipient.address_lines]

        Shipper_ = ShipReq.Shipper(
            ShipperID=payload.shipment.extra.get('ShipperID') or Billing_.ShipperAccountNumber,
            RegisteredAccount=payload.shipment.extra.get('ShipperID') or Billing_.ShipperAccountNumber,
            CompanyName=payload.shipper.company_name,
            PostalCode=payload.shipper.postal_code,
            CountryCode=payload.shipper.country_code,
            City=payload.shipper.city,
            CountryName=payload.shipper.country_name,
            Division=payload.shipper.state,
            DivisionCode=payload.shipper.state_code
        )

        if any([payload.shipper.person_name, payload.shipper.email_address]):
            Shipper_.Contact = ShipReq.Contact(
                PersonName=payload.shipper.person_name,
                PhoneNumber=payload.shipper.phone_number,
                Email=payload.shipper.email_address,
                FaxNumber=payload.shipper.extra.get('FaxNumber'),
                Telex=payload.shipper.extra.get('Telex'),
                PhoneExtension=payload.shipper.extra.get('PhoneExtension'),
                MobilePhoneNumber=payload.shipper.extra.get('MobilePhoneNumber')
            )

        [Shipper_.add_AddressLine(line)
         for line in payload.shipper.address_lines]

        Pieces_ = ShipReq.Pieces()
        for p in payload.shipment.packages:
            Pieces_.add_Piece(ShipReq.Piece(
                PieceID=p.id,
                PackageType=p.packaging_type,
                Weight=p.weight,
                DimWeight=p.extra.get('DimWeight'),
                Height=p.height,
                Width=p.width,
                Depth=p.length,
                PieceContents=p.description
            ))

        """ 
            Get PackageType from extra when implementing multi carrier,
            Get weight from total_weight if specified otherwise calculated from packages weight sum
        """
        ShipmentDetails_ = ShipReq.ShipmentDetails(
            NumberOfPieces=len(payload.shipment.packages),
            Pieces=Pieces_,
            Weight=payload.shipment.total_weight or sum([p.weight for p in payload.shipment.packages]),
            CurrencyCode=payload.shipment.currency or "USD",
            WeightUnit=(payload.shipment.weight_unit or "LB")[0],
            DimensionUnit=(payload.shipment.dimension_unit or "IN")[0],
            Date=payload.shipment.date or time.strftime('%Y-%m-%d'),
            PackageType=payload.shipment.packaging_type or payload.shipment.extra.get('PackageType'),
            IsDutiable= "N" if payload.shipment.is_document else "Y",
            InsuredAmount=payload.shipment.insured_amount,
            DoorTo=payload.shipment.extra.get('DoorTo'),
            GlobalProductCode=payload.shipment.extra.get('GlobalProductCode'),
            LocalProductCode=payload.shipment.extra.get('LocalProductCode'),
            Contents=payload.shipment.extra.get('Contents') or "..."
        )

        ShipmentRequest_ = ShipReq.ShipmentRequest(
            schemaVersion="6.1",
            Request=Request_,
            RegionCode=payload.shipment.extra.get('RegionCode') or "AM",
            RequestedPickupTime=payload.shipment.extra.get('RequestedPickupTime') or "Y",
            LanguageCode=payload.shipment.extra.get('LanguageCode') or "en",
            PiecesEnabled=payload.shipment.extra.get('PiecesEnabled') or "Y",
            NewShipper=payload.shipment.extra.get('NewShipper'),
            Billing=Billing_,
            Consignee=Consignee_,
            Shipper=Shipper_,
            ShipmentDetails=ShipmentDetails_,
            EProcShip=payload.shipment.extra.get('EProcShip')
        )

        if payload.shipment.label is not None:
            DocImages_ = ShipReq.DocImages()
            Image_ = None if 'Image' not in payload.shipment.label.extra else b64decode(
                payload.shipment.label.extra.get('Image') + '=' * (-len(payload.shipment.label.extra.get('Image')) % 4)
            )
            DocImages_.add_DocImage(ShipReq.DocImage(
                Type=payload.shipment.label.type,
                ImageFormat=payload.shipment.label.format,
                Image=Image_
            ))
            ShipmentRequest_.DocImages = DocImages_

        if ShipmentDetails_.IsDutiable == "Y":
            ShipmentRequest_.Dutiable = ShipReq.Dutiable(
                DeclaredCurrency=ShipmentDetails_.CurrencyCode,
                DeclaredValue=payload.shipment.declared_value,
                TermsOfTrade=payload.shipment.customs.terms_of_trade,
                ScheduleB=payload.shipment.customs.extra.get('ScheduleB'),
                ExportLicense=payload.shipment.customs.extra.get('ExportLicense'),
                ShipperEIN=payload.shipment.customs.extra.get('ShipperEIN'),
                ShipperIDType=payload.shipment.customs.extra.get('ShipperIDType'),
                ImportLicense=payload.shipment.customs.extra.get('ImportLicense'),
                ConsigneeEIN=payload.shipment.customs.extra.get('ConsigneeEIN')
            )

        [ShipmentRequest_.add_SpecialService(
            ShipReq.SpecialService(SpecialServiceType=service)
        ) for service in payload.shipment.services]

        [ShipmentRequest_.add_Commodity(
            ShipReq.Commodity(CommodityCode=c.code, CommodityName=c.description)
        ) for c in payload.shipment.commodities]

        [ShipmentRequest_.add_Reference(
            ShipReq.Reference(ReferenceID=r)
        ) for r in payload.shipment.references]

        return ShipmentRequest_

    def create_tracking_request(self, payload: E.tracking_request) -> Track.KnownTrackingRequest:
        known_request = Track.KnownTrackingRequest(
            Request=self.init_request(),
            LanguageCode=payload.language_code or "en",
            LevelOfDetails=payload.level_of_details or "ALL_CHECK_POINTS"
        )
        for tn in payload.tracking_numbers:
            known_request.add_AWBNumber(tn)
        return known_request

    def create_pickup_request(self, payload: E.pickup_request) -> BookPURequest:
        Requestor_, Place_, PickupContact_, Pickup_ = self._create_pickup_request(payload)

        return BookPURequest(
            Request=self.init_request(),
            schemaVersion="1.0",
            RegionCode=payload.extra.get('RegionCode') or "AM",
            Requestor=Requestor_,
            Place=Place_,
            PickupContact=PickupContact_,
            Pickup=Pickup_
        )

    def modify_pickup_request(self, payload: E.pickup_request) -> ModifyPURequest:
        Requestor_, Place_, PickupContact_, Pickup_ = self._create_pickup_request(payload)

        return ModifyPURequest(
            Request=self.init_request(),
            schemaVersion="1.0",
            RegionCode=payload.extra.get('RegionCode') or "AM",
            ConfirmationNumber=payload.confirmation_number,
            Requestor=Requestor_,
            Place=Place_,
            PickupContact=PickupContact_,
            Pickup=Pickup_,
            OriginSvcArea=payload.extra.get('OriginSvcArea')
        )

    def create_pickup_cancellation_request(self, payload: E.pickup_cancellation_request) -> CancelPURequest:
        return CancelPURequest(
            Request=self.init_request(),
            schemaVersion="2.0",
            RegionCode=payload.extra.get('RegionCode') or "AM",
            ConfirmationNumber=payload.confirmation_number,
            RequestorName=payload.person_name,
            CountryCode=payload.country_code,
            Reason=payload.extra.get('Reason') or "006",
            PickupDate=payload.pickup_date,
            CancelTime=time.strftime('%H:%M')
        )

    def parse_quote_response(self, response) -> Tuple[List[E.QuoteDetails], List[E.Error]]:
        qtdshp_list = response.xpath(
            './/*[local-name() = $name]', name="QtdShp")
        quotes = reduce(self._extract_quote, qtdshp_list, [])
        return (quotes, self.parse_error_response(response))

    def parse_tracking_response(self, response) -> Tuple[List[E.TrackingDetails], List[E.Error]]:
        awbinfos = response.xpath('.//*[local-name() = $name]', name="AWBInfo")
        trackings = reduce(self._extract_tracking, awbinfos, [])
        return (trackings, self.parse_error_response(response))

    def parse_shipment_response(self, response) -> Tuple[E.ShipmentDetails, List[E.Error]]:
        return (self._extract_shipment(response), self.parse_error_response(response))

    def parse_pickup_response(self, response) -> Tuple[E.PickupDetails, List[E.Error]]:
        ConfirmationNumbers = response.xpath('.//*[local-name() = $name]', name="ConfirmationNumber")
        success = len(ConfirmationNumbers) > 0
        if success:
            pickup = BookPUResponse() if 'BookPUResponse' in response.tag else ModifyPUResponse()
            pickup.build(response)
        return (
            self._extract_pickup(pickup) if success else None, 
            self.parse_error_response(response) if not success else []
        )

    def parse_pickup_cancellation_response(self, response) -> Tuple[dict, List[E.Error]]:
        ConfirmationNumbers = response.xpath('.//*[local-name() = $name]', name="ConfirmationNumber")
        success = len(ConfirmationNumbers) > 0
        if success:
            cancellation = dict(
                confirmation_number=response.xpath('.//*[local-name() = $name]', name="ConfirmationNumber")[0].text
            )
        return (
            cancellation if success else None,
            self.parse_error_response(response) if not success else []
        )

    """ Helpers functions """

    def _extract_error(self, errors: List[E.Error], conditionNode) -> List[E.Error]:
        condition = Res.ConditionType()
        condition.build(conditionNode)
        return errors + [
            E.Error(code=condition.ConditionCode,
                    message=condition.ConditionData, carrier=self.client.carrier_name)
        ]

    def _extract_quote(self, quotes: List[E.QuoteDetails], qtdshpNode) -> List[E.QuoteDetails]:
        qtdshp = Res.QtdShpType()
        qtdshp.build(qtdshpNode)
        ExtraCharges = list(map(lambda s: E.ChargeDetails(
            name=s.LocalServiceTypeName, amount=float(s.ChargeValue or 0)), qtdshp.QtdShpExChrg))
        Discount_ = reduce(
            lambda d, ec: d + ec.value if "Discount" in ec.name else d, ExtraCharges, 0)
        DutiesAndTaxes_ = reduce(
            lambda d, ec: d + ec.value if "TAXES PAID" in ec.name else d, ExtraCharges, 0)
        return quotes + [
            E.QuoteDetails(
                carrier=self.client.carrier_name,
                currency=qtdshp.CurrencyCode,
                delivery_date=str(qtdshp.DeliveryDate[0].DlvyDateTime),
                pickup_date=str(qtdshp.PickupDate),
                pickup_time=str(qtdshp.PickupCutoffTime),
                service_name=qtdshp.LocalProductName,
                service_type=qtdshp.NetworkTypeCode,
                base_charge=float(qtdshp.WeightCharge or 0),
                total_charge=float(qtdshp.ShippingCharge or 0),
                duties_and_taxes=DutiesAndTaxes_,
                discount=Discount_,
                extra_charges=list(map(lambda s: E.ChargeDetails(
                    name=s.LocalServiceTypeName, amount=float(s.ChargeValue or 0)), qtdshp.QtdShpExChrg))
            )
        ]

    def _extract_tracking(self, trackings: List[E.TrackingDetails], awbInfoNode) -> List[E.TrackingDetails]:
        awbInfo = TrackRes.AWBInfo()
        awbInfo.build(awbInfoNode)
        if awbInfo.ShipmentInfo == None:
            return trackings
        return trackings + [
            E.TrackingDetails(
                carrier=self.client.carrier_name,
                tracking_number=awbInfo.AWBNumber,
                shipment_date=str(awbInfo.ShipmentInfo.ShipmentDate),
                events=list(map(lambda e: E.TrackingEvent(
                    date=str(e.Date),
                    time=str(e.Time),
                    signatory=e.Signatory,
                    code=e.ServiceEvent.EventCode,
                    location=e.ServiceArea.Description,
                    description=e.ServiceEvent.Description
                ), awbInfo.ShipmentInfo.ShipmentEvent))
            )
        ]

    def _extract_shipment(self, shipmentResponseNode) -> E.ShipmentDetails:
        """
            Shipment extraction is implemented using lxml queries instead of generated ShipmentResponse type
            because the type construction fail during validation out of our control
        """
        get_value = lambda query: query[0].text if len(query) > 0 else None
        get = lambda key: get_value(shipmentResponseNode.xpath("//%s" % key))
        tracking_number = get("AirwayBillNumber")
        if tracking_number == None:
            return None
        plates = [p.text for p in shipmentResponseNode.xpath("//LicensePlateBarCode")]
        barcodes = [child.text for child in shipmentResponseNode.xpath("//Barcodes")[0].getchildren()]
        documents = reduce(lambda r,i: (r + [i] if i else r), [get("AWBBarCode")] + plates + barcodes, [])
        reference = E.ReferenceDetails(value=get("ReferenceID"), type=get("ReferenceType")) if len(shipmentResponseNode.xpath("//Reference")) > 0 else None
        currency_ = get("CurrencyCode")
        return E.ShipmentDetails(
            carrier=self.client.carrier_name,
            tracking_numbers=[tracking_number],
            shipment_date= get("ShipmentDate"),
            services=(
                [get("ProductShortName")] +
                [service.text for service in shipmentResponseNode.xpath("//SpecialServiceDesc")] +
                [service.text for service in shipmentResponseNode.xpath("//InternalServiceCode")]
            ),
            charges=[
                E.ChargeDetails(name="PackageCharge", amount=float(get("PackageCharge")), currency=currency_) 
            ],
            documents=documents,
            reference=reference,
            total_charge= E.ChargeDetails(name="Shipment charge", amount=get("ShippingCharge"), currency=currency_)
        )

    def _extract_pickup(self, pickup: Union[BookPUResponse, ModifyPURequest]) -> E.PickupDetails:
        pickup_charge = None if pickup.PickupCharge is None else E.ChargeDetails(
            name="Pickup Charge", amount=pickup.PickupCharge, currency=pickup.CurrencyCode
        )
        ref_times = (
            ([] if pickup.ReadyByTime is None else [E.TimeDetails(name="ReadyByTime", value=pickup.ReadyByTime)]) +
            ([] if pickup.CallInTime is None else [E.TimeDetails(name="CallInTime", value=pickup.CallInTime)])
        )
        return E.PickupDetails(
            carrier=self.client.carrier_name,
            confirmation_number=pickup.ConfirmationNumber,
            pickup_date=pickup.NextPickupDate,
            pickup_charge=pickup_charge,
            ref_times=ref_times
        )


    """ Private functions """

    def _create_pickup_request(self, payload: E.pickup_request) -> Tuple[
            PickpuDataTypes.Requestor,
            PickpuDataTypes.Place,
            PickpuDataTypes.Contact,
            PickpuDataTypes.Pickup
        ]:
        RequestorContact_ = None if "RequestorContact" not in payload.extra else PickpuDataTypes.RequestorContact(
            PersonName=payload.extra.get("RequestorContact").get("PersonName"),
            Phone=payload.extra.get("RequestorContact").get("Phone"),
            PhoneExtension=payload.extra.get("RequestorContact").get("PhoneExtension")
        )

        Requestor_ = PickpuDataTypes.Requestor(
            AccountNumber=payload.account_number,
            AccountType=payload.extra.get("AccountType") or "D",
            RequestorContact=RequestorContact_,
            CompanyName=payload.extra.get("CompanyName")
        )

        Place_ = PickpuDataTypes.Place(
            City=payload.city,
            StateCode=payload.state_code,
            PostalCode=payload.postal_code,
            CompanyName=payload.company_name,
            CountryCode=payload.country_code,
            PackageLocation=payload.package_location or "...",
            LocationType="B" if payload.is_business else "R",
            Address1=payload.address_lines[0] if len(payload.address_lines) > 0 else None,
            Address2=payload.address_lines[1] if len(payload.address_lines) > 1 else None
        )

        PickupContact_ = PickpuDataTypes.Contact(
            PersonName=payload.person_name,
            Phone=payload.phone_number
        )

        weight_ = PickpuDataTypes.WeightSeg(Weight=payload.weight, WeightUnit=payload.weight_unit) if any([payload.weight, payload.weight_unit]) else None

        Pickup_ = PickpuDataTypes.Pickup(
            Pieces=payload.pieces,
            PickupDate=payload.date,
            ReadyByTime=payload.ready_time,
            CloseTime=payload.closing_time,
            SpecialInstructions=payload.instruction,
            RemotePickupFlag=payload.extra.get("RemotePickupFlag"),
            weight=weight_
        )

        return Requestor_, Place_, PickupContact_, Pickup_