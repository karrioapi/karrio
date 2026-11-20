from types import SimpleNamespace
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient

from karrio.server.core.middleware import CreatorAccess
from karrio.server.core import serializers
from karrio.server.manager import models
from karrio.server.orders.serializers.base import OrderData
from karrio.server.serializers import resolve_template_to_json, process_customs_mutation, process_json_array_mutation
from karrio.server.user.models import Token

CITY = {"city": "Private city"}
EXPECTED_HYDRATED_SHIPMENT = {
    "shipper": CITY,
    "recipient": CITY,
    "return_address": CITY,
    "billing_address": CITY,
    "parcels": [{"weight": 7.0, "items": []}, {"weight": 1.0, "items": [{"title": "Private product"}]}],
    "customs": {"duty_billing_address": CITY},
}
PARTIAL_SHIPMENT_UPDATE = """mutation Update($data: PartialShipmentMutationInput!) {
    partial_shipment_update(input: $data) {
        shipment {
            shipper { city } recipient { city } return_address { city } billing_address { city }
            parcels { weight items { title } }
            customs { duty_billing_address { city } }
        }
        errors { field messages }
    } }"""


class TestModelIdScoping(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.owner = get_user_model().objects.create_user(email="owner@example.com", password="test")
        self.other = get_user_model().objects.create_user(email="other@example.com", password="test")
        self.address = models.Address.objects.create(country_code="CA", city="Private city", created_by=self.owner)
        self.parcel = models.Parcel.objects.create(weight=7, weight_unit="KG", created_by=self.owner)
        self.product = models.Commodity.objects.create(title="Private product", created_by=self.owner)
        self.context = SimpleNamespace(user=self.owner)
        access = patch("karrio.server.core.models.base.get_access_filter", new=CreatorAccess())
        access.start()
        self.addCleanup(access.stop)

    def test_decorator_owner_and_other(self):
        for cls, field, obj, key, expected in [
            (serializers.ShipmentData, "shipper", self.address, "city", "Private city"),
            (serializers.ShipmentData, "recipient", self.address, "city", "Private city"),
            (serializers.ShipmentData, "return_address", self.address, "city", "Private city"),
            (serializers.ShipmentData, "billing_address", self.address, "city", "Private city"),
            (serializers.RateRequest, "shipper", self.address, "city", "Private city"),
            (serializers.PickupRequest, "address", self.address, "city", "Private city"),
            (serializers.PickupUpdateRequest, "address", self.address, "city", "Private city"),
            (serializers.PickupCancelRequest, "address", self.address, "city", "Private city"),
            (serializers.ManifestRequestData, "address", self.address, "city", "Private city"),
            (OrderData, "shipping_to", self.address, "city", "Private city"),
            (OrderData, "line_items", self.product, "title", "Private product"),
            (serializers.ShipmentData, "parcels", self.parcel, "weight", 7),
            (serializers.ParcelData, "items", self.product, "title", "Private product"),
        ]:
            with self.subTest(field=field):
                value = {"id": obj.pk}
                data = {field: [value] if field in ("parcels", "items", "line_items") else value}
                owned = cls(data=data, context=self.context).initial_data[field]
                self.assertEqual((owned[0] if isinstance(owned, list) else owned)[key], expected)
                with self.assertRaises(ValidationError):
                    cls(data=data, context=SimpleNamespace(user=self.other))

    def test_decorator_requires_context(self):
        for context in (None, {}):
            with self.subTest(context=context), self.assertRaises(ValidationError):
                serializers.ShipmentData(data={"shipper": {"id": self.address.pk}}, context=context)

    def test_resolver_without_context(self):
        self.assertIsNone(resolve_template_to_json(self.address.pk, models.Address))

    def test_resolver_owner_and_other(self):
        for obj in (self.address, self.parcel, self.product):
            with self.subTest(model=type(obj).__name__):
                owned = resolve_template_to_json(obj.pk, type(obj), context=self.context)
                self.assertEqual(owned["id"], obj.pk)
                self.assertIsNone(resolve_template_to_json(obj.pk, type(obj), context=SimpleNamespace(user=self.other)))

    def test_nested_mutations_scope_templates(self):
        for context, allowed in [(self.context, True), (SimpleNamespace(user=self.other), False), (None, False)]:
            with self.subTest(allowed=allowed, context=context):
                customs = process_customs_mutation(
                    {"customs": {"duty_billing_address": {"id": self.address.pk}, "commodities": [{"id": self.product.pk}]}},
                    None, address_model=models.Address, product_model=models.Commodity, context=context,
                )
                parcel = process_json_array_mutation(
                    "parcels", {"parcels": [{"weight": 1, "items": [{"id": self.product.pk}]}]},
                    None, nested_arrays={"items": ("itm", models.Commodity)}, context=context,
                )[0]
                self.assertEqual(customs["duty_billing_address"] is not None, allowed)
                self.assertEqual(customs["commodities"][0].get("title"), "Private product" if allowed else None)
                self.assertEqual(parcel["items"][0].get("title"), "Private product" if allowed else None)

    def test_request_dict_context(self):
        result = serializers.ShipmentData(data={"shipper": {"id": self.address.pk}}, context={"request": self.context})
        self.assertEqual(result.initial_data["shipper"]["city"], "Private city")
        self.assertEqual(resolve_template_to_json(self.address.pk, models.Address, context={"request": self.context})["city"], "Private city")

    def test_graphql_owner_hydrates_every_nested_record(self):
        """The creator can still use each of their records by id over HTTP: the four
        addresses, a parcel, a parcel item and the customs duty billing address.
        Another user sending the same ids gets none of them. (customs.commodities
        [{id}] loses its id before the lookup for every caller; a separate,
        pre-existing bug.)"""
        product = models.Commodity.objects.create(
            title="Private product", weight=1, weight_unit="KG", quantity=1, created_by=self.owner
        )
        address = {"id": self.address.pk}
        results = {}
        for user in (self.owner, self.other):
            shipment = models.Shipment.objects.create(
                created_by=user,
                status="draft",
                test_mode=True,
                parcels=[{"id": "pcl_cccccccccccc", "weight": 1, "weight_unit": "KG", "items": []}],
            )
            client = APIClient()
            client.credentials(HTTP_AUTHORIZATION=f"Token {Token.objects.create(user=user, test_mode=True).key}")
            response = client.post(
                "/graphql",
                {
                    "query": PARTIAL_SHIPMENT_UPDATE,
                    "variables": {
                        "data": {
                            "id": shipment.pk,
                            "shipper": address,
                            "recipient": address,
                            "return_address": address,
                            "billing_address": address,
                            "parcels": [
                                {"id": self.parcel.pk},
                                {"id": "pcl_cccccccccccc", "weight": 1, "weight_unit": "KG", "items": [{"id": product.pk}]},
                            ],
                            "customs": {"duty_billing_address": address},
                        }
                    },
                },
                format="json",
            )
            self.assertEqual(response.status_code, 200)
            results[user.email] = response.json()

        owner = results[self.owner.email]
        self.assertFalse(owner.get("errors"), owner)
        self.assertFalse(owner["data"]["partial_shipment_update"]["errors"], owner)
        self.assertDictEqual(owner["data"]["partial_shipment_update"]["shipment"], EXPECTED_HYDRATED_SHIPMENT)
        other = results[self.other.email]
        self.assertNotIn("Private", str(other.get("data")), other)
