from pyusps import (
    ratev4request as Rate,
    intlratev2request as IntlRate,
    ratev4response as RateRes,
    intlratev2response as IntlRateRes
)
from .interface import reduce, Tuple, List, T, USPSMapperBase


class USPSMapperPartial(USPSMapperBase):
    
    def parse_rate_response(self, response: 'XMLElement') -> Tuple[List[T.QuoteDetails], List[T.Error]]:
        pass

    def _extract_quote(self, quotes: List[T.QuoteDetails], price_quoteNode: 'XMLElement') -> List[T.QuoteDetails]: 
        pass


    def create_rate_request(self, payload: T.shipment_request) -> Rate.RateV4Request:
        weight_unit = payload.shipment.weight_unit or "LB"
        return Rate.RateV4Request(
            USERID=self.client.username,
            Revision=None,
            Package=[
               Rate.PackageType(
                   ID=item.id or index,
                   Service=payload.shipment.service_type,
                   FirstClassMailType=None,
                   ZipOrigination=payload.shipper.postal_code,
                   ZipDestination=payload.recipient.postal_code,
                   Pounds=item.weight if weight_unit == "LB" else item.weight * 2.20462,
                   Ounces=None,
                   Container=None,
                   Size=None,
                   Width=item.width,
                   Length=item.length,
                   Height=item.height,
                   Girth=None,
                   Content=None,
                   Machinable=None
                ) for index, item in enumerate(payload.shipment.items)
            ]
        )

    def create_intl_rate_request(self, payload: T.shipment_request) -> IntlRate.IntlRateV2Request:
        return IntlRate.IntlRateV2Request(
            USERID=self.client.username,
            Revision=None,
            Package=[
                IntlRate.PackageType(
                    ID=None,
                    Pounds=None,
                    Ounces=None,
                    Machinable=None,
                    MailType=None,
                    GXG=None,
                    ValueOfContents=None,
                    Country=None,
                    Container=None,
                    Size=None,
                    Width=None,
                    Length=None,
                    Height=None,
                    Girth=None,
                    OriginZip=None,
                    CommercialFlag=None,
                    AcceptanceDateTime=None,
                    DestinationPostalCode=None,
                    ExtraServices=None
                ) for item in payload.shipment.items
            ]
        )