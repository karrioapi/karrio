from unittest.mock import ANY
from karrio.server.graph.tests.base import GraphTestCase
import karrio.server.manager.models as manager
import karrio.server.graph.models as graph


class TestAddressTemplate(GraphTestCase):
    def _create_address_template(self):
        return self.query(
            """
            mutation create_address_template($data: CreateAddressTemplateInput!) {
              create_address_template(input: $data) {
                template {
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
                }
                errors {
                  field
                  messages
                }
              }
            }
            """,
            operation_name="create_address_template",
            variables=ADDRESS_TEMPLATE_DATA,
        )

    def test_create_address_template(self):
        response = self._create_address_template()
        self.assertResponseNoErrors(response)
        self.assertDictEqual(response.data, ADDRESS_TEMPLATE_RESPONSE)

    def test_update_address_template(self):
        template = self._create_address_template().data
        response = self.query(
            """
            mutation update_address_template($data: UpdateAddressTemplateInput!) {
              update_address_template(input: $data) {
                template {
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
                }
                errors {
                  field
                  messages
                }
              }
            }
            """,
            operation_name="update_address_template",
            variables={
                "data": {
                    "id": template["data"]["create_address_template"]["template"]["id"],
                    **ADDRESS_TEMPLATE_UPDATE_DATA["data"],
                },
            },
        )
        response_data = response.data

        self.assertResponseNoErrors(response)
        self.assertDictEqual(response_data, ADDRESS_TEMPLATE_UPDATE_RESPONSE)

    def test_delete_address_template(self):
        template = self._create_address_template().data
        template_id = template["data"]["create_address_template"]["template"]["id"]
        delete_template_data = {"data": {"id": template_id}}
        response = self.query(
            """
            mutation delete_template($data: DeleteMutationInput!) {
              delete_template(input: $data) {
                id
              }
            }
            """,
            operation_name="delete_template",
            variables=delete_template_data,
        )
        response_data = response.data

        self.assertResponseNoErrors(response)
        self.assertEqual(response_data["data"]["delete_template"]["id"], template_id)
        self.assertEqual(len(graph.Template.objects.all()), 0)
        self.assertEqual(len(manager.Address.objects.all()), 0)


class TestParcelTemplate(GraphTestCase):
    def _create_parcel_template(self):
        return self.query(
            """
            mutation create_parcel_template($data: CreateParcelTemplateInput!) {
              create_parcel_template(input: $data) {
                template {
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
                }
                errors {
                  field
                  messages
                }
              }
            }
            """,
            operation_name="create_parcel_template",
            variables=PARCEL_TEMPLATE_DATA,
        )

    def test_create_parcel_template(self):
        response = self._create_parcel_template()
        response_data = response.data

        self.assertResponseNoErrors(response)
        self.assertDictEqual(response_data, PARCEL_TEMPLATE_RESPONSE)

    def test_update_parcel_template(self):
        template = self._create_parcel_template().data
        response = self.query(
            """
            mutation update_parcel_template($data: UpdateParcelTemplateInput!) {
              update_parcel_template(input: $data) {
                template {
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
                }
                errors {
                  field
                  messages
                }
              }
            }
            """,
            operation_name="update_parcel_template",
            variables={
                "data": {
                    "id": template["data"]["create_parcel_template"]["template"]["id"],
                    **PARCEL_TEMPLATE_UPDATE_DATA["data"],
                },
            },
        )
        response_data = response.data

        self.assertResponseNoErrors(response)
        self.assertDictEqual(response_data, PARCEL_TEMPLATE_UPDATE_RESPONSE)

    def test_delete_parcel_template(self):
        template = self._create_parcel_template().data
        template_id = template["data"]["create_parcel_template"]["template"]["id"]
        delete_template_data = {"data": {"id": template_id}}
        response = self.query(
            """
            mutation delete_template($data: DeleteMutationInput!) {
              delete_template(input: $data) {
                id
              }
            }
            """,
            operation_name="delete_template",
            variables=delete_template_data,
        )
        response_data = response.data

        self.assertResponseNoErrors(response)
        self.assertEqual(response_data["data"]["delete_template"]["id"], template_id)
        self.assertEqual(len(graph.Template.objects.all()), 0)
        self.assertEqual(len(manager.Parcel.objects.all()), 0)


class TestCustomsTemplate(GraphTestCase):
    def _create_customs_info_template(self):
        return self.query(
            """
            mutation create_customs_template($data: CreateCustomsTemplateInput!) {
              create_customs_template(input: $data) {
                template {
                  id
                  label
                  is_default
                  customs {
                    incoterm
                    content_type
                    commercial_invoice
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
                }
                errors {
                  field
                  messages
                }
              }
            }
            """,
            operation_name="create_customs_template",
            variables=CUSTOMS_TEMPLATE_DATA,
        )

    def test_create_customs_info_template(self):
        response = self._create_customs_info_template()
        response_data = response.data

        self.assertResponseNoErrors(response)
        self.assertDictEqual(response_data, CUSTOMS_TEMPLATE_RESPONSE)

    def test_update_customs_info_template(self):
        template = self._create_customs_info_template().data
        CUSTOMS_TEMPLATE_UPDATE_DATA["data"]["id"] = template["data"][
            "create_customs_template"
        ]["template"]["id"]
        CUSTOMS_TEMPLATE_UPDATE_DATA["data"]["customs"]["commodities"][0]["id"] = next(
            c["id"]
            for c in template["data"]["create_customs_template"]["template"]["customs"][
                "commodities"
            ]
            if c["sku"]
            == template["data"]["create_customs_template"]["template"]["customs"][
                "commodities"
            ][0]["sku"]
        )

        response = self.query(
            """
            mutation update_customs_template($data: UpdateCustomsTemplateInput!) {
              update_customs_template(input: $data) {
                template {
                  id
                  is_default
                  label
                  customs {
                    incoterm
                    content_type
                    commercial_invoice
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
                }
                errors {
                  field
                  messages
                }
              }
            }
            """,
            operation_name="update_customs_template",
            variables=CUSTOMS_TEMPLATE_UPDATE_DATA,
        )
        response_data = response.data

        self.assertResponseNoErrors(response)
        self.assertDictEqual(response_data, CUSTOMS_TEMPLATE_UPDATE_RESPONSE)

    def test_delete_customs_info(self):
        template = self._create_customs_info_template().data
        template_id = template["data"]["create_customs_template"]["template"]["id"]
        delete_template_data = {"data": {"id": template_id}}
        response = self.query(
            """
            mutation delete_template($data: DeleteMutationInput!) {
              delete_template(input: $data) {
                id
              }
            }
            """,
            operation_name="delete_template",
            variables=delete_template_data,
        )
        response_data = response.data

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
        "create_address_template": {
            "template": {
                "id": ANY,
                "is_default": False,
                "label": "Warehouse",
                "address": {
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
            },
            "errors": None,
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
        "update_address_template": {
            "template": {
                "id": ANY,
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
                "id": ANY,
                "is_default": False,
                "label": "Warehouse Update",
            },
            "errors": None,
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
    "data": {
        "create_parcel_template": {
            "errors": None,
            "template": {
                "id": ANY,
                "is_default": False,
                "label": "Purple Pack",
                "parcel": {
                    "dimension_unit": "CM",
                    "height": 32.0,
                    "length": 32.0,
                    "package_preset": "canadapost_corrugated_small_box",
                    "packaging_type": None,
                    "weight": 1.0,
                    "weight_unit": "KG",
                    "width": 42.0,
                },
            },
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
        "update_parcel_template": {
            "errors": None,
            "template": {
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
                    "sku": "3PO4I5J4PO5I4HI5OH",
                    "quantity": 4,
                },
            ],
        },
    }
}

CUSTOMS_TEMPLATE_RESPONSE = {
    "data": {
        "create_customs_template": {
            "template": {
                "id": ANY,
                "label": "Customs info template",
                "is_default": False,
                "customs": {
                    "incoterm": "DDU",
                    "content_type": "documents",
                    "commercial_invoice": None,
                    "content_description": None,
                    "duty": None,
                    "invoice": None,
                    "signer": None,
                    "certify": None,
                    "commodities": [
                        {
                            "id": ANY,
                            "sku": "6787L8K7J8L7J8L7K8",
                            "weight": 1.15,
                            "quantity": 1,
                            "weight_unit": "KG",
                            "description": None,
                            "value_amount": None,
                            "value_currency": None,
                            "origin_country": None,
                        },
                        {
                            "id": ANY,
                            "sku": "3PO4I5J4PO5I4HI5OH",
                            "weight": 0.75,
                            "quantity": 4,
                            "weight_unit": "KG",
                            "description": None,
                            "value_amount": None,
                            "value_currency": None,
                            "origin_country": None,
                        },
                    ],
                },
            },
            "errors": None,
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
            "duty": {"paid_by": "sender"},
        }
    }
}

CUSTOMS_TEMPLATE_UPDATE_RESPONSE = {
    "data": {
        "update_customs_template": {
            "template": {
                "id": ANY,
                "is_default": False,
                "label": "Customs info template",
                "customs": {
                    "incoterm": "DDU",
                    "content_type": "documents",
                    "commercial_invoice": None,
                    "content_description": None,
                    "duty": {
                        "paid_by": "sender",
                        "currency": None,
                        "account_number": None,
                        "declared_value": None,
                        "bill_to": None,
                    },
                    "invoice": None,
                    "signer": None,
                    "certify": None,
                    "commodities": [
                        {
                            "id": ANY,
                            "sku": "6787L8K7J8L7J8L7K8",
                            "weight": 1.0,
                            "quantity": 1,
                            "weight_unit": "LB",
                            "description": None,
                            "value_amount": None,
                            "value_currency": None,
                            "origin_country": None,
                        },
                        {
                            "id": ANY,
                            "sku": "3PO4I5J4PO5I4HI5OH",
                            "weight": 0.75,
                            "quantity": 4,
                            "weight_unit": "KG",
                            "description": None,
                            "value_amount": None,
                            "value_currency": None,
                            "origin_country": None,
                        },
                    ],
                },
            },
            "errors": None,
        }
    }
}
