from pyaramex.Rating import (
    RateCalculatorRequest,
    Address,
    ShipmentDetails,
    ShipmentItem,
    ArrayOfShipmentItem
)
from .interface import reduce, Tuple, List, T, AramexMapperBase


class AramexMapperPartial(AramexMapperBase):
    
    def parse_shipment_tracking_response(self, response: 'XMLElement') -> Tuple[List[T.QuoteDetails], List[T.Error]]:
        pass

    def _extract_quote(self, quotes: List[T.QuoteDetails], price_quoteNode: 'XMLElement') -> List[T.QuoteDetails]: 
        pass

    def create_rate_calculator_request(self, payload: T.shipment_request) -> RateCalculatorRequest:
        return RateCalculatorRequest(
            ClientInfo=self.client_info,
            Transaction=None,
            OriginAddress=Address(
                Line1=payload.shipper.address_lines[0],
                Line2=payload.shipper.address_lines[0] if len(payload.shipper.address_lines) > 1 else None,
                Line3=payload.shipper.address_lines[0] if len(payload.shipper.address_lines) > 2 else None,
                City=payload.shipper.city,
                StateOrProvinceCode=payload.shipper.state_code,
                PostCode=payload.shipper.postal_code,
                CountryCode=payload.shipper.country_code
            ),
            DestinationAddress=Address(
                Line1=payload.recipient.address_lines[0],
                Line2=payload.recipient.address_lines[0] if len(payload.recipient.address_lines) > 1 else None,
                Line3=payload.recipient.address_lines[0] if len(payload.recipient.address_lines) > 2 else None,
                City=payload.recipient.city,
                StateOrProvinceCode=payload.recipient.state_code,
                PostCode=payload.recipient.postal_code,
                CountryCode=payload.recipient.country_code
            ),
            ShipmentDetails=ShipmentDetails(
                Dimensions=None,
                ActualWeight=payload.shipment.total_weight,
                ChargeableWeight=None,
                DescriptionOfGoods=None,
                GoodsOriginCountry=None,
                NumberOfPieces=payload.shipment.total_items,
                ProductGroup=None,
                ProductType=None,
                PaymentType=None,
                PaymentOptions=None,
                CustomsValueAmount=None,
                CashOnDeliveryAmount=None,
                InsuranceAmount=None,
                CashAdditionalAmount=None,
                CollectAmount=None,
                Services=None,
                Items=ArrayOfShipmentItem(
                    ShipmentItem=[
                        ShipmentItem(
                            PackageType=item.packaging_type,
                            Quantity=item.quantity,
                            Weight=item.weight,
                            Comments=item.description,
                            Reference=item.content
                        ) for item in payload.shipment.items
                    ]
                )
            )
        )