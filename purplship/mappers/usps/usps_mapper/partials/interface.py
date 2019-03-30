from typing import Tuple, List, Union
from lxml import etree
from purplship.mappers.usps import USPSClient
from purplship.domain.Types import (
    RateRequest,
    TrackingRequest,
    QuoteDetails,
    TrackingDetails,
    Error,
)
from pyusps.ratev4request import RateV4Request
from pyusps.intlratev2request import IntlRateV2Request
from pyusps.trackfieldrequest import TrackFieldRequest
from pyusps.error import Error as USPSError


class USPSCapabilities:
    """
        USPS native service request types
    """

    """ Requests """

    def create_rate_request(
        self, payload: RateRequest
    ) -> Union[RateV4Request, IntlRateV2Request]:
        pass

    def create_track_request(self, payload: TrackingRequest) -> TrackFieldRequest:
        pass

    """ Reply """

    def parse_rate_response(
        self, response: etree.ElementBase
    ) -> Tuple[List[QuoteDetails], List[Error]]:
        pass

    def parse_track_response(
        self, response: etree.ElementBase
    ) -> Tuple[List[TrackingDetails], List[Error]]:
        pass


class USPSMapperBase(USPSCapabilities):
    """
        USPS mapper base class
    """

    def __init__(self, client: USPSClient):
        self.client = client

    def parse_error_response(self, response: etree.ElementBase) -> List[Error]:
        error_nodes: List[USPSError] = [
            (lambda error: (error, error.build(node)))(USPSError())[0]
            for node in response.xpath(".//*[local-name() = $name]", name="Error")
        ]
        return [
            Error(
                carrier=self.client.carrier_name,
                code=error.Number,
                message=error.Description,
                details=dict(context=error.HelpContext),
            )
            for error in error_nodes
        ]
