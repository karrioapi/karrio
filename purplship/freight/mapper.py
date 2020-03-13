"""PurplShip Mapper base class definition module."""

import attr
from abc import ABC
from typing import List, Tuple
from purplship.core.settings import Settings
from purplship.core.models import (
    Error, RateRequest, TrackingRequest, ShipmentDetails, ShipmentRequest,
    PickupRequest, PickupCancellationRequest, PickupUpdateRequest, PickupDetails,
    RateDetails, TrackingDetails
)
from purplship.core.errors import MethodNotSupportedError
from purplship.core.utils.serializable import Deserializable, Serializable


@attr.s(auto_attribs=True)
class Mapper(ABC):
    """Unified Shipping API Mapper (Interface)
    """
    settings: Settings

    def create_rate_request(self, payload: RateRequest) -> Serializable:
        """ Create a carrier specific rate request data from payload """
        raise MethodNotSupportedError(self.__class__.create_rate_request.__name__, self.__class__.__name__)

    def parse_rate_response(self, response: Deserializable) -> Tuple[List[RateDetails], List[Error]]:
        """ Create a united API quote result list from carrier response  """
        raise MethodNotSupportedError(self.__class__.parse_rate_response.__name__, self.__class__.__name__)

    def create_tracking_request(self, payload: TrackingRequest) -> Serializable:
        """ Create a carrier specific tracking request data from payload """
        raise MethodNotSupportedError(self.__class__.create_tracking_request.__name__, self.__class__.__name__)

    def parse_tracking_response(self, response: Deserializable) -> Tuple[List[TrackingDetails], List[Error]]:
        """ Create a united API tracking result list from carrier response  """
        raise MethodNotSupportedError(self.__class__.parse_tracking_response.__name__, self.__class__.__name__)

    def create_shipment_request(self, payload: ShipmentRequest) -> Serializable:
        """ Create a carrier specific shipment creation request data from payload """
        raise MethodNotSupportedError(self.__class__.create_shipment_request.__name__, self.__class__.__name__)

    def parse_shipment_response(self, response: Deserializable) -> Tuple[ShipmentDetails, List[Error]]:
        """ Create a united API shipment creation result from carrier response  """
        raise MethodNotSupportedError(self.__class__.parse_shipment_response.__name__, self.__class__.__name__)

    def create_pickup_request(self, payload: PickupRequest) -> Serializable:
        """ Create a carrier specific pickup request xml data from payload """
        raise MethodNotSupportedError(self.__class__.create_pickup_request.__name__, self.__class__.__name__)

    def parse_pickup_response(self, response: Deserializable) -> Tuple[PickupDetails, List[Error]]:
        """ Create a united API pickup result from carrier response  """
        raise MethodNotSupportedError(self.__class__.parse_pickup_response.__name__, self.__class__.__name__)

    def create_modify_pickup_request(self, payload: PickupUpdateRequest) -> Serializable:
        """ Create a carrier specific pickup modification request data from payload """
        raise MethodNotSupportedError(self.__class__.create_modify_pickup_request.__name__, self.__class__.__name__)

    def parse_modify_pickup_response(self, response: Deserializable) -> Tuple[PickupDetails, List[Error]]:
        """ Create a united API pickup result from carrier response  """
        raise MethodNotSupportedError(self.__class__.parse_modify_pickup_response.__name__, self.__class__.__name__)

    def create_cancel_pickup_request(self, payload: PickupCancellationRequest) -> Serializable:
        """ Create a carrier specific pickup cancellation request data from payload """
        raise MethodNotSupportedError(self.__class__.create_cancel_pickup_request.__name__, self.__class__.__name__)

    def parse_cancel_pickup_response(self, response: Deserializable) -> Tuple[dict, List[Error]]:
        """ Create a united API pickup cancellation result from carrier response  """
        raise MethodNotSupportedError(self.__class__.parse_cancel_pickup_response.__name__, self.__class__.__name__)
