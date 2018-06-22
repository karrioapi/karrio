from typing import List, Tuple
from functools import reduce
import time
from ...domain import entities as E 
from ...domain.mapper import Mapper
from .dhl_client import DHLClient
from pydhl import DCT_req_global as Req, DCT_Response_global as Res
from pydhl.datatypes_global_v61 import ServiceHeader, MetaData, Request

class DHLMapper(Mapper):
    def __init__(self, client: DHLClient):
        self.client = client

    def init_request(self) -> Request:
        ServiceHeader_ = ServiceHeader(
            MessageReference="1234567890123456789012345678901",
            MessageTime=time.strftime('%Y-%m-%dT%H:%M:%S'),
            SiteID=self.client.site_id, 
            Password=self.client.password
        )
        MetaData_ = MetaData(SoftwareName="3PV", SoftwareVersion="1.0")
        return Request(ServiceHeader=ServiceHeader_, MetaData=MetaData_)



    def create_quote_request(self, payload: E.quote_request) -> Req.DCTRequest:
        Request_ = self.init_request()

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



    def parse_quote_response(self, response) -> Tuple[List[E.quote_details], List[E.Error]]:
        quotes = reduce(self._extract_quote, response.findall('.//QtdShp'), [])
        errors = reduce(self._extract_error, response.findall('.//Condition'), [])
        return (quotes, errors)




    """ Helpers functions """
    def _extract_error(self, errors: List[E.Error], conditionNode: Res.ConditionType) -> List[E.Error]:
        condition = Res.ConditionType()
        condition.build(conditionNode)
        return errors + [
            E.Error(code=condition.ConditionCode, message=condition.ConditionData, carrier=self.client.carrier_name)
        ]


    def _extract_quote(self, quotes: List[E.quote_details], qtdshpNode: Res.QtdShpType) -> List[E.quote_details]:
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