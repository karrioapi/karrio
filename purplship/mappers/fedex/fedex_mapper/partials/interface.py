from typing import Tuple, List
from functools import reduce
from lxml import etree
from purplship.mappers.fedex import FedexClient
from purplship.domain import Types as T
from pyfedex.track_service_v14 import TrackRequest
from pyfedex.ship_service_v21 import ProcessShipmentRequest
from pyfedex.rate_v22 import (
    RateRequest,
    WebAuthenticationCredential,
    WebAuthenticationDetail,
    ClientDetail,
    Notification,
)


class FedexCapabilities:
    """
        FedEx native service request types
    """

    """ Requests """

    def create_rate_request(self, payload: T.shipment_request) -> RateRequest:
        pass

    def create_track_request(self, payload: T.tracking_request) -> TrackRequest:
        pass

    def create_process_shipment_request(
        self, payload: T.shipment_request
    ) -> ProcessShipmentRequest:
        pass

    """ Replys """

    def parse_rate_reply(
        self, response: etree.ElementBase
    ) -> Tuple[List[T.QuoteDetails], List[T.Error]]:
        pass

    def parse_track_reply(
        self, response: etree.ElementBase
    ) -> Tuple[List[T.TrackingDetails], List[T.Error]]:
        pass

    def parse_process_shipment_reply(
        self, response: etree.ElementBase
    ) -> Tuple[T.ShipmentDetails, List[T.Error]]:
        pass


class FedexMapperBase(FedexCapabilities):
    """
        FedEx mapper base class
    """

    def __init__(self, client: FedexClient):
        self.client = client

        userCredential = WebAuthenticationCredential(
            Key=client.user_key, Password=client.password
        )
        self.webAuthenticationDetail = WebAuthenticationDetail(
            UserCredential=userCredential
        )
        self.clientDetail = ClientDetail(
            AccountNumber=client.account_number, MeterNumber=client.meter_number
        )

    def parse_error_response(self, response: etree.ElementBase) -> List[T.Error]:
        notifications = response.xpath(
            ".//*[local-name() = $name]", name="Notifications"
        ) + response.xpath(".//*[local-name() = $name]", name="Notification")
        return reduce(self._extract_error, notifications, [])

    def _extract_error(
        self, errors: List[T.Error], notificationNode: etree.ElementBase
    ) -> List[T.Error]:
        notification = Notification()
        notification.build(notificationNode)
        if notification.Severity in ("SUCCESS", "NOTE"):
            return errors
        return errors + [
            T.Error(
                code=notification.Code,
                message=notification.Message,
                carrier=self.client.carrier_name,
            )
        ]
