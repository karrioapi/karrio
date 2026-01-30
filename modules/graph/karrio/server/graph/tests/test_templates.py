from unittest.mock import ANY
from karrio.server.graph.tests.base import GraphTestCase
import karrio.server.manager.models as manager


class TestAddress(GraphTestCase):
    def _create_address(self):
        return self.query(
            """
            mutation create_address($data: CreateAddressInput!) {
              create_address(input: $data) {
                address {
                  id
                  meta
                  company_name
                  person_name
                  address_line1
                  address_line2
                  postal_code
                  residential
                  city
                  state_code
                  country_code
                  email
                  phone_number
                  validation
                  validate_location
                }
                errors {
                  field
                  messages
                }
              }
            }
            """,
            operation_name="create_address",
            variables=ADDRESS_DATA,
        )

    def test_create_address(self):
        response = self._create_address()
        self.assertResponseNoErrors(response)
        self.assertDictEqual(response.data, ADDRESS_RESPONSE)

    def test_update_address(self):
        address = self._create_address().data
        response = self.query(
            """
            mutation update_address($data: UpdateAddressInput!) {
              update_address(input: $data) {
                address {
                  id
                  meta
                  company_name
                  person_name
                  address_line1
                  address_line2
                  postal_code
                  residential
                  city
                  state_code
                  country_code
                  email
                  phone_number
                  validation
                  validate_location
                }
                errors {
                  field
                  messages
                }
              }
            }
            """,
            operation_name="update_address",
            variables={
                "data": {
                    "id": address["data"]["create_address"]["address"]["id"],
                    **ADDRESS_UPDATE_DATA["data"],
                },
            },
        )

        self.assertResponseNoErrors(response)
        self.assertDictEqual(response.data, ADDRESS_UPDATE_RESPONSE)

    def test_delete_address(self):
        address = self._create_address().data
        address_id = address["data"]["create_address"]["address"]["id"]
        delete_data = {"data": {"id": address_id}}
        response = self.query(
            """
            mutation delete_address($data: DeleteMutationInput!) {
              delete_address(input: $data) {
                id
              }
            }
            """,
            operation_name="delete_address",
            variables=delete_data,
        )

        self.assertResponseNoErrors(response)
        self.assertEqual(response.data["data"]["delete_address"]["id"], address_id)
        self.assertEqual(len(manager.Address.objects.all()), 0)


class TestParcel(GraphTestCase):
    def _create_parcel(self):
        return self.query(
            """
            mutation create_parcel($data: CreateParcelInput!) {
              create_parcel(input: $data) {
                parcel {
                  id
                  meta
                  width
                  height
                  length
                  dimension_unit
                  weight
                  weight_unit
                  packaging_type
                  package_preset
                }
                errors {
                  field
                  messages
                }
              }
            }
            """,
            operation_name="create_parcel",
            variables=PARCEL_DATA,
        )

    def test_create_parcel(self):
        response = self._create_parcel()

        self.assertResponseNoErrors(response)
        self.assertDictEqual(response.data, PARCEL_RESPONSE)

    def test_update_parcel(self):
        parcel = self._create_parcel().data
        response = self.query(
            """
            mutation update_parcel($data: UpdateParcelInput!) {
              update_parcel(input: $data) {
                parcel {
                  id
                  meta
                  width
                  height
                  length
                  dimension_unit
                  weight
                  weight_unit
                  packaging_type
                  package_preset
                }
                errors {
                  field
                  messages
                }
              }
            }
            """,
            operation_name="update_parcel",
            variables={
                "data": {
                    "id": parcel["data"]["create_parcel"]["parcel"]["id"],
                    **PARCEL_UPDATE_DATA["data"],
                },
            },
        )

        self.assertResponseNoErrors(response)
        self.assertDictEqual(response.data, PARCEL_UPDATE_RESPONSE)

    def test_delete_parcel(self):
        parcel = self._create_parcel().data
        parcel_id = parcel["data"]["create_parcel"]["parcel"]["id"]
        delete_data = {"data": {"id": parcel_id}}
        response = self.query(
            """
            mutation delete_parcel($data: DeleteMutationInput!) {
              delete_parcel(input: $data) {
                id
              }
            }
            """,
            operation_name="delete_parcel",
            variables=delete_data,
        )

        self.assertResponseNoErrors(response)
        self.assertEqual(response.data["data"]["delete_parcel"]["id"], parcel_id)
        self.assertEqual(len(manager.Parcel.objects.all()), 0)


ADDRESS_DATA = {
    "data": {
        "address_line1": "125 Church St",
        "person_name": "John Doe",
        "company_name": "A corp.",
        "phone_number": "514 000 0000",
        "city": "Moncton",
        "country_code": "CA",
        "postal_code": "E1C4Z8",
        "residential": False,
        "state_code": "NB",
        "meta": {"label": "Warehouse"},
    }
}

ADDRESS_RESPONSE = {
    "data": {
        "create_address": {
            "address": {
                "id": ANY,
                "meta": {"label": "Warehouse", "is_default": False},
                "company_name": "A corp.",
                "person_name": "John Doe",
                "address_line1": "125 Church St",
                "address_line2": None,
                "postal_code": "E1C4Z8",
                "residential": False,
                "city": "Moncton",
                "state_code": "NB",
                "country_code": "CA",
                "email": None,
                "phone_number": "+1 514-000-0000",
                "validation": None,
                "validate_location": None,
            },
            "errors": None,
        }
    }
}

ADDRESS_UPDATE_DATA = {
    "data": {
        "city": "Moncton",
        "email": "test@gmail.com",
        "person_name": "John Moe",
        "meta": {"label": "Warehouse Update"},
    }
}

ADDRESS_UPDATE_RESPONSE = {
    "data": {
        "update_address": {
            "address": {
                "id": ANY,
                "meta": {"label": "Warehouse Update", "is_default": False},
                "address_line1": "125 Church St",
                "address_line2": None,
                "city": "Moncton",
                "company_name": "A corp.",
                "country_code": "CA",
                "email": "test@gmail.com",
                "person_name": "John Moe",
                "phone_number": "+1 514-000-0000",
                "postal_code": "E1C4Z8",
                "residential": False,
                "state_code": "NB",
                "validate_location": None,
                "validation": None,
            },
            "errors": None,
        }
    }
}

PARCEL_DATA = {
    "data": {
        "weight": 1,
        "weight_unit": "KG",
        "package_preset": "canadapost_corrugated_small_box",
        "meta": {"label": "Purple Pack"},
    }
}

PARCEL_RESPONSE = {
    "data": {
        "create_parcel": {
            "errors": None,
            "parcel": {
                "id": ANY,
                "meta": {"label": "Purple Pack", "is_default": False},
                "dimension_unit": "CM",
                "height": 32.0,
                "length": 32.0,
                "package_preset": "canadapost_corrugated_small_box",
                "packaging_type": None,
                "weight": 1.0,
                "weight_unit": "KG",
                "width": 42.0,
            },
        }
    }
}

PARCEL_UPDATE_DATA = {
    "data": {
        "weight": 0.45,
        "weight_unit": "LB",
    }
}

PARCEL_UPDATE_RESPONSE = {
    "data": {
        "update_parcel": {
            "errors": None,
            "parcel": {
                "id": ANY,
                "meta": {"label": "Purple Pack", "is_default": False},
                "dimension_unit": "CM",
                "height": 32.0,
                "length": 32.0,
                "package_preset": "canadapost_corrugated_small_box",
                "packaging_type": None,
                "weight": 0.45,
                "weight_unit": "LB",
                "width": 42.0,
            },
        }
    }
}


class TestProduct(GraphTestCase):
    def _create_product(self):
        return self.query(
            """
            mutation create_product($data: CreateProductInput!) {
              create_product(input: $data) {
                product {
                  id
                  meta
                  weight
                  weight_unit
                  quantity
                  sku
                  title
                  hs_code
                  description
                  value_amount
                  value_currency
                  origin_country
                }
                errors {
                  field
                  messages
                }
              }
            }
            """,
            operation_name="create_product",
            variables=PRODUCT_DATA,
        )

    def test_create_product(self):
        response = self._create_product()

        self.assertResponseNoErrors(response)
        self.assertDictEqual(response.data, PRODUCT_RESPONSE)

    def test_update_product(self):
        product = self._create_product().data
        response = self.query(
            """
            mutation update_product($data: UpdateProductInput!) {
              update_product(input: $data) {
                product {
                  id
                  meta
                  weight
                  weight_unit
                  quantity
                  sku
                  title
                  hs_code
                  description
                  value_amount
                  value_currency
                  origin_country
                }
                errors {
                  field
                  messages
                }
              }
            }
            """,
            operation_name="update_product",
            variables={
                "data": {
                    "id": product["data"]["create_product"]["product"]["id"],
                    **PRODUCT_UPDATE_DATA["data"],
                },
            },
        )

        self.assertResponseNoErrors(response)
        self.assertDictEqual(response.data, PRODUCT_UPDATE_RESPONSE)

    def test_delete_product(self):
        product = self._create_product().data
        product_id = product["data"]["create_product"]["product"]["id"]
        delete_data = {"data": {"id": product_id}}
        response = self.query(
            """
            mutation delete_product($data: DeleteMutationInput!) {
              delete_product(input: $data) {
                id
              }
            }
            """,
            operation_name="delete_product",
            variables=delete_data,
        )

        self.assertResponseNoErrors(response)
        self.assertEqual(response.data["data"]["delete_product"]["id"], product_id)
        self.assertEqual(len(manager.Commodity.objects.filter(meta__label__isnull=False)), 0)


PRODUCT_DATA = {
    "data": {
        "weight": 1.5,
        "weight_unit": "KG",
        "quantity": 1,
        "sku": "TEST-SKU-001",
        "title": "Test Product Title",
        "hs_code": "123456",
        "description": "A test product",
        "value_amount": 99.99,
        "value_currency": "USD",
        "origin_country": "US",
        "meta": {"label": "Test Product"},
    }
}

PRODUCT_RESPONSE = {
    "data": {
        "create_product": {
            "errors": None,
            "product": {
                "id": ANY,
                "meta": {"label": "Test Product", "is_default": False},
                "weight": 1.5,
                "weight_unit": "KG",
                "quantity": 1,
                "sku": "TEST-SKU-001",
                "title": "Test Product Title",
                "hs_code": "123456",
                "description": "A test product",
                "value_amount": 99.99,
                "value_currency": "USD",
                "origin_country": "US",
            },
        }
    }
}

PRODUCT_UPDATE_DATA = {
    "data": {
        "weight": 2.0,
        "title": "Updated Title",
        "meta": {"label": "Updated Product"},
    }
}

PRODUCT_UPDATE_RESPONSE = {
    "data": {
        "update_product": {
            "errors": None,
            "product": {
                "id": ANY,
                "meta": {"label": "Updated Product", "is_default": False},
                "weight": 2.0,
                "weight_unit": "KG",
                "quantity": 1,
                "sku": "TEST-SKU-001",
                "title": "Updated Title",
                "hs_code": "123456",
                "description": "A test product",
                "value_amount": 99.99,
                "value_currency": "USD",
                "origin_country": "US",
            },
        }
    }
}
