from typing import List, Tuple
from functools import reduce
import time
from purplship.domain import entities as E
from purplship.domain.mapper import Mapper

from purplship.mappers.caps.caps_client import CanadaPostClient

from pycaps import rating as Rate, track as Track, messages as Msg


class CanadaPostMapper(Mapper):
    def __init__(self, client: CanadaPostClient):
        self.client = client

    """ Shared functions """

    def parse_error_response(self, response) -> List[E.Error]:
        messages = response.xpath('.//*[local-name() = $name]', name="message")
        return reduce(self._extract_error, messages, [])

    """ Interface functions """

    def create_quote_request(self, payload: E.quote_request) -> Rate.mailing_scenario:
        package = payload.shipment.packages[0]
        parcel = Rate.parcel_characteristicsType(
            weight=package.weight,
            dimensions=Rate.dimensionsType(
                length=package.length,
                width=package.width,
                height=package.height
            )
        )
        destinationPostalCode = Rate.domesticType(
            postal_code=payload.recipient.postal_code)
        destination = Rate.destinationType(
            domestic=destinationPostalCode)
        return Rate.mailing_scenario(
            customer_number=self.client.customer_number,
            parcel_characteristics=parcel,
            origin_postal_code=payload.shipper.postal_code,
            destination=destination
        )

    def create_tracking_request(self, payload: E.tracking_request) -> List[str]:
        return payload.tracking_numbers

    def parse_quote_response(self, response) -> Tuple[List[E.QuoteDetails], List[E.Error]]:
        price_quotes = response.xpath('.//*[local-name() = $name]', name="price-quote")
        quotes = reduce(self._extract_quote, price_quotes, [])
        return (quotes, self.parse_error_response(response))

    def parse_tracking_response(self, response) -> Tuple[List[E.TrackingDetails], List[E.Error]]:
        pin_summaries = response.xpath('.//*[local-name() = $name]', name="pin-summary")
        trackings = reduce(self._extract_tracking, pin_summaries, [])
        return (trackings, self.parse_error_response(response))

    """ Helpers functions """

    def _extract_error(self, errors: List[E.Error], messageNode) -> List[E.Error]:
        message = Msg.messageType()
        message.build(messageNode)
        return errors + [
            E.Error(code=message.code,
                    message=message.description, carrier=self.client.carrier_name)
        ]

    def _extract_quote(self, quotes: List[E.QuoteDetails], price_quoteNode) -> List[E.QuoteDetails]:
        price_quote = Rate.price_quoteType()
        price_quote.build(price_quoteNode)
        discounts = [E.ChargeDetails(name=d.adjustment_name, currency="CAD", amount=float(d.adjustment_cost or 0)) for d in price_quote.price_details.adjustments.adjustment]
        return quotes + [
            E.QuoteDetails(
                carrier=self.client.carrier_name,
                currency="CAD",
                delivery_date=str(price_quote.service_standard.expected_delivery_date),
                service_name=price_quote.service_name,
                service_type=price_quote.service_code,
                base_charge=float(price_quote.price_details.base or 0),
                total_charge=float(price_quote.price_details.due or 0),
                discount=reduce(lambda sum, d: sum + d.amount, discounts, 0),
                duties_and_taxes=float(price_quote.price_details.taxes.gst.valueOf_ or 0) + 
                    float(price_quote.price_details.taxes.pst.valueOf_ or 0) + 
                    float(price_quote.price_details.taxes.hst.valueOf_ or 0),
                extra_charges=list(map(lambda a: E.ChargeDetails(
                    name=a.adjustment_name, currency="CAD", amount=float(a.adjustment_cost or 0)), price_quote.price_details.adjustments.adjustment)
                )
            )
        ]

    def _extract_tracking(self, trackings: List[E.TrackingDetails], pin_summaryNode) -> List[E.TrackingDetails]:
        pin_summary = Track.pin_summary()
        pin_summary.build(pin_summaryNode)
        return trackings + [
            E.TrackingDetails(
                carrier=self.client.carrier_name,
                tracking_number=pin_summary.pin,
                shipment_date=str(pin_summary.mailed_on_date),
                events=[E.TrackingEvent(
                    date=str(pin_summary.event_date_time),
                    signatory=pin_summary.signatory_name,
                    code=pin_summary.event_type,
                    location=pin_summary.event_location,
                    description=pin_summary.event_description
                )]
            )
        ]
