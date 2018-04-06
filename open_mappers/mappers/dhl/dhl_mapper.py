from typing import List, Tuple
from functools import reduce
import time
from pydhl import DCT_req_global as Request, DCT_Response_global as Response
from ...domain import entities as E 
from ...domain.mapper import Mapper
from .dhl_client import DHLClient

class DHLMapper(Mapper):
    def __init__(self, client: DHLClient):
        self.client = client

    def quote_request(self, payload: E.QuoteRequest) -> Request.DCTRequest:
        Request_ = self.client.initRequest()

        From_ = Request.DCTFrom(
            CountryCode=payload.Shipper.Address.CountryCode, 
            Postalcode=payload.Shipper.Address.PostalCode,
            City=payload.Shipper.Address.City,
            Suburb=payload.Shipper.Address.StateOrProvince
        )

        To_ = Request.DCTTo(
            CountryCode=payload.Recipient.Address.CountryCode, 
            Postalcode=payload.Recipient.Address.PostalCode,
            City=payload.Recipient.Address.City,
            Suburb=payload.Recipient.Address.StateOrProvince
        )

        Pieces = Request.PiecesType()
        for p in payload.ShipmentDetails.Packages:
            Pieces.add_Piece(Request.PieceType(
                PieceID=p.Id, 
                PackageTypeCode=p.PackagingType, 
                Height=p.Height, Width=p.Width,
                Weight=p.Weight, Depth=p.Lenght
            ))

        BkgDetails_ = Request.BkgDetailsType(
            PaymentCountryCode="CA", NetworkTypeCode="AL", 
            WeightUnit=payload.ShipmentDetails.WeightUnit, 
            DimensionUnit=payload.ShipmentDetails.DimensionUnit,
            ReadyTime=time.strftime("PT%HH%MM"),
            Date=time.strftime("%Y-%m-%d"), 
            PaymentAccountNumber=self.client.account_number,
            IsDutiable=payload.ShipmentDetails.IsDutiable,
            Pieces=Pieces
        )

        GetQuote = Request.GetQuoteType(Request=Request_, From=From_, To=To_, BkgDetails=BkgDetails_)
        
        return Request.DCTRequest(schemaVersion="1.0", GetQuote=GetQuote)

    def quote_response(self, res: Response.DCTResponse) -> Tuple[List[E.Quote], List[E.Error]]:
        quotes = reduce(extractDetails, res.GetQuoteResponse.BkgDetails, [])
        errors = []
        return (quotes, errors)


def extractDetails(quotes: List[E.Quote], detail: Response.BkgDetailsType): 
    return quotes + reduce(extractQuote, detail.QtdShp, [])

def extractQuote(quotes: List[E.Quote], qtdshp: Response.QtdShpType) -> List[E.Quote]:
    if not qtdshp.QtdShpExChrg:
        return quotes
    ExtraCharges=list(map(lambda s: E.Charge(Name=s.LocalServiceTypeName, Value=float(s.ChargeValue)), qtdshp.QtdShpExChrg))
    Discount_ = reduce(lambda d, ec: d + ec.Value if "Discount" in ec.Name else d, ExtraCharges, 0)
    DutiesAndTaxes_ = reduce(lambda d, ec: d + ec.Value if "TAXES PAID" in ec.Name else d, ExtraCharges, 0)
    return quotes + [
        E.Quote(
            Provider="DHL", 
            ServiceName=qtdshp.LocalProductName,
            ServiceType=qtdshp.NetworkTypeCode,
            BaseCharge=float(qtdshp.WeightCharge),
            TotalCharge=float(qtdshp.ShippingCharge),
            DutiesAndTaxes=DutiesAndTaxes_,
            Discount=Discount_,
            ExtraCharges=list(map(lambda s: E.Charge(Name=s.LocalServiceTypeName, Value=float(s.ChargeValue)), qtdshp.QtdShpExChrg))
        )
    ]