"""PurplShip Australia post rate mapper module."""

from functools import reduce
from typing import List, Tuple
from .interface import AustraliaPostMapperBase
from purplship.domain.Types import (
    Error,
    ChargeDetails,
    ShipmentRequest,
    QuoteDetails
)
from pyaups.shipping_price_response import (
    ShippingPriceResponse,
    Shipment as ResponseShipment,
    ShipmentSummary
)
from pyaups.shipping_price_request import (
    ShippingPriceRequest,
    Shipment,
    From,
    To,
    Item
)


class AustraliaPostMapperPartial(AustraliaPostMapperBase):
    def parse_shipping_price_response(
        self, response: dict
    ) -> Tuple[List[QuoteDetails], List[Error]]:
        def prune(s: dict) -> dict:
            s['from_'] = s.pop('from')
            return s
        clean_response = {
            **response,
            **{"shipments": [prune(s) for s in response.get('shipments', [])]}
        }
        price_response: ShippingPriceResponse = ShippingPriceResponse(**clean_response)
        return (
            reduce(self._extract_quote, price_response.shipments, []),
            self.parse_error_response(response)
        )

    def _extract_quote(
        self, quotes: List[QuoteDetails], shipping_price: ResponseShipment
    ) -> List[QuoteDetails]:
        summary = shipping_price.shipment_summary or ShipmentSummary()
        return quotes + [
            QuoteDetails(
                carrier=self.client.carrier_name,
                service_name=None,
                service_type=None,
                base_charge=summary.total_cost_ex_gst,
                duties_and_taxes=summary.total_gst,
                total_charge=summary.total_cost,
                currency="AUD",
                delivery_date=None,
                discount=summary.discount,
                extra_charges=(
                    [ChargeDetails(
                        name='Fuel', amount=summary.fuel_surcharge
                    )] if summary.fuel_surcharge is not None else [] +
                    [ChargeDetails(
                        name='Security', amount=summary.security_surcharge
                    )] if summary.security_surcharge is not None else [] +
                    [ChargeDetails(
                        name='Transit', amount=summary.transit_cover
                    )] if summary.transit_cover is not None else [] +
                    [ChargeDetails(
                        name='Freight', amount=summary.freight_charge
                    )] if summary.freight_charge is not None else []
                )
            )
        ]

    def create_shipping_price_request(self, payload: ShipmentRequest) -> ShippingPriceRequest:
        return ShippingPriceRequest(
            shipments=[
                Shipment(
                    shipment_reference=" ".join(payload.shipment.references),
                    sender_references=None,
                    goods_descriptions=None,
                    despatch_date=payload.shipment.date,
                    consolidate=None,
                    email_tracking_enabled=payload.shipment.extra.get('email_tracking_enabled'),
                    from_=From(
                        name=payload.shipper.person_name,
                        type=None,
                        lines=payload.shipper.address_lines,
                        suburb=payload.shipper.suburb,
                        state=payload.shipper.state_code,
                        postcode=payload.shipper.postal_code,
                        country=payload.shipper.country_code,
                        phone=payload.shipper.phone_number,
                        email=payload.shipper.email_address
                    ),
                    to=To(
                        name=payload.recipient.person_name,
                        business_name=payload.recipient.company_name,
                        type=None,
                        lines=payload.recipient.address_lines,
                        suburb=payload.recipient.suburb,
                        state=payload.recipient.state_code,
                        postcode=payload.recipient.postal_code,
                        country=payload.recipient.country_code,
                        phone=payload.recipient.phone_number,
                        email=payload.recipient.email_address,
                        delivery_instructions=None
                    ),
                    dangerous_goods=None,
                    movement_type=None,
                    features=None,
                    authorisation_number=None,
                    items=[
                        Item(
                            item_reference=item.sku,
                            product_id=item.id,
                            item_description=item.description,
                            length=item.length,
                            width=item.width,
                            height=item.height,
                            cubic_volume=None,
                            weight=item.weight,
                            contains_dangerous_goods=None,
                            transportable_by_air=None,
                            dangerous_goods_declaration=None,
                            authority_to_leave=item.extra.get('authority_to_leave'),
                            reason_for_return=None,
                            allow_partial_delivery=item.extra.get('allow_partial_delivery'),
                            packaging_type=item.packaging_type,
                            atl_number=None,
                            features=None,
                            tracking_details=None,
                            commercial_value=None,
                            export_declaration_number=None,
                            import_reference_number=None,
                            classification_type=None,
                            description_of_other=None,
                            international_parcel_sender_name=None,
                            non_delivery_action=None,
                            certificate_number=None,
                            licence_number=None,
                            invoice_number=None,
                            comments=None,
                            tariff_concession=None,
                            free_trade_applicable=None
                        ) for item in payload.shipment.items
                    ]
                )
            ]
        )
