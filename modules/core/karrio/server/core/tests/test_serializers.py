from django.test import TestCase

from karrio.server.core.serializers import Message


class TestMessageSerializer(TestCase):
    """The SDK ``Message`` model declares message/code/level/details optional
    (default ``None``). When a shipment draft is saved it echoes a carrier's
    rate messages back as input, so the serializer must accept null for these
    fields rather than raise "This field may not be null"."""

    def test_accepts_null_level_and_details(self):
        serializer = Message(
            data={
                "carrier_id": "postnord",
                "carrier_name": "postnord",
                "code": "transit_time_unavailable",
                "message": "ETA enrichment unavailable",
                "level": None,
                "details": None,
            }
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_accepts_all_null_optional_fields_many(self):
        serializer = Message(
            many=True,
            data=[
                {
                    "carrier_id": "postnord",
                    "carrier_name": "postnord",
                    "message": None,
                    "code": None,
                    "level": None,
                    "details": None,
                }
            ],
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_omits_missing_optional_fields_from_representation(self):
        data = Message(
            {
                "carrier_id": "postnord",
                "carrier_name": "postnord",
                "message": "Label created",
            }
        ).data

        self.assertDictEqual(
            dict(data),
            {
                "carrier_id": "postnord",
                "carrier_name": "postnord",
                "message": "Label created",
            },
        )
