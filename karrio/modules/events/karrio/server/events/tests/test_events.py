from datetime import datetime
from unittest.mock import ANY

from karrio.server.events import serializers
from karrio.server.graph.tests.base import GraphTestCase
from karrio.server.events.task_definitions.base import webhook


class TestEventCreation(GraphTestCase):
    def setUp(self) -> None:
        super().setUp()

        event_data = TRACKER_VALUE
        context = dict(user_id=self.user.id, test_mode=False)
        event_type = serializers.EventTypes.tracker_created.value
        event_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f%z")

        webhook.notify_webhook_subscribers(event_type, event_data, event_at, context)

    # def test_query_events(self):
    #     response = self.query(
    #         """
    #         query get_events {
    #           events {
    #             edges {
    #               node {
    #                 id
    #                 type
    #                 data
    #                 test_mode
    #                 pending_webhooks
    #               }
    #             }
    #           }
    #         }
    #         """,
    #         operation_name="get_events",
    #     )
    #     response_data = response.data

    #     self.assertResponseNoErrors(response)
    #     self.assertDictEqual(response_data, EVENTS_RESPONSE)

    def test_query_event(self):
        response = self.query(
            """
            query get_event($id: String!) {
              event(id: $id) {
                id
                type
                data
                test_mode
                pending_webhooks
              }
            }
            """,
            operation_name="get_event",
            variables=dict(id=self.user.event_set.first().id),
        )
        response_data = response.data

        self.assertResponseNoErrors(response)
        self.assertDictEqual(response_data, EVENT_RESPONSE)


TRACKER_VALUE = {
    "tracking_number": "1Z12345E6205277936",
    "test_mode": False,
    "delivered": False,
    "events": [
        {
            "date": "2012-10-04",
            "description": "Order Processed: Ready for UPS",
            "location": "FR",
            "code": "MP",
            "time": "13:58",
        }
    ],
    "status": "in_transit",
}

EVENTS_RESPONSE = {
    "data": {
        "events": {
            "edges": [
                {
                    "node": {
                        "id": ANY,
                        "type": "tracker_created",
                        "data": {
                            "events": [
                                {
                                    "code": "MP",
                                    "date": "2012-10-04",
                                    "time": "13:58",
                                    "location": "FR",
                                    "description": "Order Processed: Ready for UPS",
                                }
                            ],
                            "status": "in_transit",
                            "delivered": False,
                            "test_mode": False,
                            "tracking_number": "1Z12345E6205277936",
                        },
                        "test_mode": False,
                        "pending_webhooks": 0,
                    }
                }
            ]
        }
    }
}

EVENT_RESPONSE = {
    "data": {
        "event": {
            "id": ANY,
            "type": "tracker_created",
            "data": {
                "events": [
                    {
                        "code": "MP",
                        "date": "2012-10-04",
                        "time": "13:58",
                        "location": "FR",
                        "description": "Order Processed: Ready for UPS",
                    }
                ],
                "status": "in_transit",
                "delivered": False,
                "test_mode": False,
                "tracking_number": "1Z12345E6205277936",
            },
            "test_mode": False,
            "pending_webhooks": 0,
        }
    }
}
