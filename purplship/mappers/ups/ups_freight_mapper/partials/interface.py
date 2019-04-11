from typing import Tuple, List
from functools import reduce
from lxml import etree
from purplship.mappers.ups import UPSClient
from purplship.domain import Types as T
from pyups import (
    freight_rate as Rate,
    UPSSecurity as Security,
    error as Err,
    freight_ship as FShip,
)


class UPSCapabilities:
    """
        UPS native service request types
    """

    """ Requests factories """

    def create_freight_rate_request(
        self, payload: T.ShipmentRequest
    ) -> Rate.FreightRateRequest:
        pass

    def create_freight_ship_request(
        self, payload: T.ShipmentRequest
    ) -> FShip.FreightShipRequest:
        pass

    """ Response Parser """

    def parse_freight_rate_response(
        self, response: etree.ElementBase
    ) -> Tuple[List[T.QuoteDetails], List[T.Error]]:
        pass

    def parse_freight_shipment_response(
        self, response: etree.ElementBase
    ) -> T.ShipmentDetails:
        pass


class UPSMapperBase(UPSCapabilities):
    """
        UPS mapper base class
    """

    def __init__(self, client: UPSClient):
        self.client = client

        self.Security = Security.UPSSecurity(
            UsernameToken=Security.UsernameTokenType(
                Username=self.client.username, Password=self.client.password
            ),
            ServiceAccessToken=Security.ServiceAccessTokenType(
                AccessLicenseNumber=self.client.access_license_number
            ),
        )

    def parse_error_response(self, response) -> List[T.Error]:
        notifications = response.xpath(
            ".//*[local-name() = $name]", name="PrimaryErrorCode"
        )
        return reduce(self._extract_error, notifications, [])

    def _extract_error(
        self, errors: List[T.Error], errorNode: etree.ElementBase
    ) -> List[T.Error]:
        error = Err.CodeType()
        error.build(errorNode)
        return errors + [
            T.Error(
                code=error.Code,
                message=error.Description,
                carrier=self.client.carrier_name,
            )
        ]
