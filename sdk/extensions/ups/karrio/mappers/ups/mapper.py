import typing
import karrio.lib as lib
import karrio.api.mapper as mapper
import karrio.core.models as models
import karrio.providers.ups as provider
from karrio.mappers.ups.settings import Settings


class Mapper(mapper.Mapper):
    settings: Settings

    def create_rate_request(self, payload: models.RateRequest) -> lib.Serializable:
        return provider.rate_request(payload, self.settings)

    def create_tracking_request(
        self, payload: models.TrackingRequest
    ) -> lib.Serializable:
        return provider.tracking_request(payload, self.settings)

    def create_shipment_request(
        self, payload: models.ShipmentRequest
    ) -> lib.Serializable:
        return provider.shipment_request(payload, self.settings)

    def create_cancel_shipment_request(
        self, payload: models.ShipmentCancelRequest
    ) -> lib.Serializable:
        return provider.shipment_cancel_request(payload, self.settings)

    def create_document_upload_request(
        self, payload: models.DocumentUploadRequest
    ) -> lib.Serializable:
        return provider.document_upload_request(payload, self.settings)

    def parse_cancel_shipment_response(
        self, response: lib.Deserializable
    ) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
        return provider.parse_shipment_cancel_response(response, self.settings)

    def parse_rate_response(
        self, response: lib.Deserializable
    ) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
        return provider.parse_rate_response(response, self.settings)

    def parse_shipment_response(
        self, response: lib.Deserializable
    ) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
        return provider.parse_shipment_response(response, self.settings)

    def parse_tracking_response(
        self, response: lib.Deserializable
    ) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
        return provider.parse_tracking_response(response, self.settings)

    def parse_document_upload_response(
        self,
        response: lib.Deserializable,
    ) -> typing.Tuple[models.DocumentUploadDetails, typing.List[models.Message]]:
        return provider.parse_document_upload_response(response, self.settings)
