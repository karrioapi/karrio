from typing import List, Tuple
from functools import reduce
import time
from ...domain import entities as E 
from ...domain.mapper import Mapper
from .dhl_client import DHLClient
from pydhl import DCT_req_global as Req, DCT_Response_global as Res, tracking_request_known as Track, tracking_response as TrackRes
from pydhl.datatypes_global_v61 import ServiceHeader, MetaData, Request

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


    def parse_error_response(self, response):
        return reduce(self._extract_error, response.findall('.//Condition'), [])


    """ Interface functions """
    def create_quote_request(self, payload: E.quote_request) -> Req.DCTRequest:
        Request_ = self.init_request()
        Request_.MetaData = MetaData(SoftwareName="3PV", SoftwareVersion="1.0")

        From_ = Req.DCTFrom(
            CountryCode=payload.shipper.address.country_code, 
            Postalcode=payload.shipper.address.postal_code,
            City=payload.shipper.address.city,
            Suburb=payload.shipper.address.state_or_province
        )

        To_ = Req.DCTTo(
            CountryCode=payload.recipient.address.country_code, 
            Postalcode=payload.recipient.address.postal_code,
            City=payload.recipient.address.city,
            Suburb=payload.recipient.address.state_or_province
        )

        Pieces = Req.PiecesType()
        for p in payload.shipment_details.packages:
            Pieces.add_Piece(Req.PieceType(
                PieceID=p.id, 
                PackageTypeCode=p.packaging_type, 
                Height=p.height, Width=p.width,
                Weight=p.weight, Depth=p.lenght
            ))

        payment_country_code = "CA" if not payload.shipment_details.payment_country_code else payload.shipment_details.payment_country_code

        BkgDetails_ = Req.BkgDetailsType(
            PaymentCountryCode=payment_country_code, 
            NetworkTypeCode="AL", 
            WeightUnit=payload.shipment_details.weight_unit, 
            DimensionUnit=payload.shipment_details.dimension_unit,
            ReadyTime=time.strftime("PT%HH%MM"),
            Date=time.strftime("%Y-%m-%d"), 
            PaymentAccountNumber=self.client.account_number,
            IsDutiable=payload.shipment_details.is_dutiable,
            Pieces=Pieces
        )

        GetQuote = Req.GetQuoteType(Request=Request_, From=From_, To=To_, BkgDetails=BkgDetails_)
        
        return Req.DCTRequest(GetQuote=GetQuote)


    def create_tracking_request(self, payload: E.tracking_request) -> Track.KnownTrackingRequest:
        known_request = Track.KnownTrackingRequest(
            Request=self.init_request(),
            LanguageCode= payload.language_code or "en",
            LevelOfDetails= payload.level_of_details or "ALL_CHECK_POINTS"
        )
        for tn in payload.tracking_numbers:
            known_request.add_AWBNumber(tn)
        return known_request


    def parse_quote_response(self, response) -> Tuple[List[E.quote_details], List[E.Error]]:
        quotes = reduce(self._extract_quote, response.findall('.//QtdShp'), [])
        return (quotes, self.parse_error_response(response))


    def parse_tracking_response(self, response) -> Tuple[List[E.tracking_details], List[E.Error]]:
        trackings = reduce(self._extract_tracking, response.findall('.//AWBInfo'), [])
        return (trackings, self.parse_error_response(response))



    """ Helpers functions """
    def _extract_error(self, errors: List[E.Error], conditionNode) -> List[E.Error]:
        condition = Res.ConditionType()
        condition.build(conditionNode)
        return errors + [
            E.Error(code=condition.ConditionCode, message=condition.ConditionData, carrier=self.client.carrier_name)
        ]


    def _extract_quote(self, quotes: List[E.quote_details], qtdshpNode) -> List[E.quote_details]:
        qtdshp = Res.QtdShpType()
        qtdshp.build(qtdshpNode)
        ExtraCharges=list(map(lambda s: E.Charge(name=s.LocalServiceTypeName, value=float(s.ChargeValue)), qtdshp.QtdShpExChrg))
        Discount_ = reduce(lambda d, ec: d + ec.value if "Discount" in ec.name else d, ExtraCharges, 0)
        DutiesAndTaxes_ = reduce(lambda d, ec: d + ec.value if "TAXES PAID" in ec.name else d, ExtraCharges, 0)
        return quotes + [
            E.Quote.parse(
                carrier=self.client.carrier_name, 
                delivery_date = str(qtdshp.DeliveryDate[0].DlvyDateTime),
                delivery_time = str(qtdshp.DeliveryTime),
                pickup_date = str(qtdshp.PickupDate),
                pickup_time = str(qtdshp.PickupCutoffTime),
                service_name=qtdshp.LocalProductName,
                service_type=qtdshp.NetworkTypeCode,
                base_charge=float(qtdshp.WeightCharge),
                total_charge=float(qtdshp.ShippingCharge),
                duties_and_taxes=DutiesAndTaxes_,
                discount=Discount_,
                extra_charges=list(map(lambda s: E.Charge(name=s.LocalServiceTypeName, value=float(s.ChargeValue)), qtdshp.QtdShpExChrg))
            )
        ]


    def _extract_tracking(self, trackings: List[E.tracking_details], awbInfoNode) -> List[E.tracking_details]:
        awbInfo = TrackRes.AWBInfo()
        awbInfo.build(awbInfoNode)
        return trackings + [
            E.Tracking.parse(
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