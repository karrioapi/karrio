from gds_helpers import request as http
from purplship.domain import Proxy
from purplship.mappers.carrier.carrier_mapper import CarrierNameMapper
from purplship.mappers.carrier.carrier_client import CarrierNameClient
from typing import TypeVar
from template.carrier_datatype_mock import (
    CarrierRateRequestType,
    CarrierTrackingRequestType,
    CarrierShipmentRequestType,
    CarrierPickupBookingRequestType,
    CarrierPickupModificationRequestType,
    CarrierPickupCancellationRequestType,
)

CarrierGenericResponseType = TypeVar("T")


class CarrierNameProxy(Proxy):
    def __init__(self, client: CarrierNameClient, mapper: CarrierNameMapper = None):
        self.client = client
        self.mapper = CarrierNameMapper(client) if mapper is None else mapper

    def get_quotes(self, request: CarrierRateRequestType) -> CarrierGenericResponseType:
        data = None

        result = http(
            url=self.client.server_url,
            data=bytearray(data, "utf-8"),
            headers={},
            method="",
        )
        return result

    def get_trackings(
        self, request: CarrierTrackingRequestType
    ) -> CarrierGenericResponseType:
        data = None

        result = http(
            url=self.client.server_url,
            data=bytearray(data, "utf-8"),
            headers={},
            method="",
        )
        return result

    def create_shipment(
        self, request: CarrierShipmentRequestType
    ) -> CarrierGenericResponseType:
        data = None

        result = http(
            url=self.client.server_url,
            data=bytearray(data, "utf-8"),
            headers={},
            method="",
        )
        return result

    def request_pickup(
        self, request: CarrierPickupBookingRequestType
    ) -> CarrierGenericResponseType:
        data = None

        result = http(
            url=self.client.server_url,
            data=bytearray(data, "utf-8"),
            headers={},
            method="",
        )
        return result

    def modify_pickup(
        self, request: CarrierPickupModificationRequestType
    ) -> CarrierGenericResponseType:
        data = None

        result = http(
            url=self.client.server_url,
            data=bytearray(data, "utf-8"),
            headers={},
            method="",
        )
        return result

    def cancel_pickup(
        self, request: CarrierPickupCancellationRequestType
    ) -> CarrierGenericResponseType:
        data = None

        result = http(
            url=self.client.server_url,
            data=bytearray(data, "utf-8"),
            headers={},
            method="",
        )
        return result
