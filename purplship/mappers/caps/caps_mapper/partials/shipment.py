from pycaps import shipment as Shipment, ncshipment as NCShipment
from base64 import b64encode
from datetime import datetime
from lxml import etree
from typing import Any, Tuple, List, Union
from .interface import reduce, T, CanadaPostMapperBase
from purplship.domain.Types.units import Dimension, DimensionUnit, Weight, WeightUnit
from purplship.mappers.caps.caps_units import OptionCode, ServiceType


class CanadaPostMapperPartial(CanadaPostMapperBase):
    def parse_shipment_info(
        self, response: etree.ElementBase
    ) -> Tuple[T.ShipmentDetails, List[T.Error]]:
        shipment = (
            self._extract_shipment(response)
            if len(response.xpath(".//*[local-name() = $name]", name="shipment-id")) > 0
            else None
        )
        return (shipment, self.parse_error_response(response))

    def create_shipment(
        self, payload: T.shipment_request
    ) -> Union[Shipment.ShipmentType, NCShipment.NonContractShipmentType]:
        is_non_contract = payload.shipment.extra.get("settlement-info") is None
        shipment = (
            self._create_ncshipment(payload)
            if is_non_contract
            else self._create_shipment(payload)
        )
        return shipment

    """ Private functions """

    def _extract_shipment(self, response: etree.ElementBase) -> T.ShipmentDetails:
        is_non_contract = (
            len(
                response.xpath(
                    ".//*[local-name() = $name]", name="non-contract-shipment-info"
                )
            )
            > 0
        )
        info = (
            NCShipment.NonContractShipmentInfoType()
            if is_non_contract
            else Shipment.ShipmentInfoType()
        )
        data = (
            NCShipment.NonContractShipmentReceiptType()
            if is_non_contract
            else Shipment.ShipmentPriceType()
        )

        info.build(
            response.xpath(
                ".//*[local-name() = $name]",
                name=(
                    "non-contract-shipment-info" if is_non_contract else "shipment-info"
                ),
            )[0]
        )
        data.build(
            response.xpath(
                ".//*[local-name() = $name]",
                name=(
                    "non-contract-shipment-receipt"
                    if is_non_contract
                    else "shipment-price"
                ),
            )[0]
        )
        currency_ = data.cc_receipt_details.currency if is_non_contract else "CAD"

        return T.ShipmentDetails(
            carrier=self.client.carrier_name,
            tracking_numbers=[info.tracking_pin],
            total_charge=T.ChargeDetails(
                name="Shipment charge",
                amount=data.cc_receipt_details.charge_amount
                if is_non_contract
                else data.due_amount,
                currency=currency_,
            ),
            charges=(
                [
                    T.ChargeDetails(
                        name="base-amount", amount=data.base_amount, currency=currency_
                    ),
                    T.ChargeDetails(
                        name="gst-amount", amount=data.gst_amount, currency=currency_
                    ),
                    T.ChargeDetails(
                        name="pst-amount", amount=data.pst_amount, currency=currency_
                    ),
                    T.ChargeDetails(
                        name="hst-amount", amount=data.hst_amount, currency=currency_
                    ),
                ]
                + [
                    T.ChargeDetails(
                        name=adjustment.adjustment_code,
                        amount=adjustment.adjustment_amount,
                        currency=currency_,
                    )
                    for adjustment in data.adjustments.get_adjustment()
                ]
                + [
                    T.ChargeDetails(
                        name=option.option_code,
                        amount=option.option_price,
                        currency=currency_,
                    )
                    for option in data.priced_options.get_priced_option()
                ]
            ),
            shipment_date=data.service_standard.expected_delivery_date,
            services=(
                [data.service_code]
                + [
                    option.option_code
                    for option in data.priced_options.get_priced_option()
                ]
            ),
            documents=[
                link.get("href")
                for link in response.xpath(".//*[local-name() = $name]", name="link")
                if link.get("rel") == "label"
            ],
            reference=T.ReferenceDetails(value=info.shipment_id, type="Shipment Id"),
        )

    def _create_shipment(self, payload: T.shipment_request) -> Shipment.ShipmentType:
        delivery_spec_: Shipment.DeliverySpecType = self._initialise_delivery_spec(
            payload, False
        )

        delivery_spec_.parcel_characteristics.oversized = payload.shipment.extra.get(
            "oversized"
        )

        delivery_spec_.print_preferences = Shipment.PrintPreferencesType(
            output_format=payload.shipment.label.format,
            encoding=payload.shipment.label.extra.get("encoding")
            if "encoding" in payload.shipment.label.extra
            else None,
        )

        if (
            payload.shipment.payment_account_number is not None
            or "settlement-info" in payload.shipment.extra
        ):
            delivery_spec_.settlement_info = Shipment.SettlementInfoType(
                promo_code=payload.shipment.extra.get("settlement-info").get(
                    "promo-code"
                ),
                paid_by_customer=payload.shipment.payment_account_number,
                contract_id=payload.shipment.extra.get("settlement-info").get(
                    "contract-id"
                ),
                cif_shipment=payload.shipment.extra.get("settlement-info").get(
                    "cif-shipment"
                ),
                intended_method_of_payment=payload.shipment.extra.get(
                    "settlement-info"
                ).get("intended-method-of-payment"),
            )

        shipment_ = Shipment.ShipmentType(
            customer_request_id=payload.shipper.account_number
            or payload.shipment.payment_account_number,
            quickship_label_requested=payload.shipment.extra.get(
                "quickship-label-requested"
            ),
            cpc_pickup_indicator=payload.shipment.extra.get("cpc-pickup-indicator"),
            requested_shipping_point=payload.shipment.extra.get(
                "requested-shipping-point"
            ),
            shipping_point_id=payload.shipment.extra.get("shipping-point-id"),
            expected_mailing_date=payload.shipment.extra.get("expected-mailing-date"),
            provide_pricing_info=payload.shipment.extra.get("provide-pricing-info"),
            provide_receipt_info=payload.shipment.extra.get("provide-receipt-info"),
            delivery_spec=delivery_spec_,
        )

        if "group-id" in payload.shipment.extra:
            shipment_.groupIdOrTransmitShipment = Shipment.GroupType(
                group_id=payload.shipment.extra.get("group-id").get("group-id"),
                link=payload.shipment.extra.get("group-id").get("link"),
            )
        elif "transmit-shipment" in payload.shipment.extra:
            shipment_.groupIdOrTransmitShipment = payload.shipment.extra.get(
                "transmit-shipment"
            )

        if "return-spec" in payload.shipment.extra:
            shipment_.return_spec = Shipment.ReturnSpecType(
                service_code=payload.shipment.extra.get("return-spec").get(
                    "service-code"
                )
            )
            if "return-recipient" in payload.shipment.extra.get("return-spec"):
                shipment_.return_spec.return_recipient = Shipment.ReturnRecipientType(
                    name=payload.shipment.extra.get("return-recipient").get("name"),
                    company=payload.shipment.extra.get("return-recipient").get(
                        "company"
                    ),
                    address_details=Shipment.AddressDetailsType(
                        address_line_1=payload.shipment.extra.get("return-recipient")
                        .get("address-details")
                        .get("address-line-1"),
                        address_line_2=payload.shipment.extra.get("return-recipient")
                        .get("address-details")
                        .get("address-line-2"),
                        city=payload.shipment.extra.get("return-recipient")
                        .get("address-details")
                        .get("city"),
                        prov_state=payload.shipment.extra.get("return-recipient")
                        .get("address-details")
                        .get("prov-state"),
                        country_code=payload.shipment.extra.get("return-recipient")
                        .get("address-details")
                        .get("country-code"),
                        postal_zip_code=payload.shipment.extra.get("return-recipient")
                        .get("address-details")
                        .get("postal-zip-code"),
                    ),
                )
                shipment_.return_spec.return_notification = payload.shipment.extra.get(
                    "return-recipient"
                ).get("return-notification")

        if "pre-authorized-payment" in payload.shipment.extra:
            shipment_.pre_authorized_payment = Shipment.PreAuthorizedPaymentType(
                account_number=payload.shipment.extra.get("pre-authorized-payment").get(
                    "account-number"
                ),
                auth_code=payload.shipment.extra.get("pre-authorized-payment").get(
                    "auth-code"
                ),
                auth_timestamp=payload.shipment.extra.get("pre-authorized-payment").get(
                    "auth-timestamp"
                ),
                charge_amount=payload.shipment.extra.get("pre-authorized-payment").get(
                    "charge-amount"
                ),
            )

        return shipment_

    def _create_ncshipment(
        self, payload: T.shipment_request
    ) -> NCShipment.NonContractShipmentType:
        delivery_spec_: NCShipment.DeliverySpecType = self._initialise_delivery_spec(
            payload
        )

        delivery_spec_.parcel_characteristics.document = payload.shipment.is_document

        if "settlement-info" in payload.shipment.extra:
            delivery_spec_.settlement_info = NCShipment.SettlementInfoType(
                promo_code=payload.shipment.extra.get("settlement_info").get(
                    "promo_code"
                )
            )

        return NCShipment.NonContractShipmentType(
            requested_shipping_point=payload.shipment.extra.get(
                "requested-shipping-point"
            )
            or payload.shipper.postal_code,
            delivery_spec=delivery_spec_,
        )

    def _initialise_delivery_spec(
        self, payload: T.shipment_request, is_non_contract: bool = True
    ) -> Union[Shipment.DeliverySpecType, NCShipment.DeliverySpecType]:
        Package = NCShipment if is_non_contract else Shipment
        package = payload.shipment.items[0]
        requested_services = [
            svc for svc in payload.shipment.services if svc in ServiceType.__members__
        ]
        requested_options = [
            opt
            for opt in payload.shipment.options
            if opt.code in OptionCode.__members__
        ]

        return Package.DeliverySpecType(
            service_code=ServiceType[requested_services[0]].value
            if len(requested_services) > 0
            else None,
            sender=Package.SenderType(
                name=payload.shipper.person_name,
                company=payload.shipper.company_name,
                contact_phone=payload.shipper.phone_number,
                address_details=Package.AddressDetailsType(
                    city=payload.shipper.city,
                    prov_state=payload.shipper.state_code,
                    country_code=payload.shipper.country_code,
                    postal_zip_code=payload.shipper.postal_code,
                    address_line_1=payload.shipper.address_lines[0]
                    if len(payload.shipper.address_lines) > 0
                    else None,
                    address_line_2=payload.shipper.address_lines[1]
                    if len(payload.shipper.address_lines) > 1
                    else None,
                ),
            ),
            destination=Package.DestinationType(
                name=payload.recipient.person_name,
                company=payload.recipient.company_name,
                additional_address_info=payload.recipient.extra.get(
                    "additional-address-info"
                ),
                client_voice_number=payload.recipient.extra.get("client-voice-number"),
                address_details=Package.DestinationAddressDetailsType(
                    city=payload.recipient.city,
                    prov_state=payload.recipient.state_code,
                    country_code=payload.recipient.country_code,
                    postal_zip_code=payload.recipient.postal_code,
                    address_line_1=payload.recipient.address_lines[0]
                    if len(payload.recipient.address_lines) > 0
                    else None,
                    address_line_2=payload.recipient.address_lines[1]
                    if len(payload.recipient.address_lines) > 1
                    else None,
                ),
            ),
            parcel_characteristics=Package.ParcelCharacteristicsType(
                weight=Weight(
                    payload.shipment.total_weight or package.weight,
                    WeightUnit[payload.shipment.weight_unit],
                ).KG,
                dimensions=Package.dimensionsType(
                    length=Dimension(
                        package.length, DimensionUnit[payload.shipment.dimension_unit]
                    ).CM,
                    width=Dimension(
                        package.width, DimensionUnit[payload.shipment.dimension_unit]
                    ).CM,
                    height=Dimension(
                        package.height, DimensionUnit[payload.shipment.dimension_unit]
                    ).CM,
                ),
                unpackaged=payload.shipment.extra.get("unpackaged"),
                mailing_tube=payload.shipment.extra.get("mailing-tube"),
            ),
            options=Shipment.optionsType(
                option=[
                    Package.OptionType(
                        option_code=OptionCode[option.code].value,
                        option_amount=option.value.get("option-amount"),
                        option_qualifier_1=option.value.get("option-qualifier-1"),
                        option_qualifier_2=option.value.get("option-qualifier-2"),
                    )
                    for option in requested_options
                ]
            )
            if len(requested_options) > 0
            else None,
            notification=Package.NotificationType(
                email=payload.shipment.extra.get("notification").get("email"),
                on_shipment=payload.shipment.extra.get("notification").get(
                    "on-shipment"
                ),
                on_exception=payload.shipment.extra.get("notification").get(
                    "on-exception"
                ),
                on_delivery=payload.shipment.extra.get("notification").get(
                    "on-delivery"
                ),
            )
            if ("notification" in payload.shipment.extra)
            else None,
            preferences=Package.PreferencesType(
                show_packing_instructions=payload.shipment.extra.get("preferences").get(
                    "show-packing-instructions"
                ),
                show_postage_rate=payload.shipment.extra.get("preferences").get(
                    "show-postage-rate"
                ),
                show_insured_value=payload.shipment.extra.get("preferences").get(
                    "show-insured-value"
                ),
            )
            if ("preferences" in payload.shipment.extra)
            else None,
            customs=Package.CustomsType(
                currency=payload.shipment.currency,
                conversion_from_cad=payload.shipment.customs.extra.get(
                    "conversion-from-cad"
                ),
                reason_for_export=payload.shipment.customs.terms_of_trade,
                other_reason=payload.shipment.customs.description,
                duties_and_taxes_prepaid=payload.shipment.duty_payment_account,
                certificate_number=payload.shipment.customs.extra.get(
                    "certificate-number"
                ),
                licence_number=payload.shipment.customs.extra.get("licence-number"),
                invoice_number=payload.shipment.customs.extra.get("invoice-number"),
                sku_list=Package.sku_listType(
                    item=[
                        Package.SkuType(
                            customs_number_of_units=item.quantity,
                            customs_description=item.description,
                            sku=item.sku,
                            hs_tariff_code=item.extra.get("hs-tariff-code"),
                            unit_weight=WeightUnit.KG.value,
                            customs_value_per_unit=item.value_amount,
                            customs_unit_of_measure=DimensionUnit.CM.value,
                            country_of_origin=item.origin_country,
                            province_of_origin=item.extra.get("province-of-origin"),
                        )
                        for item in payload.shipment.items
                    ]
                ),
            )
            if _has_any(payload.shipment, ["customs", "duty-payment-account"])
            else None,
            references=Package.ReferencesType(
                cost_centre=payload.shipment.extra.get("cost-centre"),
                customer_ref_1=payload.shipment.references[0]
                if len(payload.shipment.references) > 0
                else None,
                customer_ref_2=payload.shipment.references[1]
                if len(payload.shipment.references) > 1
                else None,
            )
            if len(payload.shipment.references) > 0
            else None,
        )


""" Should be extracted to gds_helpers...? """


def _has_any(obj: Any, keys: List[str]) -> bool:
    """
    Return True if at least one key of the list is contained by the obj
    """
    return any([k for k in keys if k in obj])
