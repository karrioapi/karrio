import unittest.mock as mock
import karrio.server.automation.models as models
import karrio.server.automation.tests.base as base


class TestWorkflowAction(base.WorkflowTestCase):
    def test_query_workflow_actions(self):
        response = self.query(
            """
            query GetWorkflowActions($filter: WorkflowActionFilter) {
              workflow_actions(filter: $filter) {
                edges {
                  node {
                    name
                    description
                    object_type
                    action_type
                    port
                    host
                    endpoint
                    method
                    parameters_type
                    header_template
                    content_type
                    connection {
                      object_type
                      name
                      auth_type
                      port
                      host
                      endpoint
                      description
                      parameters_template
                      auth_template
                      credentials
                      metadata
                      template_slug
                    }
                    metadata
                    template_slug
                  }
                }
              }
            }
            """,
            operation_name="GetWorkflowActions",
        )
        response_data = response.data

        self.assertResponseNoErrors(response)
        self.assertEqual(response_data, WORKFLOW_ACTIONS)

    def test_create_workflow_action(self):
        response = self.query(
            """
            mutation CreateWorkflowAction($data: CreateWorkflowActionMutationInput!) {
              create_workflow_action(input: $data) {
                workflow_action {
                  name
                  description
                  object_type
                  action_type
                  port
                  host
                  endpoint
                  method
                  parameters_type
                  header_template
                  content_type
                  parameters_template
                  connection {
                    object_type
                    name
                    auth_type
                    port
                    host
                    endpoint
                    description
                    parameters_template
                    auth_template
                    credentials
                    metadata
                    template_slug
                  }
                  metadata
                  template_slug
                }
                errors {
                  field
                  messages
                }
              }
            }
            """,
            operation_name="CreateWorkflowAction",
            variables=CREATE_WORKFLOW_ACTION,
        )
        response_data = response.data

        self.assertResponseNoErrors(response)
        self.assertEqual(response_data, WORKFLOW_ACTION_RESPONSE)

    def test_update_workflow_action(self):
        UPDATE_WORKFLOW_ACTION["data"]["id"] = self.action.id
        response = self.query(
            """
            mutation UpdateWorkflowAction($data: UpdateWorkflowActionMutationInput!) {
              update_workflow_action(input: $data) {
                workflow_action {
                  name
                  description
                  object_type
                  action_type
                  port
                  host
                  endpoint
                  method
                  parameters_type
                  header_template
                  content_type
                  parameters_template
                  connection {
                    object_type
                    name
                    auth_type
                    port
                    host
                    endpoint
                    description
                    parameters_template
                    auth_template
                    credentials
                    metadata
                    template_slug
                  }
                  metadata
                  template_slug
                }
                errors {
                  field
                  messages
                }
              }
            }
            """,
            operation_name="UpdateWorkflowAction",
            variables=UPDATE_WORKFLOW_ACTION,
        )
        response_data = response.data

        self.assertResponseNoErrors(response)
        self.assertEqual(response_data, WORKFLOW_ACTION_UPDATE_RESPONSE)

    def test_delete_workflow_action(self):
        response = self.query(
            """
            mutation DeleteWorkflowAction($data: DeleteMutationInput!) {
              delete_workflow_action(input: $data) {
                id
                errors {
                  field
                  messages
                }
              }
            }
            """,
            operation_name="DeleteWorkflowAction",
            variables={"data": {"id": self.action.id}},
        )
        response_data = response.data

        self.assertResponseNoErrors(response)
        self.assertEqual(response_data, WORKFLOW_DELETE_RESPONSE)
        self.assertEqual(
            models.WorkflowAction.objects.filter(id=self.action.id).exists(), False
        )


WORKFLOW_ACTIONS = {
    "data": {
        "workflow_actions": {
            "edges": [
                {
                    "node": {
                        "action_type": "http_request",
                        "connection": None,
                        "content_type": None,
                        "description": None,
                        "endpoint": None,
                        "header_template": "{ "
                        '"Content-type": '
                        '"application/json" '
                        "}",
                        "host": "https://api.karrio.io",
                        "metadata": {},
                        "method": "get",
                        "name": "Karrio metadata",
                        "object_type": "workflow-action",
                        "parameters_type": None,
                        "port": None,
                        "template_slug": None,
                    }
                }
            ]
        }
    }
}

CREATE_WORKFLOW_ACTION = {
    "data": {
        "name": "Karrio reference",
        "action_type": "http_request",
        "host": "https://api.karrio.io",
        "endpoint": "/v1/reference",
        "parameters_type": "querystring",
        "method": "get",
        "parameters_template": '{"reduced": true }',
        "header_template": '{ "Content-type": "application/json" }',
    }
}

UPDATE_WORKFLOW_ACTION = {"data": {"name": "Karrio metadata updated"}}


WORKFLOW_ACTION_RESPONSE = {
    "data": {
        "create_workflow_action": {
            "errors": None,
            "workflow_action": {
                "action_type": "http_request",
                "connection": None,
                "content_type": None,
                "description": None,
                "endpoint": "/v1/reference",
                "parameters_template": '{"reduced": true }',
                "header_template": '{ "Content-type": "application/json" }',
                "host": "https://api.karrio.io",
                "metadata": {},
                "method": "get",
                "name": "Karrio reference",
                "object_type": "workflow-action",
                "parameters_type": "querystring",
                "port": None,
                "template_slug": None,
            },
        }
    }
}
WORKFLOW_ACTION_UPDATE_RESPONSE = {
    "data": {
        "update_workflow_action": {
            "errors": None,
            "workflow_action": {
                "action_type": "http_request",
                "connection": None,
                "content_type": None,
                "description": None,
                "endpoint": None,
                "header_template": "{ " '"Content-type": ' '"application/json" ' "}",
                "host": "https://api.karrio.io",
                "metadata": {},
                "method": "get",
                "name": "Karrio " "metadata " "updated",
                "object_type": "workflow-action",
                "parameters_template": None,
                "parameters_type": None,
                "port": None,
                "template_slug": None,
            },
        }
    }
}
WORKFLOW_DELETE_RESPONSE = {
    "data": {"delete_workflow_action": {"id": mock.ANY, "errors": None}}
}
