from typing import List, Tuple, Union
from functools import reduce
import time
from purplship.domain import entities as E
from purplship.domain.mapper import Mapper

from purplship.mappers.caps.caps_client import CanadaPostClient

from pycaps import rating as Rate, track as Track, messages as Msg
from pycaps import shipment as Shipment
from pycaps import ncshipment as NCShipment


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
        
        if len(payload.shipment.services) > 0:
            services = Rate.servicesType()
            for code in payload.shipment.services:
                services.add_service_code(code)

        if 'options' in payload.shipment.extra:
            options = Rate.optionsType()
            for option in payload.shipment.extra.get('options'):
                options.add_option(Rate.optionType(
                    option_amount=option.get('option-amount'),
                    option_code=option.get('option-code')
                ))

        return Rate.mailing_scenario(
            customer_number=payload.shipment.shipper_account_number or payload.shipment.payment_account_number or self.client.customer_number,
            contract_id=payload.shipment.extra.get('contract-id'),
            promo_code=payload.shipment.extra.get('promo-code'),
            quote_type=payload.shipment.extra.get('quote-type'),
            expected_mailing_date=payload.shipment.extra.get('expected-mailing-date'),
            options=options if ('options' in payload.shipment.extra) else None,
            parcel_characteristics=Rate.parcel_characteristicsType(
                weight=payload.shipment.total_weight or package.weight,
                dimensions=Rate.dimensionsType(
                    length=package.length,
                    width=package.width,
                    height=package.height
                ),
                unpackaged=payload.shipment.extra.get('unpackaged'),
                mailing_tube=payload.shipment.extra.get('mailing-tube'),
                oversized=payload.shipment.extra.get('oversized')
            ),
            services=services if (len(payload.shipment.services) > 0) else None,
            origin_postal_code=payload.shipper.postal_code,
            destination=Rate.destinationType(
                domestic=Rate.domesticType(
                    postal_code=payload.recipient.postal_code
                ) if (payload.recipient.country_code == 'CA') else None,
                united_states=Rate.united_statesType(
                    zip_code=payload.recipient.postal_code
                ) if (payload.recipient.country_code == 'US') else None,
                international=Rate.internationalType(
                    country_code=payload.shipment.country_code
                ) if (payload.recipient.country_code not in ['US', 'CA']) else None
            )
        )

    def create_tracking_request(self, payload: E.tracking_request) -> List[str]:
        return payload.tracking_numbers

    def create_shipment_request(self, payload: E.shipment_request) -> Union[Shipment.ShipmentType, NCShipment.NonContractShipmentType]:
        is_non_contract = payload.shipment.extra.get('settlement-info') is None
        shipment = self._create_ncshipment(payload) if is_non_contract else self._create_shipment(payload)
        return shipment


    """ Mapper Interface parsing methods """

    def parse_quote_response(self, response: 'XMLElement') -> Tuple[List[E.QuoteDetails], List[E.Error]]:
        price_quotes = response.xpath('.//*[local-name() = $name]', name="price-quote")
        quotes = reduce(self._extract_quote, price_quotes, [])
        return (quotes, self.parse_error_response(response))

    def parse_tracking_response(self, response: 'XMLElement') -> Tuple[List[E.TrackingDetails], List[E.Error]]:
        pin_summaries = response.xpath('.//*[local-name() = $name]', name="pin-summary")
        trackings = reduce(self._extract_tracking, pin_summaries, [])
        return (trackings, self.parse_error_response(response))

    def parse_shipment_response(self, response: 'XMLElement') -> Tuple[E.ShipmentDetails, List[E.Error]]:
        shipment = self._extract_shipment(response) if len(response.xpath('.//*[local-name() = $name]', name="shipment-id")) > 0 else None
        return (shipment, self.parse_error_response(response))

    """ Helpers functions """

    def _extract_error(self, errors: List[E.Error], messageNode: 'XMLElement') -> List[E.Error]:
        message = Msg.messageType()
        message.build(messageNode)
        return errors + [
            E.Error(code=message.code,
                    message=message.description, carrier=self.client.carrier_name)
        ]

    def _extract_quote(self, quotes: List[E.QuoteDetails], price_quoteNode: 'XMLElement') -> List[E.QuoteDetails]:
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

    def _extract_tracking(self, trackings: List[E.TrackingDetails], pin_summaryNode: 'XMLElement') -> List[E.TrackingDetails]:
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

    def _extract_shipment(self, response: 'XMLElement') -> E.ShipmentDetails:
        is_non_contract = len(response.xpath('.//*[local-name() = $name]', name="non-contract-shipment-info")) > 0
        info = NCShipment.NonContractShipmentInfoType() if is_non_contract else Shipment.ShipmentInfoType()
        data = NCShipment.NonContractShipmentReceiptType() if is_non_contract else Shipment.ShipmentPriceType()
        
        info.build(response.xpath(
            './/*[local-name() = $name]', 
            name=("non-contract-shipment-info" if is_non_contract else "shipment-info")
        )[0])
        data.build(response.xpath(
            './/*[local-name() = $name]', 
            name=("non-contract-shipment-receipt" if is_non_contract else "shipment-price")
        )[0])
        currency_ = data.cc_receipt_details.currency if is_non_contract else "CAD" 

        return E.ShipmentDetails(
            carrier=self.client.carrier_name,
            tracking_numbers=[info.tracking_pin],
            total_charge=E.ChargeDetails(
                name="Shipment charge",
                amount=data.cc_receipt_details.charge_amount if is_non_contract else data.due_amount,
                currency=currency_
            ),
            charges=(
                [
                    E.ChargeDetails(name="base-amount", amount=data.base_amount, currency=currency_),
                    E.ChargeDetails(name="gst-amount", amount=data.gst_amount, currency=currency_),
                    E.ChargeDetails(name="pst-amount", amount=data.pst_amount, currency=currency_),
                    E.ChargeDetails(name="hst-amount", amount=data.hst_amount, currency=currency_),
                ] + [ 
                    E.ChargeDetails(
                        name=adjustment.adjustment_code, 
                        amount=adjustment.adjustment_amount, 
                        currency=currency_
                    ) for adjustment in data.adjustments.get_adjustment()
                ] + [ 
                    E.ChargeDetails(
                        name=option.option_code, 
                        amount=option.option_price, 
                        currency=currency_
                    ) for option in data.priced_options.get_priced_option()
                ]
            ),
            shipment_date=data.service_standard.expected_delivery_date,
            services=(
                [data.service_code] +
                [option.option_code for option in data.priced_options.get_priced_option()]
            ),
            documents=[
                link.get('href') for link in response.xpath('.//*[local-name() = $name]', name="link") if link.get('rel') == 'label'
            ],
            reference=E.ReferenceDetails(
                value=info.shipment_id,
                type="Shipment Id"
            )
        )


    """ Private functions """

    def _create_shipment(self, payload: E.shipment_request) -> Shipment.ShipmentType:
        def _initialise_delivery_spec() -> Shipment.DeliverySpecType:            
            """
            This function is define to ensure type casting
            Note: It is more a convenience than anything else.
            """
            return self._initialise_delivery_spec(payload, False)

        delivery_spec_ = _initialise_delivery_spec()

        delivery_spec_.parcel_characteristics.oversized = payload.shipment.extra.get('oversized')
        
        delivery_spec_.print_preferences = Shipment.PrintPreferencesType(
            output_format=payload.shipment.label.format,
            encoding=payload.shipment.label.extra.get('encoding') if 'encoding' in payload.shipment.label.extra  else None
        )

        if payload.shipment.payment_account_number is not None or 'settlement-info' in payload.shipment.extra:
            delivery_spec_.settlement_info = Shipment.SettlementInfoType(
                promo_code=payload.shipment.extra.get('settlement-info').get('promo-code'),
                paid_by_customer=payload.shipment.payment_account_number,
                contract_id=payload.shipment.extra.get('settlement-info').get('contract-id'),
                cif_shipment=payload.shipment.extra.get('settlement-info').get('cif-shipment'),
                intended_method_of_payment=payload.shipment.extra.get('settlement-info').get('intended-method-of-payment'),
            )

        shipment_ = Shipment.ShipmentType(
            customer_request_id=payload.shipment.shipper_account_number or payload.shipment.payment_account_number or self.client.customer_number,
            quickship_label_requested=payload.shipment.extra.get('quickship-label-requested'),
            cpc_pickup_indicator=payload.shipment.extra.get('cpc-pickup-indicator'),
            requested_shipping_point=payload.shipment.extra.get('requested-shipping-point'),
            shipping_point_id=payload.shipment.extra.get('shipping-point-id'),
            expected_mailing_date=payload.shipment.extra.get('expected-mailing-date'),
            provide_pricing_info=payload.shipment.extra.get('provide-pricing-info'),
            provide_receipt_info=payload.shipment.extra.get('provide-receipt-info'),
            delivery_spec=delivery_spec_
        )

        if 'group-id' in payload.shipment.extra:
            shipment_.groupIdOrTransmitShipment = Shipment.GroupType(
                group_id=payload.shipment.extra.get('group-id').get('group-id'),
                link=payload.shipment.extra.get('group-id').get('link')
            )
        elif 'transmit-shipment' in payload.shipment.extra:
            shipment_.groupIdOrTransmitShipment = payload.shipment.extra.get('transmit-shipment')

        if 'return-spec' in payload.shipment.extra:
            shipment_.return_spec = Shipment.ReturnSpecType(
                service_code=payload.shipment.extra.get('return-spec').get('service-code')
            )
            if 'return-recipient' in payload.shipment.extra.get('return-spec'):
                shipment_.return_spec.return_recipient=Shipment.ReturnRecipientType(
                    name=payload.shipment.extra.get('return-recipient').get('name'),
                    company=payload.shipment.extra.get('return-recipient').get('company'),
                    address_details=Shipment.AddressDetailsType(
                        address_line_1=payload.shipment.extra.get('return-recipient').get('address-details').get('address-line-1'),
                        address_line_2=payload.shipment.extra.get('return-recipient').get('address-details').get('address-line-2'),
                        city=payload.shipment.extra.get('return-recipient').get('address-details').get('city'),
                        prov_state=payload.shipment.extra.get('return-recipient').get('address-details').get('prov-state'),
                        country_code=payload.shipment.extra.get('return-recipient').get('address-details').get('country-code'),
                        postal_zip_code=payload.shipment.extra.get('return-recipient').get('address-details').get('postal-zip-code')
                    )
                )
                shipment_.return_spec.return_notification = payload.shipment.extra.get('return-recipient').get('return-notification')

        if 'pre-authorized-payment' in payload.shipment.extra:
            shipment_.pre_authorized_payment = Shipment.PreAuthorizedPaymentType(
                account_number=payload.shipment.extra.get('pre-authorized-payment').get('account-number'),
                auth_code=payload.shipment.extra.get('pre-authorized-payment').get('auth-code'),
                auth_timestamp=payload.shipment.extra.get('pre-authorized-payment').get('auth-timestamp'),
                charge_amount=payload.shipment.extra.get('pre-authorized-payment').get('charge-amount')
            )

        return shipment_

    def _create_ncshipment(self, payload: E.shipment_request) -> NCShipment.NonContractShipmentType:
        def _initialise_delivery_spec() -> NCShipment.DeliverySpecType:
            """
            This function is define to ensure type casting
            Note: It is more a convenience than anything else.
            """
            return self._initialise_delivery_spec(payload)

        delivery_spec_ = _initialise_delivery_spec()

        delivery_spec_.parcel_characteristics.document = payload.shipment.is_document

        if 'settlement-info' in payload.shipment.extra:
            delivery_spec_.settlement_info = NCShipment.SettlementInfoType(
                promo_code=payload.shipment.extra.get('settlement_info').get('promo_code')
            )

        return NCShipment.NonContractShipmentType(
            requested_shipping_point=payload.shipment.extra.get('requested-shipping-point') or payload.shipper.postal_code,
            delivery_spec=delivery_spec_
        ) 

    def _initialise_delivery_spec(self, payload: E.shipment_request, is_non_contract: bool = True) -> Union[Shipment.DeliverySpecType, NCShipment.DeliverySpecType]:
        Package = NCShipment if is_non_contract else Shipment
        
        sender_ = Package.SenderType(
            name=payload.shipper.person_name,
            company=payload.shipper.company_name,
            contact_phone=payload.shipper.phone_number,
            address_details=Package.AddressDetailsType(
                city=payload.shipper.city,
                prov_state=payload.shipper.state_code,
                country_code=payload.shipper.country_code,
                postal_zip_code=payload.shipper.postal_code,
                address_line_1=payload.shipper.address_lines[0] if len(payload.shipper.address_lines) > 0 else None,
                address_line_2=payload.shipper.address_lines[1] if len(payload.shipper.address_lines) > 1 else None
            )
        )

        destination_ = Package.DestinationType(
            name=payload.recipient.person_name,
            company=payload.recipient.company_name,
            additional_address_info=payload.recipient.extra.get('additional-address-info'),
            client_voice_number=payload.recipient.extra.get('client-voice-number'),
            address_details=Package.DestinationAddressDetailsType(
                city=payload.recipient.city,
                prov_state=payload.recipient.state_code,
                country_code=payload.recipient.country_code,
                postal_zip_code=payload.recipient.postal_code,
                address_line_1=payload.recipient.address_lines[0] if len(payload.recipient.address_lines) > 0 else None,
                address_line_2=payload.recipient.address_lines[1] if len(payload.recipient.address_lines) > 1 else None
            )
        )

        package = payload.shipment.packages[0]
        parcel_characteristics_ = Package.ParcelCharacteristicsType(
            weight=payload.shipment.total_weight or package.weight,
            dimensions=Package.dimensionsType(
                length=package.length,
                width=package.width,
                height=package.height
            ),
            unpackaged=payload.shipment.extra.get('unpackaged'),
            mailing_tube=payload.shipment.extra.get('mailing-tube')
        )

        delivery_spec_ = Package.DeliverySpecType(
            service_code=payload.shipment.services[0].type if len(payload.shipment.services) > 0 else None,
            sender=sender_,
            destination=destination_,
            parcel_characteristics=parcel_characteristics_,
        )

        if 'preferences' in payload.shipment.extra:
            delivery_spec_.preferences = Package.PreferencesType(
                show_packing_instructions=payload.shipment.extra.get('preferences').get('show-packing-instructions'),
                show_postage_rate=payload.shipment.extra.get('preferences').get('show-postage-rate'),
                show_insured_value=payload.shipment.extra.get('preferences').get('show-insured-value')
            )

        if _has_any(payload.shipment.extra, ['cost-centre', 'customer-ref-1', 'customer-ref-2']):
            delivery_spec_.references =  Package.ReferencesType(
                cost_centre=payload.shipment.extra.get('cost-centre'),
                customer_ref_1=payload.shipment.extra.get('customer-ref-1'),
                customer_ref_2=payload.shipment.extra.get('customer-ref-2')
            )

        if _has_any(payload.shipment, ['customs', 'duty-payment-account']):
            delivery_spec_.customs = Package.CustomsType(
                currency=payload.shipment.currency,
                conversion_from_cad=payload.shipment.customs.extra.get('conversion-from-cad'),
                reason_for_export=payload.shipment.customs.terms_of_trade,
                other_reason=payload.shipment.customs.description,
                duties_and_taxes_prepaid=payload.shipment.duty_payment_account,
                certificate_number=payload.shipment.customs.extra.get('certificate-number'),
                licence_number=payload.shipment.customs.extra.get('licence-number'),
                invoice_number=payload.shipment.customs.extra.get('invoice-number')
            )

            if 'sku-list' in payload.shipment.customs.extra:
                delivery_spec_.customs.sku_list = Package.sku_listType()
                for sku in payload.shipment.customs.extra.get('sku-list'):
                    delivery_spec_.customs.sku_list.add_item(Package.SkuType(
                        customs_number_of_units=sku.get('customs-number-of-units'),
                        customs_description=sku.get('customs-description'),
                        sku=sku.get('sku'),
                        hs_tariff_code=sku.get('hs-tariff-code'),
                        unit_weight=sku.get('unit-weight'),
                        customs_value_per_unit=sku.get('customs-value-per-unit'),
                        customs_unit_of_measure=sku.get('customs-unit-of-measure'),
                        country_of_origin=sku.get('country-of-origin'),
                        province_of_origin=sku.get('province-of-origin')
                    ))

        if 'notification' in payload.shipment.extra:
            delivery_spec_.notification = Package.NotificationType(
                email=payload.shipment.extra.get('notification').get('email'),
                on_shipment=payload.shipment.extra.get('notification').get('on-shipment'),
                on_exception=payload.shipment.extra.get('notification').get('on-exception'),
                on_delivery=payload.shipment.extra.get('notification').get('on-delivery')
            )

        if 'options' in payload.shipment.extra:
            delivery_spec_.options = Shipment.optionsType()
            for option in payload.shipment.extra.get('options'):
                delivery_spec_.options.add_option(
                    Package.OptionType(
                        option_code=option.get('option-code'),
                        option_amount=option.get('option-amount'),
                        option_qualifier_1=option.get('option-qualifier-1'),
                        option_qualifier_2=option.get('option-qualifier-2')
                    )
                )

        return delivery_spec_


""" Should be extracted to gds_helpers...? """
def _has_any(dictionary: dict, keys: List[str]) -> bool:
    """
    Return True if at least one key of the list is contained by the dictionary
    """
    return any([k for k in keys if k in dictionary])