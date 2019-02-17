from gds_helpers import to_xml, export, request as http
from lxml import etree
from pyfedex import (
    rate_v22 as Rate,
    track_service_v14 as Track,
    ship_service_v21 as Ship,
    pickup_service_v15 as Pick,
)
from pysoap.envelope import Body, Envelope
from pysoap import create_envelope, clean_namespaces
from purplship.domain.proxy import Proxy
from purplship.mappers.fedex.fedex_mapper import FedexMapper
from purplship.mappers.fedex.fedex_client import FedexClient


class FedexProxy(Proxy):
    def __init__(self, client: FedexClient, mapper: FedexMapper = None):
        self.client = client
        self.mapper = FedexMapper(client) if mapper is None else mapper

    def get_quotes(self, RateRequest_: Rate.RateRequest) -> etree.ElementBase:
        envelopeStr = export(
            create_envelope(body_content=RateRequest_),
            namespacedef_='xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:ns="http://fedex.com/ws/rate/v22"',
        )
        xmlStr = clean_namespaces(
            envelopeStr,
            envelope_prefix="tns:",
            body_child_prefix="ns:",
            body_child_name="RateRequest",
        )

        result = http(
            url=self.client.server_url,
            data=bytearray(xmlStr, "utf-8"),
            headers={"Content-Type": "application/xml"},
            method="POST",
        )
        return to_xml(result)

    def get_trackings(self, TrackRequest_: Track.TrackRequest) -> etree.ElementBase:
        envelopeStr = export(
            create_envelope(body_content=TrackRequest_),
            namespacedef_='xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://fedex.com/ws/track/v14"',
        )
        xmlStr = clean_namespaces(
            envelopeStr,
            envelope_prefix="tns:",
            body_child_prefix="ns:",
            body_child_name="TrackRequest",
        )
        result = http(
            url=self.client.server_url,
            data=bytearray(xmlStr, "utf-8"),
            headers={"Content-Type": "application/xml"},
            method="POST",
        )
        return to_xml(result)

    def create_shipment(
        self, ShipmenRequest_: Ship.ProcessShipmentRequest
    ) -> etree.ElementBase:
        envelopeStr = export(
            create_envelope(body_content=ShipmenRequest_),
            namespacedef_='xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://fedex.com/ws/ship/v21"',
        )
        xmlStr = clean_namespaces(
            envelopeStr,
            envelope_prefix="tns:",
            body_child_prefix="ns:",
            body_child_name="ProcessShipmentRequest",
        )
        result = http(
            url=self.client.server_url,
            data=bytearray(xmlStr, "utf-8"),
            headers={"Content-Type": "application/xml"},
            method="POST",
        )
        return to_xml(result)

    def request_pickup(
        self, CreatePickupRequest_: Pick.CreatePickupRequest
    ) -> etree.ElementBase:
        envelopeStr = export(
            create_envelope(body_content=CreatePickupRequest_),
            namespacedef_='xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://fedex.com/ws/pickup/v15"',
        )
        xmlStr = clean_namespaces(
            envelopeStr,
            envelope_prefix="tns:",
            body_child_prefix="ns:",
            body_child_name="CreatePickupRequest",
        )
        result = http(
            url=self.client.server_url,
            data=bytearray(xmlStr, "utf-8"),
            headers={"Content-Type": "application/xml"},
            method="POST",
        )
        return to_xml(result)

    def cancel_pickup(
        self, CancelPickupRequest_: Pick.CancelPickupRequest
    ) -> etree.ElementBase:
        envelopeStr = export(
            create_envelope(body_content=CancelPickupRequest_),
            namespacedef_='xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://fedex.com/ws/pickup/v15"',
        )
        xmlStr = clean_namespaces(
            envelopeStr,
            envelope_prefix="tns:",
            body_child_prefix="ns:",
            body_child_name="CancelPickupRequest",
        )
        result = http(
            url=self.client.server_url,
            data=bytearray(xmlStr, "utf-8"),
            headers={"Content-Type": "application/xml"},
            method="POST",
        )
        return to_xml(result)
