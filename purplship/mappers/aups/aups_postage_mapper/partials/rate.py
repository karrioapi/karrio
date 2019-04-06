"""PurplShip Australia post rate mapper module."""

from typing import List, Tuple, Union
from .interface import AustraliaPostMapperBase
from purplship.domain.Types import (
    Error,
    ShipmentRequest,
    QuoteDetails,
    Item
)
from purplship.domain.Types.errors import OriginNotServicedError, MultiItemShipmentSupportError
from purplship.domain.Types.units import (
    Weight,
    WeightUnit,
    Dimension,
    DimensionUnit,
    PackagingUnit,
    Country
)
from pyaups.international_parcel_postage import ServiceRequest as IntlParcelServiceRequest
from pyaups.domestic_letter_postage import ServiceRequest as DomesticLetterServiceRequest
from pyaups.international_letter_postage import ServiceRequest as IntlLetterServiceRequest
from pyaups.domestic_parcel_postage import (
    ServiceRequest as DomesticParcelServiceRequest,
    ServiceResponse,
    Service
)

DomesticServiceRequest = Union[DomesticLetterServiceRequest, DomesticParcelServiceRequest]
IntlServiceRequest = Union[IntlLetterServiceRequest, IntlParcelServiceRequest]


class AustraliaPostMapperPartial(AustraliaPostMapperBase):
    def parse_service_response(
        self, response: dict
    ) -> Tuple[List[QuoteDetails], List[Error]]:
        services: List[Service] = (
            ServiceResponse(**response).services.service
            if "services" in response else []
        )
        return (
            [self._extract_quote(svc) for svc in services],
            self.parse_error_response(response)
        )

    def _extract_quote(self, service: Service) -> QuoteDetails:
        return QuoteDetails(
            carrier=self.client.carrier_name,
            service_name=service.name,
            service_type=service.code,
            base_charge=None,
            duties_and_taxes=None,
            total_charge=float(service.price),
            currency="AUD",
            delivery_date=None,
            discount=None,
            extra_charges=None
        )

    def create_service_request(self, payload: ShipmentRequest) -> Union[DomesticServiceRequest, IntlServiceRequest]:
        """Create the appropriate Australia post postage service request depending on the destination

        :param payload: PurplShip unified API rate request data
        :return: a domestic or international Australia post compatible request
        :raises: an OriginNotServicedError when origin country is not serviced by the carrier
        """
        if payload.shipper.country_code and payload.shipper.country_code != 'AU':
            raise OriginNotServicedError(payload.shipper.country_code, self.client.carrier_name)
        if len(payload.shipment.items) > 1:
            raise MultiItemShipmentSupportError(self.client.carrier_name)

        return (
            AustraliaPostMapperPartial._create_domestic_service_request
            if (
                payload.recipient.country_code is None or
                payload.recipient.country_code == Country.AU.name
            ) else
            AustraliaPostMapperPartial._create_intl_service_request
        )(payload)

    @staticmethod
    def _create_domestic_service_request(payload: ShipmentRequest) -> DomesticServiceRequest:
        weight_unit: WeightUnit = WeightUnit[payload.shipment.weight_unit or "KG"]
        dimension_unit: DimensionUnit = DimensionUnit[payload.shipment.dimension_unit or "CM"]
        item: Item = payload.shipment.items[0]
        is_letter: bool = (
            any(svc for svc in payload.shipment.services if 'LETTER' in svc)
            or payload.shipment.packaging_type == PackagingUnit.SM.name
            or item.packaging_type == PackagingUnit.SM.name
        )
        return (
            DomesticLetterServiceRequest(
                length=Dimension(item.length, dimension_unit).CM,
                width=Dimension(item.width, dimension_unit).CM,
                thickness=Dimension(item.extra.get('thickness') or item.height, dimension_unit).CM,
                weight=Weight(item.weight or payload.shipment.total_weight, weight_unit).KG
            )
            if is_letter else
            DomesticParcelServiceRequest(
                from_postcode=payload.shipper.postal_code,
                to_postcode=payload.recipient.postal_code,
                length=Dimension(item.length, dimension_unit).CM,
                width=Dimension(item.width, dimension_unit).CM,
                height=Dimension(item.height, dimension_unit).CM,
                weight=Weight(item.weight or payload.shipment.total_weight, weight_unit).KG,
            )
        )

    @staticmethod
    def _create_intl_service_request(payload: ShipmentRequest) -> IntlServiceRequest:
        weight_unit: WeightUnit = WeightUnit[payload.shipment.weight_unit or "KG"]
        item: Item = payload.shipment.items[0]
        weight: float = item.weight or payload.shipment.total_weight
        is_letter: bool = (
            any(svc for svc in payload.shipment.services if 'LETTER' in svc)
            or payload.shipment.packaging_type == PackagingUnit.SM.name
            or item.packaging_type == PackagingUnit.SM.name
        )
        return (
            IntlLetterServiceRequest(
                country_code=payload.recipient.country_code,
                weight=Weight(weight, weight_unit).KG
            )
            if is_letter else
            IntlParcelServiceRequest(
                country_code=payload.recipient.country_code,
                weight=Weight(weight, weight_unit).KG
            )
        )
