import json
from unittest.mock import ANY
from purplship.server.graph.tests.base import GraphTestCase
import purplship.server.manager.models as manager
import purplship.server.graph.models as graph


class TestAddressTemplate(GraphTestCase):
    def _create_address_template(self):
        return self.query(
            """
            mutation create_template($data: CreateTemplateInput!) {
              create_template(input: $data) {
                id
                is_default
                label
                address {
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
            op_name="create_template",
            variables=ADDRESS_TEMPLATE_DATA,
        )

    def test_create_address_template(self):
        response = self._create_address_template()
        response_data = json.loads(response.content)

        self.assertResponseNoErrors(response)
        self.assertDictEqual(response_data, ADDRESS_TEMPLATE_RESPONSE)

    def test_update_address_template(self):
        template = json.loads(self._create_address_template().content)
        response = self.query(
            """
            mutation update_template($data: UpdateTemplateInput!) {
              update_template(input: $data) {
                id
                is_default
                label
                address {
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
            op_name="update_template",
            variables={
                **ADDRESS_TEMPLATE_UPDATE_DATA,
                "data": {
                    "id": template["data"]["create_template"]["id"],
                    **ADDRESS_TEMPLATE_UPDATE_DATA["data"],
                },
            },
        )
        response_data = json.loads(response.content)

        self.assertResponseNoErrors(response)
        self.assertDictEqual(response_data, ADDRESS_TEMPLATE_UPDATE_RESPONSE)

    def test_delete_address_template(self):
        template = json.loads(self._create_address_template().content)
        template_id = template["data"]["create_template"]["id"]
        delete_template_data = {"data": {"id": template_id}}
        response = self.query(
            """
            mutation delete_template($data: DeleteTemplateInput!) {
              delete_template(input: $data) {
                id
              }
            }
            """,
            op_name="delete_template",
            variables=delete_template_data,
        )
        response_data = json.loads(response.content)

        self.assertResponseNoErrors(response)
        self.assertEqual(response_data["data"]["delete_template"]["id"], template_id)
        self.assertEqual(len(graph.Template.objects.all()), 0)
        self.assertEqual(len(manager.Address.objects.all()), 0)


class TestParcelTemplate(GraphTestCase):
    def _create_parcel_template(self):
        return self.query(
            """
            mutation create_template($data: CreateTemplateInput!) {
              create_template(input: $data) {
                id
                is_default
                label
                parcel {
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
            op_name="create_template",
            variables=PARCEL_TEMPLATE_DATA,
        )

    def test_create_parcel_template(self):
        response = self._create_parcel_template()
        response_data = json.loads(response.content)

        self.assertResponseNoErrors(response)
        self.assertDictEqual(response_data, PARCEL_TEMPLATE_RESPONSE)

    def test_update_parcel_template(self):
        template = json.loads(self._create_parcel_template().content)
        response = self.query(
            """
            mutation update_template($data: UpdateTemplateInput!) {
              update_template(input: $data) {
                id
                is_default
                label
                parcel {
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
            op_name="update_template",
            variables={
                **PARCEL_TEMPLATE_UPDATE_DATA,
                "data": {
                    "id": template["data"]["create_template"]["id"],
                    **PARCEL_TEMPLATE_UPDATE_DATA["data"],
                },
            },
        )
        response_data = json.loads(response.content)

        self.assertResponseNoErrors(response)
        self.assertDictEqual(response_data, PARCEL_TEMPLATE_UPDATE_RESPONSE)

    def test_delete_parcel_template(self):
        template = json.loads(self._create_parcel_template().content)
        template_id = template["data"]["create_template"]["id"]
        delete_template_data = {"data": {"id": template_id}}
        response = self.query(
            """
            mutation delete_template($data: DeleteTemplateInput!) {
              delete_template(input: $data) {
                id
              }
            }
            """,
            op_name="delete_template",
            variables=delete_template_data,
        )
        response_data = json.loads(response.content)

        self.assertResponseNoErrors(response)
        self.assertEqual(response_data["data"]["delete_template"]["id"], template_id)
        self.assertEqual(len(graph.Template.objects.all()), 0)
        self.assertEqual(len(manager.Parcel.objects.all()), 0)


class TestCustomsTemplate(GraphTestCase):
    def _create_customs_info_template(self):
        return self.query(
            """
            mutation create_template($data: CreateTemplateInput!) {
              create_template(input: $data) {
                id
                label
                is_default
                customs {
                  aes
                  eel_pfc
                  incoterm
                  content_type
                  commercial_invoice
                  certificate_number
                  content_description
                  duty {
                    paid_by
                    currency
                    account_number
                    declared_value
                    bill_to {
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
                  }
                  invoice
                  signer
                  certify
                  commodities {
                    id
                    sku
                    weight
                    quantity
                    weight_unit
                    description
                    value_amount
                    value_currency
                    origin_country
                  }
                }
                errors {
                  field
                  messages
                }
              }
            }
            """,
            op_name="create_template",
            variables=CUSTOMS_TEMPLATE_DATA,
        )

    def test_create_customs_info_template(self):
        response = self._create_customs_info_template()
        response_data = json.loads(response.content)

        self.assertResponseNoErrors(response)
        self.assertDictEqual(response_data, CUSTOMS_TEMPLATE_RESPONSE)

    def test_update_customs_info_template(self):
        template = json.loads(self._create_customs_info_template().content)
        CUSTOMS_TEMPLATE_UPDATE_DATA["data"]["id"] = template["data"][
            "create_template"
        ]["id"]
        CUSTOMS_TEMPLATE_UPDATE_DATA["data"]["customs"]["commodities"][0]["id"] = next(
            c["id"]
            for c in template["data"]["create_template"]["customs"]["commodities"]
            if c["sku"]
            == template["data"]["create_template"]["customs"]["commodities"][0]["sku"]
        )

        response = self.query(
            """
            mutation update_template($data: UpdateTemplateInput!) {
              update_template(input: $data) {
                id
                is_default
                label
                customs {
                  aes
                  eel_pfc
                  incoterm
                  content_type
                  commercial_invoice
                  certificate_number
                  content_description
                  duty {
                    paid_by
                    currency
                    account_number
                    declared_value
                    bill_to {
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
                  }
                  invoice
                  signer
                  certify
                  commodities {
                    id
                    sku
                    weight
                    quantity
                    weight_unit
                    description
                    value_amount
                    value_currency
                    origin_country
                  }
                }
                errors {
                  field
                  messages
                }
              }
            }
            """,
            op_name="update_template",
            variables=CUSTOMS_TEMPLATE_UPDATE_DATA,
        )
        response_data = json.loads(response.content)

        self.assertResponseNoErrors(response)
        self.assertDictEqual(response_data, CUSTOMS_TEMPLATE_UPDATE_RESPONSE)

    def test_delete_customs_info(self):
        template = json.loads(self._create_customs_info_template().content)
        template_id = template["data"]["create_template"]["id"]
        delete_template_data = {"data": {"id": template_id}}
        response = self.query(
            """
            mutation delete_template($data: DeleteTemplateInput!) {
              delete_template(input: $data) {
                id
              }
            }
            """,
            op_name="delete_template",
            variables=delete_template_data,
        )
        response_data = json.loads(response.content)

        self.assertResponseNoErrors(response)
        self.assertEqual(response_data["data"]["delete_template"]["id"], template_id)
        self.assertEqual(len(graph.Template.objects.all()), 0)
        self.assertEqual(len(manager.Customs.objects.all()), 0)


ADDRESS_TEMPLATE_DATA = {
    "data": {
        "label": "Warehouse",
        "address": {
            "address_line1": "125 Church St",
            "person_name": "John Doe",
            "company_name": "A corp.",
            "phone_number": "514 000 0000",
            "city": "Moncton",
            "country_code": "CA",
            "postal_code": "E1C4Z8",
            "residential": False,
            "state_code": "NB",
        },
    }
}

ADDRESS_TEMPLATE_RESPONSE = {
    "data": {
        "create_template": {
            "address": {
                "address_line1": "125 Church St",
                "address_line2": None,
                "city": "Moncton",
                "company_name": "A corp.",
                "country_code": "CA",
                "email": None,
                "person_name": "John Doe",
                "phone_number": "+1 514-000-0000",
                "postal_code": "E1C4Z8",
                "residential": False,
                "state_code": "NB",
                "validate_location": None,
                "validation": None,
            },
            'errors': None,
            'id': ANY,
            'is_default': False,
            'label': 'Warehouse'
        }
    }
}

ADDRESS_TEMPLATE_UPDATE_DATA = {
    "data": {
        "label": "Warehouse Update",
        "address": {
            "city": "Moncton",
            "email": "test@gmail.com",
            "person_name": "John Moe",
        },
    }
}

ADDRESS_TEMPLATE_UPDATE_RESPONSE = {
    "data": {
        "update_template": {
            "address": {
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
            'id': ANY,
            'is_default': False,
            'label': 'Warehouse Update',
            'errors': None,
        }
    }
}

PARCEL_TEMPLATE_DATA = {
    "data": {
        "label": "Purple Pack",
        "parcel": {
            "weight": 1,
            "weight_unit": "KG",
            "package_preset": "canadapost_corrugated_small_box",
        },
    }
}

PARCEL_TEMPLATE_RESPONSE = {
    'data': {
        'create_template': {
            'errors': None,
            'id': ANY,
            'is_default': False,
            'label': 'Purple Pack',
            'parcel': {
                'dimension_unit': 'CM',
                'height': 32.0,
                'length': 32.0,
                'package_preset': 'canadapost_corrugated_small_box',
                'packaging_type': None,
                'weight': 1.0,
                'weight_unit': 'KG',
                'width': 42.0
            }
        }
    }
}

PARCEL_TEMPLATE_UPDATE_DATA = {
    "data": {
        "parcel": {
            "weight": 0.45,
            "weight_unit": "LB",
        }
    }
}

PARCEL_TEMPLATE_UPDATE_RESPONSE = {
    "data": {
        "update_template": {
            "errors": None,
            "id": ANY,
            "is_default": False,
            "label": "Purple Pack",
            "parcel": {
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

CUSTOMS_TEMPLATE_DATA = {
    "data": {
        "label": "Customs info template",
        "customs": {
            "content_type": "documents",
            "incoterm": "DDU",
            "commodities": [
                {"weight": 1.15, "weight_unit": "KG", "sku": "6787L8K7J8L7J8L7K8"},
                {
                    "weight": 0.75,
                    "weight_unit": "KG",
                    "sku": "3PO4I5J4PO5I4HI5OH4O5IH4IO5",
                    "quantity": 4,
                },
            ],
        },
    }
}

CUSTOMS_TEMPLATE_RESPONSE = {
    "data": {
        "create_template": {
            "customs": {
                "aes": None,
                "certificate_number": None,
                "certify": None,
                "commercial_invoice": None,
                "commodities": [
                    {
                        "description": None,
                        "id": ANY,
                        "origin_country": None,
                        "quantity": 4,
                        "sku": "3PO4I5J4PO5I4HI5OH4O5IH4IO5",
                        "value_amount": None,
                        "value_currency": None,
                        "weight": 0.75,
                        "weight_unit": "KG",
                    },
                    {
                        "description": None,
                        "id": ANY,
                        "origin_country": None,
                        "quantity": None,
                        "sku": "6787L8K7J8L7J8L7K8",
                        "value_amount": None,
                        "value_currency": None,
                        "weight": 1.15,
                        "weight_unit": "KG",
                    },
                ],
                "content_description": None,
                "content_type": "documents",
                "duty": None,
                "eel_pfc": None,
                "incoterm": "DDU",
                "invoice": None,
                "signer": None,
            },
            'id': ANY,
            'is_default': False,
            'label': 'Customs info template',
            'errors': None,
        }
    }
}

CUSTOMS_TEMPLATE_UPDATE_DATA = {
    "data": {
        "customs": {
            "commodities": [
                {
                    "weight": 1,
                    "weight_unit": "LB",
                }
            ],
            "duty": '{"paid_by": "SENDER"}',
        }
    }
}

CUSTOMS_TEMPLATE_UPDATE_RESPONSE = {
    "data": {
        "update_template": {
            "id": ANY,
            "is_default": False,
            "label": "Customs info template",
            "customs": {
                "aes": None,
                "eel_pfc": None,
                "incoterm": "DDU",
                "content_type": "documents",
                "commercial_invoice": None,
                "certificate_number": None,
                "content_description": None,
                "duty": {
                    "account_number": None,
                    "bill_to": None,
                    "currency": None,
                    "declared_value": None,
                    "paid_by": "SENDER",
                },
                "invoice": None,
                "signer": None,
                "certify": None,
                "commodities": [
                    {
                        "id": ANY,
                        "sku": "3PO4I5J4PO5I4HI5OH4O5IH4IO5",
                        "weight": 1.0,
                        "quantity": 4,
                        "weight_unit": "LB",
                        "description": None,
                        "value_amount": None,
                        "value_currency": None,
                        "origin_country": None,
                    },
                    {
                        "id": ANY,
                        "sku": "6787L8K7J8L7J8L7K8",
                        "weight": 1.15,
                        "quantity": None,
                        "weight_unit": "KG",
                        "description": None,
                        "value_amount": None,
                        "value_currency": None,
                        "origin_country": None,
                    },
                ],
            },
            "errors": None,
        }
    }
}
