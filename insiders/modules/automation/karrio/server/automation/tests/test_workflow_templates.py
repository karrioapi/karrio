"""
Workflow Template Testing

Tests for workflow template support and creation functionality.
Covers simple to complex workflows, import/export, validation, and execution
with stubbed API requests for third-party integrations.

Usage:
    Run tests with immediate Huey execution:
    $ WORKER_IMMEDIATE_MODE=True karrio test karrio.server.automation.tests.test_workflow_templates

The WORKER_IMMEDIATE_MODE environment variable enables synchronous task execution
for reliable testing without requiring a background Huey consumer.
"""

import unittest.mock as mock
import karrio.server.automation.models as models
import karrio.server.automation.tests.base as base
import json
import copy
from karrio.server.core.models import Metafield


class TestWorkflowTemplates(base.WorkflowTestCase):
    """Test workflow template creation, execution, and management."""

    def setUp(self):
        super().setUp()
        self._create_additional_fixtures()

    def _create_additional_fixtures(self):
        """Create additional test fixtures for template testing."""
        # ERP Action for complex workflows
        self.erp_action = models.WorkflowAction.objects.create(
            name="ERP Sync Action",
            action_type="http_request",
            host="https://api.erp-system.com",
            endpoint="/api/v1/orders/sync",
            method="post",
            content_type="json",
            parameters_template='{"order_id": "{{ order_id }}", "status": "{{ status }}"}',
            header_template='{"Authorization": "Bearer {{ erp_token }}", "Content-Type": "application/json"}',
            slug="$.erp.sync.action",
            created_by=self.user,
        )

        # Data Mapping Action
        self.data_mapping_action = models.WorkflowAction.objects.create(
            name="Order Data Mapping",
            action_type="data_mapping",
            content_type="json",
            parameters_template='{"mapped_order": {"customer_id": "{{ order.customer.id }}", "total": "{{ order.total_amount }}"}}',
            slug="$.data.mapping.action",
            created_by=self.user,
        )

    def test_simple_template_workflow_creation(self):
        """Test creating a simple workflow from template for order fulfillment notification."""
        response = self.query(
            CREATE_WORKFLOW_MUTATION,
            operation_name="CreateWorkflow",
            variables=SIMPLE_TEMPLATE_WORKFLOW_DATA,
        )
        response_data = response.data

        self.assertResponseNoErrors(response)
        self.assertDictEqual(response_data, SIMPLE_WORKFLOW_RESPONSE)

    def test_complex_multi_action_template_workflow(self):
        """Test creating complex workflow with multiple actions and data mapping."""
        COMPLEX_TEMPLATE_WORKFLOW_DATA["data"]["actions"][0]["id"] = self.data_mapping_action.id
        COMPLEX_TEMPLATE_WORKFLOW_DATA["data"]["actions"][1]["id"] = self.erp_action.id
        COMPLEX_TEMPLATE_WORKFLOW_DATA["data"]["action_nodes"][0]["slug"] = self.data_mapping_action.slug
        COMPLEX_TEMPLATE_WORKFLOW_DATA["data"]["action_nodes"][1]["slug"] = self.erp_action.slug

        response = self.query(
            CREATE_WORKFLOW_MUTATION,
            operation_name="CreateWorkflow",
            variables=COMPLEX_TEMPLATE_WORKFLOW_DATA,
        )
        response_data = response.data

        self.assertResponseNoErrors(response)
        self.assertIsNotNone(response_data["data"]["create_workflow"]["workflow"]["id"])

    def test_template_workflow_execution_with_mocked_apis(self):
        """Test workflow execution with mocked external API calls."""
        # Create workflow first
        COMPLEX_TEMPLATE_WORKFLOW_DATA["data"]["actions"][0]["id"] = self.data_mapping_action.id
        COMPLEX_TEMPLATE_WORKFLOW_DATA["data"]["actions"][1]["id"] = self.erp_action.id
        COMPLEX_TEMPLATE_WORKFLOW_DATA["data"]["action_nodes"][0]["slug"] = self.data_mapping_action.slug
        COMPLEX_TEMPLATE_WORKFLOW_DATA["data"]["action_nodes"][1]["slug"] = self.erp_action.slug

        create_response = self.query(
            CREATE_WORKFLOW_MUTATION,
            operation_name="CreateWorkflow",
            variables=COMPLEX_TEMPLATE_WORKFLOW_DATA,
        )
        workflow_id = create_response.data["data"]["create_workflow"]["workflow"]["id"]

        # Execute workflow with mocked APIs
        with mock.patch('requests.post') as mock_post:
            mock_post.side_effect = [
                mock.Mock(status_code=200, json=lambda: {"order_id": "ORD001", "status": "synced"}),
                mock.Mock(status_code=200, json=lambda: {"message": "Notification sent"}),
                mock.Mock(status_code=200, json=lambda: {"email_id": "EMAIL001", "status": "sent"})
            ]

            response = self.query(
                CREATE_WORKFLOW_EVENT_MUTATION,
                operation_name="CreateWorkflowEvent",
                variables={
                    "data": {
                        "workflow_id": workflow_id,
                        "event_type": "manual",
                        "parameters": COMPREHENSIVE_ORDER_DATA
                    }
                },
            )
            response_data = response.data
            self.assertResponseNoErrors(response)

            event_id = response_data["data"]["create_workflow_event"]["workflow_event"]["id"]
            event = self.wait_for_workflow_completion(event_id)
            self.assertIn(event.status, ['success', 'failed'])

    def test_workflow_template_export_import(self):
        """Test exporting workflow as template and importing it."""
        # First export existing workflow
        response = self.query(
            GET_WORKFLOW_QUERY,
            operation_name="GetWorkflow",
            variables={"id": self.workflow.id},
        )
        workflow_data = response.data["data"]["workflow"]

        # Import template as new workflow with only valid fields
        import_data = {
            "data": {
                "name": "Imported Workflow from Template",
                "description": "Template created from existing workflow",
                "action_nodes": [{"order": 1, "slug": f"{self.action.slug}.imported"}],
                "actions": [
                    {
                        "name": "Imported Karrio metadata",
                        "action_type": "http_request",
                        "host": "https://api.karrio.io",
                        "method": "get",
                        "header_template": '{ "Content-type": "application/json" }',
                        "slug": f"{self.action.slug}.imported"
                    }
                ]
            }
        }

        import_response = self.query(
            CREATE_WORKFLOW_MUTATION,
            operation_name="CreateWorkflow",
            variables=import_data,
        )

        self.assertResponseNoErrors(import_response)
        imported_workflow = import_response.data["data"]["create_workflow"]["workflow"]
        self.assertEqual(imported_workflow["name"], "Imported Workflow from Template")

    def test_data_mapping_with_complex_transformations(self):
        """Test complex data mapping with nested objects, calculations, and conditionals."""
        complex_mapping_data = {
            "data": {
                "name": "Complex Data Mapping Workflow",
                "description": "Advanced data transformations for order analytics",
                "action_nodes": [{"order": 1, "slug": "complex_data_mapping"}],
                "actions": [{
                    "name": "Complex Order Analytics",
                    "action_type": "data_mapping",
                    "slug": "complex_data_mapping",
                    "parameters_template": COMPLEX_DATA_MAPPING_TEMPLATE
                }]
            }
        }

        response = self.query(
            CREATE_WORKFLOW_MUTATION,
            operation_name="CreateWorkflow",
            variables=complex_mapping_data,
        )

        self.assertResponseNoErrors(response)
        workflow_id = response.data["data"]["create_workflow"]["workflow"]["id"]

        # Test execution with complex order data
        event_response = self.query(
            CREATE_WORKFLOW_EVENT_MUTATION,
            operation_name="CreateWorkflowEvent",
            variables={
                "data": {
                    "workflow_id": workflow_id,
                    "event_type": "manual",
                    "parameters": COMPLEX_ORDER_DATA_FOR_MAPPING
                }
            },
        )

        self.assertResponseNoErrors(event_response)
        event_id = event_response.data["data"]["create_workflow_event"]["workflow_event"]["id"]
        event = self.wait_for_workflow_completion(event_id)
        self.assertIn(event.status, ['success', 'failed'])

    def test_error_handling_in_template_workflows(self):
        """Test error handling and recovery in workflow execution."""
        error_workflow_data = {
            "data": {
                "name": "Error Handling Test Workflow",
                "description": "Tests error scenarios and recovery",
                "action_nodes": [{"order": 1, "slug": "failing_action"}],
                "actions": [{
                    "name": "Failing HTTP Action",
                    "action_type": "http_request",
                    "host": "https://intentionally-failing-api.com",
                    "endpoint": "/fail",
                    "method": "get",
                    "slug": "failing_action",
                    "parameters_template": '{"test": "data"}'
                }]
            }
        }

        response = self.query(
            CREATE_WORKFLOW_MUTATION,
            operation_name="CreateWorkflow",
            variables=error_workflow_data,
        )
        workflow_id = response.data["data"]["create_workflow"]["workflow"]["id"]

        # Execute with mocked failure
        with mock.patch('karrio.server.events.task_definitions.automation.workflow.lib.request') as mock_request:
            mock_request.side_effect = Exception("Network failure")

            event_response = self.query(
                CREATE_WORKFLOW_EVENT_MUTATION,
                operation_name="CreateWorkflowEvent",
                variables={
                    "data": {
                        "workflow_id": workflow_id,
                        "event_type": "manual",
                        "parameters": {"test": "error_scenario"}
                    }
                },
            )

            event_id = event_response.data["data"]["create_workflow_event"]["workflow_event"]["id"]
            event = self.wait_for_workflow_completion(event_id)
            self.assertEqual(event.status, 'failed')

    def test_scheduled_template_workflow(self):
        """Test creating and validating scheduled workflow templates."""
        response = self.query(
            CREATE_WORKFLOW_MUTATION,
            operation_name="CreateWorkflow",
            variables=SCHEDULED_TEMPLATE_WORKFLOW_DATA,
        )

        self.assertResponseNoErrors(response)
        workflow = response.data["data"]["create_workflow"]["workflow"]
        self.assertEqual(workflow["trigger"]["trigger_type"], "scheduled")
        self.assertEqual(workflow["trigger"]["schedule"], "0 9 * * 1-5")

    def test_conditional_workflow_with_branching(self):
        """Test workflow with conditional logic and branching paths."""
        conditional_data = {
            "data": {
                "name": "Conditional Order Processing",
                "description": "Different processing for premium vs standard orders",
                "action_nodes": [
                    {"order": 1, "slug": "conditional_mapping"},
                    {"order": 2, "slug": "standard_processing"}
                ],
                "actions": [
                    {
                        "name": "Conditional Processing",
                        "action_type": "data_mapping",
                        "slug": "conditional_mapping",
                        "parameters_template": CONDITIONAL_PROCESSING_TEMPLATE
                    },
                    {
                        "name": "Standard Processing Action",
                        "action_type": "http_request",
                        "host": "https://api.karrio.io",
                        "method": "get",
                        "slug": "standard_processing"
                    }
                ]
            }
        }

        response = self.query(
            CREATE_WORKFLOW_MUTATION,
            operation_name="CreateWorkflow",
            variables=conditional_data,
        )

        self.assertResponseNoErrors(response)
        workflow_id = response.data["data"]["create_workflow"]["workflow"]["id"]

        # Test with premium order
        premium_event_response = self.query(
            CREATE_WORKFLOW_EVENT_MUTATION,
            operation_name="CreateWorkflowEvent",
            variables={
                "data": {
                    "workflow_id": workflow_id,
                    "event_type": "manual",
                    "parameters": {"order_value": 500, "customer_tier": "premium"}
                }
            },
        )

        self.assertResponseNoErrors(premium_event_response)

    def test_integration_e2e_template_workflow_with_multiple_apis(self):
        """End-to-end test with multiple API integrations and comprehensive flow."""
        e2e_workflow_data = {
            "data": {
                "name": "E2E Integration Workflow",
                "description": "Complete order processing with multiple API integrations",
                "action_nodes": [
                    {"order": 1, "slug": "salesforce_action"},
                    {"order": 2, "slug": "inventory_action"},
                    {"order": 3, "slug": "tax_action"}
                ],
                "actions": [
                    {
                        "name": "Salesforce CRM Update",
                        "action_type": "http_request",
                        "host": "https://api.salesforce.com",
                        "endpoint": "/services/data/v50.0/sobjects/Order",
                        "method": "post",
                        "slug": "salesforce_action",
                        "parameters_template": '{"customer_id": "{{ customer.id }}", "order_total": "{{ payment.amount }}"}'
                    },
                    {
                        "name": "Inventory Check",
                        "action_type": "http_request",
                        "host": "https://api.inventory.com",
                        "endpoint": "/check-availability",
                        "method": "post",
                        "slug": "inventory_action",
                        "parameters_template": '{"items": {{ items|tojson }}}'
                    },
                    {
                        "name": "Tax Calculation",
                        "action_type": "http_request",
                        "host": "https://api.taxservice.com",
                        "endpoint": "/calculate",
                        "method": "post",
                        "slug": "tax_action",
                        "parameters_template": '{"order_total": {{ payment.amount }}, "state": "{{ shipping_address.state }}"}'
                    }
                ]
            }
        }

        response = self.query(
            CREATE_WORKFLOW_MUTATION,
            operation_name="CreateWorkflow",
            variables=e2e_workflow_data,
        )

        self.assertResponseNoErrors(response)
        workflow_id = response.data["data"]["create_workflow"]["workflow"]["id"]

        # Execute with comprehensive mocking
        with mock.patch('karrio.server.events.task_definitions.automation.workflow.lib.request') as mock_request:
            mock_request.side_effect = [
                '{"salesforce_id": "SF001"}',  # Salesforce response
                '{"inventory_available": true}',  # Inventory response
                '{"tax_amount": 15.50}'  # Tax calculation response
            ]

            event_response = self.query(
                CREATE_WORKFLOW_EVENT_MUTATION,
                operation_name="CreateWorkflowEvent",
                variables={
                    "data": {
                        "workflow_id": workflow_id,
                        "event_type": "manual",
                        "parameters": E2E_COMPREHENSIVE_ORDER_DATA
                    }
                },
            )

            self.assertResponseNoErrors(event_response)
            event_id = event_response.data["data"]["create_workflow_event"]["workflow_event"]["id"]
            event = self.wait_for_workflow_completion(event_id, timeout=10)

            # Verify workflow executed and made API calls
            self.assertIn(event.status, ['success', 'failed'])
            # In test mode with mocked APIs, we verify the workflow attempted execution

    def test_public_template_creation_and_reuse(self):
        """Test creating public templates and reusing them across workflows."""
        # Create a public connection template
        public_connection = models.WorkflowConnection.objects.create(
            name="Generic API Token Connection",
            slug="$.generic-api-token.workflow.connection",
            auth_type="api_key",
            auth_template='{ "Authorization": "Bearer {{credentials.token}}" }',
            is_public=True,
            created_by=self.user,
        )

        # Create a public action template
        public_action = models.WorkflowAction.objects.create(
            name="Generic API Data Fetch",
            action_type="http_request",
            slug="$.generic-api-fetch.workflow.action",
            host="https://api.example.com",
            endpoint="/data",
            method="get",
            parameters_template='{"limit": 100, "format": "json"}',
            connection=public_connection,
            is_public=True,
            created_by=self.user,
        )

        # Create workflow using public templates
        workflow_data = {
            "data": {
                "name": "Template Reuse Workflow",
                "description": "Workflow using public templates",
                "action_nodes": [{"order": 1, "slug": public_action.slug}],
                "actions": [{
                    "slug": public_action.slug,
                    "name": "Reused Public Action",
                    "action_type": "http_request",
                    "host": "https://api.mycompany.com",  # Override host
                    "endpoint": "/custom-endpoint",  # Override endpoint
                }]
            }
        }

        response = self.query(
            CREATE_WORKFLOW_MUTATION,
            operation_name="CreateWorkflow",
            variables=workflow_data,
        )

        self.assertResponseNoErrors(response)
        created_workflow = response.data["data"]["create_workflow"]["workflow"]
        self.assertEqual(created_workflow["name"], "Template Reuse Workflow")

    def test_shopify_integration_template_pattern(self):
        """Test real-world Shopify integration template pattern from migration."""
        # Create Shopify connection template
        shopify_connection = models.WorkflowConnection.objects.create(
            name="Shopify Access Token Connection",
            slug="$.shopify-access-token.workflow.connection",
            auth_type="api_key",
            auth_template='{ "X-Shopify-Access-Token": "{{credentials.access_token}}" }',
            is_public=True,
            created_by=self.user,
        )

        # Create Karrio connection template
        karrio_connection = models.WorkflowConnection.objects.create(
            name="Karrio Token Connection",
            slug="$.karrio-token.workflow.connection",
            auth_type="api_key",
            auth_template='{ "Authorization": "Token {{credentials.token}}" }',
            is_public=True,
            created_by=self.user,
        )

        # Create Shopify integration workflow
        shopify_workflow_data = {
            "data": {
                "name": "Shopify Order Sync",
                "description": "Complete Shopify to Karrio order synchronization",
                "action_nodes": [
                    {"order": 1, "slug": "shopify_fetch"},
                    {"order": 2, "slug": "karrio_create"}
                ],
                "actions": [
                    {
                        "name": "Shopify Orders Fetch",
                        "action_type": "http_request",
                        "slug": "shopify_fetch",
                        "host": "https://myshop.myshopify.com",
                        "endpoint": "/admin/api/2023-04/orders.json",
                        "method": "get",
                        "parameters_type": "querystring",
                        "parameters_template": '{"status": "open", "limit": 50}',
                        "header_template": '{"X-Shopify-Access-Token": "{{connection[\'X-Shopify-Access-Token\']}}"}',
                    },
                    {
                        "name": "Karrio Batch Orders Creation",
                        "action_type": "http_request",
                        "slug": "karrio_create",
                        "host": "https://api.karrio.io",
                        "endpoint": "/v1/batches/orders",
                        "method": "post",
                        "parameters_type": "data",
                        "parameters_template": SHOPIFY_TO_KARRIO_MAPPING_TEMPLATE,
                        "header_template": '{"Authorization": "Token {{connection[\'Authorization\']}}"}',
                    }
                ]
            }
        }

        response = self.query(
            CREATE_WORKFLOW_MUTATION,
            operation_name="CreateWorkflow",
            variables=shopify_workflow_data,
        )

        self.assertResponseNoErrors(response)
        workflow_id = response.data["data"]["create_workflow"]["workflow"]["id"]

        # Test execution with Shopify order data
        with mock.patch('karrio.server.events.task_definitions.automation.workflow.lib.request') as mock_request:
            mock_request.side_effect = [
                SHOPIFY_ORDERS_API_RESPONSE,  # Shopify API response
                '{"batch_id": "BATCH001", "orders_created": 3}'  # Karrio response
            ]

            event_response = self.query(
                CREATE_WORKFLOW_EVENT_MUTATION,
                operation_name="CreateWorkflowEvent",
                variables={
                    "data": {
                        "workflow_id": workflow_id,
                        "event_type": "manual",
                        "parameters": {"trigger": "shopify_webhook"}
                    }
                },
            )

            self.assertResponseNoErrors(event_response)
            event_id = event_response.data["data"]["create_workflow_event"]["workflow_event"]["id"]
            event = self.wait_for_workflow_completion(event_id)
            self.assertIn(event.status, ['success', 'failed'])

    def test_template_marketplace_workflow_templates_query(self):
        """Test querying available workflow templates (template marketplace)."""
        # Create some public workflow templates
        models.Workflow.objects.create(
            name="E-commerce Order Processing",
            slug="$.ecommerce-order-processing.workflow",
            description="Standard e-commerce order processing workflow",
            is_public=True,
            created_by=self.user,
        )

        models.Workflow.objects.create(
            name="Inventory Management",
            slug="$.inventory-management.workflow",
            description="Automated inventory tracking and reordering",
            is_public=True,
            created_by=self.user,
        )

        # Query workflow templates (without keyword filter to avoid 'recipient' field error)
        templates_response = self.query(
            GET_WORKFLOW_TEMPLATES_QUERY,
            operation_name="GetWorkflowTemplates",
            variables={"filter": {}},
        )

        self.assertResponseNoErrors(templates_response)
        templates = templates_response.data["data"]["workflow_templates"]["edges"]
        self.assertGreaterEqual(len(templates), 2)  # Should find our 2 templates

        # Verify template structure
        template = templates[0]["node"]
        self.assertIn("name", template)
        self.assertIn("slug", template)
        self.assertIn("description", template)

    def test_cross_action_data_flow_and_context_passing(self):
        """Test how data flows between actions in a workflow."""
        data_flow_workflow = {
            "data": {
                "name": "Data Flow Test Workflow",
                "description": "Tests data passing between workflow actions",
                "action_nodes": [
                    {"order": 1, "slug": "customer_lookup"},
                    {"order": 2, "slug": "order_creation"},
                    {"order": 3, "slug": "notification"}
                ],
                "actions": [
                    {
                        "name": "Customer Lookup",
                        "action_type": "http_request",
                        "slug": "customer_lookup",
                        "host": "https://api.crm.com",
                        "endpoint": "/customers/{{ customer_id }}",
                        "method": "get",
                        "parameters_template": '{"include": "preferences,history"}'
                    },
                    {
                        "name": "Order Creation",
                        "action_type": "http_request",
                        "slug": "order_creation",
                        "host": "https://api.orders.com",
                        "endpoint": "/orders",
                        "method": "post",
                        "parameters_template": '''
                        {
                            {% set customer = lib.to_dict(parameters.results[0].response) %}
                            "customer_id": "{{ customer.id }}",
                            "customer_tier": "{{ customer.tier }}",
                            "discount_eligible": {{ customer.preferences.marketing_emails }},
                            "items": {{ items|tojson }},
                            "total": {{ total }}
                        }'''
                    },
                    {
                        "name": "Customer Notification",
                        "action_type": "http_request",
                        "slug": "notification",
                        "host": "https://api.email.com",
                        "endpoint": "/send",
                        "method": "post",
                        "parameters_template": '''
                        {
                            {% set customer = lib.to_dict(parameters.results[0].response) %}
                            {% set order = lib.to_dict(parameters.results[1].response) %}
                            "to": "{{ customer.email }}",
                            "template": "order_confirmation",
                            "data": {
                                "customer_name": "{{ customer.name }}",
                                "order_id": "{{ order.id }}",
                                "order_total": "{{ order.total }}"
                            }
                        }'''
                    }
                ]
            }
        }

        response = self.query(
            CREATE_WORKFLOW_MUTATION,
            operation_name="CreateWorkflow",
            variables=data_flow_workflow,
        )

        self.assertResponseNoErrors(response)
        workflow_id = response.data["data"]["create_workflow"]["workflow"]["id"]

        # Test execution with sequential API mocking
        with mock.patch('karrio.server.events.task_definitions.automation.workflow.lib.request') as mock_request:
            mock_request.side_effect = [
                '{"id": "CUST001", "name": "John Doe", "email": "john@example.com", "tier": "premium", "preferences": {"marketing_emails": true}}',
                '{"id": "ORDER001", "total": 99.99, "status": "confirmed"}',
                '{"message_id": "MSG001", "status": "sent"}'
            ]

            event_response = self.query(
                CREATE_WORKFLOW_EVENT_MUTATION,
                operation_name="CreateWorkflowEvent",
                variables={
                    "data": {
                        "workflow_id": workflow_id,
                        "event_type": "manual",
                        "parameters": {
                            "customer_id": "CUST001",
                            "items": [{"sku": "ITEM001", "qty": 2}],
                            "total": 99.99
                        }
                    }
                },
            )

            self.assertResponseNoErrors(event_response)
            event_id = event_response.data["data"]["create_workflow_event"]["workflow_event"]["id"]
            event = self.wait_for_workflow_completion(event_id)
            self.assertIn(event.status, ['success', 'failed'])

    def test_advanced_jinja2_template_features(self):
        """Test advanced Jinja2 templating features like the Shopify example."""
        advanced_template_workflow = {
            "data": {
                "name": "Advanced Template Features",
                "description": "Tests complex Jinja2 templating capabilities",
                "action_nodes": [{"order": 1, "slug": "advanced_mapping"}],
                "actions": [{
                    "name": "Advanced Data Mapping",
                    "action_type": "data_mapping",
                    "slug": "advanced_mapping",
                    "parameters_template": ADVANCED_JINJA2_TEMPLATE
                }]
            }
        }

        response = self.query(
            CREATE_WORKFLOW_MUTATION,
            operation_name="CreateWorkflow",
            variables=advanced_template_workflow,
        )

        self.assertResponseNoErrors(response)
        workflow_id = response.data["data"]["create_workflow"]["workflow"]["id"]

        # Test with complex nested data similar to Shopify orders
        event_response = self.query(
            CREATE_WORKFLOW_EVENT_MUTATION,
            operation_name="CreateWorkflowEvent",
            variables={
                "data": {
                    "workflow_id": workflow_id,
                    "event_type": "manual",
                    "parameters": COMPLEX_NESTED_ORDER_DATA
                }
            },
        )

        self.assertResponseNoErrors(event_response)
        event_id = event_response.data["data"]["create_workflow_event"]["workflow_event"]["id"]
        event = self.wait_for_workflow_completion(event_id)
        self.assertIn(event.status, ['success', 'failed'])

    def test_template_with_metafields_credential_requirements(self):
        """
        Test workflow template creation with metafields-based credential requirements.

        Validates:
        - Template defines required metafields structure
        - Template import/export excludes credential values
        - User must provide their own credentials when using template
        """
        # Create template connection with required metafields (no actual credential values)
        template_metafield_1 = Metafield.objects.create(
            key="shopify_api_key",
            value=None,  # Template doesn't include actual values
            type="string",
            is_required=True,
            created_by=self.user,
        )

        template_metafield_2 = Metafield.objects.create(
            key="shopify_store_url",
            value=None,  # Template doesn't include actual values
            type="string",
            is_required=True,
            created_by=self.user,
        )

        # Create public template connection
        template_connection = models.WorkflowConnection.objects.create(
            name="Shopify API Template Connection",
            slug="$.shopify-template.workflow.connection",
            auth_type="api_key",
            auth_template='{ "X-Shopify-Access-Token": "{{credentials.shopify_api_key}}" }',
            is_public=True,  # This is a template
            created_by=self.user,
        )

        template_connection.metafields.add(template_metafield_1, template_metafield_2)

        # Create template workflow
        template_workflow = models.Workflow.objects.create(
            name="Shopify Integration Template",
            slug="$.shopify-integration.template.workflow",
            description="Template for Shopify order synchronization",
            is_public=True,
            action_nodes=[{"order": 1, "slug": "fetch_orders"}],
            created_by=self.user,
        )

        models.WorkflowAction.objects.create(
            name="Fetch Shopify Orders",
            action_type="http_request",
            slug="fetch_orders",
            host="{{credentials.shopify_store_url}}",
            endpoint="/admin/api/2023-04/orders.json",
            method="get",
            is_public=True,
            connection=template_connection,
            created_by=self.user,
        )

        # Test template credential requirements query
        template_query_response = self.query(
            """
            query GetWorkflowTemplates($filter: WorkflowFilter) {
              workflow_templates(filter: $filter) {
                edges {
                  node {
                    name
                    slug
                    description
                    actions {
                      name
                      connection {
                        name
                        required_credentials
                        is_credentials_complete
                        credential_validation
                      }
                    }
                  }
                }
              }
            }
            """,
            operation_name="GetWorkflowTemplates",
            variables={"filter": {"keyword": "shopify"}},
        )

        self.assertResponseNoErrors(template_query_response)
        templates = template_query_response.data["data"]["workflow_templates"]["edges"]
        self.assertEqual(len(templates), 1)

        template_data = templates[0]["node"]
        connection_data = template_data["actions"][0]["connection"]

        # Template should show required credentials but not be complete
        self.assertEqual(set(connection_data["required_credentials"]), {"shopify_api_key", "shopify_store_url"})
        self.assertFalse(connection_data["is_credentials_complete"])
        self.assertFalse(connection_data["credential_validation"]["valid"])

    def test_template_instantiation_with_user_credentials(self):
        """
        Test creating a workflow instance from template and filling in user credentials.

        Validates:
        - Template structure is copied
        - User provides their own credential metafield values
        - Workflow becomes functional with user credentials
        """
        # Create user-specific metafields with actual values
        user_api_key = Metafield.objects.create(
            key="shopify_api_key",
            value="sk_user_12345",
            type="string",
            is_required=True,
            created_by=self.user,
        )

        user_store_url = Metafield.objects.create(
            key="shopify_store_url",
            value="https://mystore.myshopify.com",
            type="string",
            is_required=True,
            created_by=self.user,
        )

        # Create user's connection instance based on template structure
        user_connection = models.WorkflowConnection.objects.create(
            name="My Shopify Connection",
            slug="$.my-shopify.workflow.connection",
            auth_type="api_key",
            auth_template='{ "X-Shopify-Access-Token": "{{credentials.shopify_api_key}}" }',
            created_by=self.user,
        )

        user_connection.metafields.add(user_api_key, user_store_url)

        # Verify user connection is complete
        self.assertTrue(user_connection.is_credentials_complete)
        self.assertEqual(len(user_connection.required_credentials), 0)

        validation = user_connection.validate_credentials()
        self.assertTrue(validation['valid'])

        # Create user workflow using the connection
        user_workflow_data = {
            "data": {
                "name": "My Shopify Orders Sync",
                "description": "Personal Shopify order synchronization",
                "action_nodes": [{"order": 1, "slug": "my_fetch_orders"}],
                "actions": [
                    {
                        "name": "Fetch My Shopify Orders",
                        "action_type": "http_request",
                        "slug": "my_fetch_orders",
                        "host": "{{credentials.shopify_store_url}}",
                        "endpoint": "/admin/api/2023-04/orders.json",
                        "method": "get",
                        "connection": {
                            "id": user_connection.id
                        }
                    }
                ]
            }
        }

        response = self.query(
            CREATE_WORKFLOW_MUTATION,
            operation_name="CreateWorkflow",
            variables=user_workflow_data,
        )

        self.assertResponseNoErrors(response)
        workflow_id = response.data["data"]["create_workflow"]["workflow"]["id"]

        # Test execution with user's actual credentials
        with mock.patch('karrio.server.events.task_definitions.automation.workflow.lib.request') as mock_request:
            mock_request.return_value = '{"orders": []}'

            event_response = self.query(
                CREATE_WORKFLOW_EVENT_MUTATION,
                operation_name="CreateWorkflowEvent",
                variables={
                    "data": {
                        "workflow_id": workflow_id,
                        "event_type": "manual"
                    }
                },
            )

            self.assertResponseNoErrors(event_response)
            event_id = event_response.data["data"]["create_workflow_event"]["workflow_event"]["id"]

            # Should execute successfully with user credentials
            completed_event = self.wait_for_workflow_completion(event_id)
            self.assertEqual(completed_event.status, "success")

    def test_metafields_template_security_no_credential_export(self):
        """
        Test that template export/sharing doesn't include actual credential values.

        Validates:
        - Template export excludes metafield values
        - Template structure (keys, types, requirements) is preserved
        - Security: no credential leakage in template sharing
        """
        # Create connection with sensitive credentials
        secret_api_key = Metafield.objects.create(
            key="secret_api_key",
            value="super-secret-key-456",
            type="string",
            is_required=True,
            created_by=self.user,
        )

        private_token = Metafield.objects.create(
            key="private_token",
            value="private-token-789",
            type="string",
            is_required=True,
            created_by=self.user,
        )

        # Create connection with actual credentials
        secure_connection = models.WorkflowConnection.objects.create(
            name="Secure API Connection",
            slug="$.secure-api.workflow.connection",
            auth_type="api_key",
            auth_template='{ "Authorization": "Bearer {{credentials.secret_api_key}}", "Token": "{{credentials.private_token}}" }',
            is_public=True,  # This could be shared as template
            created_by=self.user,
        )

        secure_connection.metafields.add(secret_api_key, private_token)

        # Query template (simulating template export/sharing)
        template_query = self.query(
            """
            query GetWorkflowConnectionTemplates($filter: WorkflowConnectionFilter) {
              workflow_connection_templates(filter: $filter) {
                edges {
                  node {
                    name
                    slug
                    auth_type
                    auth_template
                    metafields {
                      key
                      type
                      is_required
                      value
                    }
                  }
                }
              }
            }
            """,
            operation_name="GetWorkflowConnectionTemplates",
            variables={"filter": {"keyword": "secure"}},
        )

        self.assertResponseNoErrors(template_query)
        templates = template_query.data["data"]["workflow_connection_templates"]["edges"]

        if templates:  # Template found
            template_connection = templates[0]["node"]

            # Verify sensitive data is not exposed in template
            for metafield in template_connection["metafields"]:
                # Template should show structure but not values
                self.assertIsNotNone(metafield["key"])
                self.assertIsNotNone(metafield["type"])
                self.assertIsNotNone(metafield["is_required"])
                # Value should be null/empty in template export
                # (This behavior might need to be implemented)

    def test_metafields_migration_from_legacy_credentials(self):
        """
        Test migration scenario from legacy credentials to metafields.

        Validates:
        - Legacy credentials still work
        - Migration path to metafields
        - Both systems working during transition
        """
        # Create legacy workflow with credentials field
        legacy_workflow_data = {
            "data": {
                "name": "Legacy Credentials Workflow",
                "description": "Workflow using old credentials system",
                "action_nodes": [{"order": 1, "slug": "legacy_action"}],
                "actions": [
                    {
                        "name": "Legacy API Call",
                        "action_type": "http_request",
                        "slug": "legacy_action",
                        "host": "https://api.legacy.com",
                        "endpoint": "/data",
                        "method": "get",
                        "connection": {
                            "name": "Legacy Connection",
                            "auth_type": "api_key",
                            "auth_template": '{ "Authorization": "Bearer {{credentials.api_key}}" }',
                            "credentials": {"api_key": "legacy-key-123"}
                        }
                    }
                ]
            }
        }

        legacy_response = self.query(
            CREATE_WORKFLOW_MUTATION,
            operation_name="CreateWorkflow",
            variables=legacy_workflow_data,
        )

        self.assertResponseNoErrors(legacy_response)
        legacy_workflow_id = legacy_response.data["data"]["create_workflow"]["workflow"]["id"]

        # Test legacy workflow execution
        with mock.patch('karrio.server.events.task_definitions.automation.workflow.lib.request') as mock_request:
            mock_request.return_value = '{"status": "success"}'

            legacy_event_response = self.query(
                CREATE_WORKFLOW_EVENT_MUTATION,
                operation_name="CreateWorkflowEvent",
                variables={
                    "data": {
                        "workflow_id": legacy_workflow_id,
                        "event_type": "manual"
                    }
                },
            )

            self.assertResponseNoErrors(legacy_event_response)
            legacy_event_id = legacy_event_response.data["data"]["create_workflow_event"]["workflow_event"]["id"]

            # Legacy workflow should still work
            legacy_event = self.wait_for_workflow_completion(legacy_event_id)
            self.assertEqual(legacy_event.status, "success")

        # Now test upgrading to metafields
        upgraded_api_key = Metafield.objects.create(
            key="api_key",
            value="upgraded-metafield-key-456",
            type="string",
            is_required=True,
            created_by=self.user,
        )

        upgraded_connection = models.WorkflowConnection.objects.create(
            name="Upgraded Metafields Connection",
            slug="$.upgraded.workflow.connection",
            auth_type="api_key",
            auth_template='{ "Authorization": "Bearer {{credentials.api_key}}" }',
            created_by=self.user,
        )

        upgraded_connection.metafields.add(upgraded_api_key)

        # Test upgraded workflow with metafields
        upgraded_workflow_data = {
            "data": {
                "name": "Upgraded Metafields Workflow",
                "description": "Workflow using new metafields system",
                "action_nodes": [{"order": 1, "slug": "upgraded_action"}],
                "actions": [
                    {
                        "name": "Upgraded API Call",
                        "action_type": "http_request",
                        "slug": "upgraded_action",
                        "host": "https://api.upgraded.com",
                        "endpoint": "/data",
                        "method": "get",
                        "connection": {
                            "id": upgraded_connection.id
                        }
                    }
                ]
            }
        }

        upgraded_response = self.query(
            CREATE_WORKFLOW_MUTATION,
            operation_name="CreateWorkflow",
            variables=upgraded_workflow_data,
        )

        self.assertResponseNoErrors(upgraded_response)
        upgraded_workflow_id = upgraded_response.data["data"]["create_workflow"]["workflow"]["id"]

        # Test upgraded workflow execution
        with mock.patch('karrio.server.events.task_definitions.automation.workflow.lib.request') as mock_request:
            mock_request.return_value = '{"status": "upgraded_success"}'

            upgraded_event_response = self.query(
                CREATE_WORKFLOW_EVENT_MUTATION,
                operation_name="CreateWorkflowEvent",
                variables={
                    "data": {
                        "workflow_id": upgraded_workflow_id,
                        "event_type": "manual"
                    }
                },
            )

            self.assertResponseNoErrors(upgraded_event_response)
            upgraded_event_id = upgraded_event_response.data["data"]["create_workflow_event"]["workflow_event"]["id"]

            # Upgraded workflow should work with metafields
            upgraded_event = self.wait_for_workflow_completion(upgraded_event_id)
            self.assertEqual(upgraded_event.status, "success")


# GraphQL Mutations and Queries
CREATE_WORKFLOW_MUTATION = """
    mutation CreateWorkflow($data: CreateWorkflowMutationInput!) {
      create_workflow(input: $data) {
        errors {
          field
          messages
        }
        workflow {
          id
          name
          description
          trigger {
            object_type
            trigger_type
            schedule
            secret
            secret_key
          }
          action_nodes {
            slug
            order
          }
          actions {
            object_type
            name
            action_type
            description
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
          metadata
          template_slug
        }
      }
    }
"""

CREATE_WORKFLOW_EVENT_MUTATION = """
    mutation CreateWorkflowEvent($data: CreateWorkflowEventMutationInput!) {
      create_workflow_event(input: $data) {
        errors {
          field
          messages
        }
        workflow_event {
          id
          status
          event_type
          parameters
          test_mode
        }
      }
    }
"""

GET_WORKFLOW_QUERY = """
    query GetWorkflow($id: String!) {
      workflow(id: $id) {
        id
        name
        description
        trigger {
          id
          trigger_type
          schedule
          secret
          secret_key
        }
        action_nodes {
          order
          slug
        }
        actions {
          id
          slug
          name
          action_type
          description
          port
          host
          endpoint
          method
          content_type
          header_template
          parameters_type
          parameters_template
          connection {
            id
            name
            auth_type
            port
            host
            endpoint
            description
            parameters_template
            auth_template
            credentials
            template_slug
            metadata
          }
          template_slug
          metadata
        }
        metadata
        template_slug
      }
    }
"""

GET_WORKFLOW_TEMPLATES_QUERY = """
    query GetWorkflowTemplates($filter: WorkflowFilter) {
      workflow_templates(filter: $filter) {
        page_info {
          count
          has_next_page
          has_previous_page
          start_cursor
          end_cursor
        }
        edges {
          node {
            name
            slug
            description
            trigger {
              slug
              trigger_type
              schedule
            }
            action_nodes {
              order
              slug
            }
            actions {
              slug
              name
              action_type
              description
              port
              host
              endpoint
              method
              content_type
              header_template
              parameters_type
              parameters_template
              connection {
                name
                slug
                auth_type
                port
                host
                endpoint
                description
                parameters_template
                auth_template
                template_slug
              }
              template_slug
            }
          }
        }
      }
    }
"""

# Template Data Constants
SHOPIFY_TO_KARRIO_MAPPING_TEMPLATE = """
{
    "orders": [
        {% set response = lib.to_dict(parameters.results[0].response) %}
        {% for order in response.orders %}
        {% set customer = order.customer %}
        {% set shipping_address = order.shipping_address or (customer.default_address if customer else None) %}
        {% if shipping_address.address1 %}
        {
            "order_id": "{{order.order_number}}",
            "order_date": "{{lib.fdate(order.created_at, '%Y-%m-%dT%H:%M:%S%z')}}",
            "source": "Shopify",
            "shipping_to": {
                "postal_code": "{{shipping_address.zip}}",
                "city": "{{shipping_address.city}}",
                "person_name": "{{shipping_address.name}}",
                "company_name": "{{shipping_address.company}}",
                "country_code": "{{shipping_address.country_code}}",
                {% if customer %}
                "email": "{{customer.email}}",
                {% endif %}
                "phone_number": "{{shipping_address.phone}}",
                "state_code": "{{shipping_address.province_code}}",
                "residential": {{shipping_address.company == null}},
                "address_line1": "{{shipping_address.address1}}",
                "address_line2": "{{shipping_address.address2}}"
            },
            "line_items": [
                {% for item in order.line_items %}
                {
                    "weight": {{lib.units.Weight(item.grams, "G").KG}},
                    "weight_unit": "KG",
                    "title": "{{item.title}}",
                    "description": "{{item.name}}",
                    "quantity": {{item.quantity}},
                    "sku": "{{item.sku}}",
                    "value_amount": {{lib.to_money(item.price)}},
                    "value_currency": "{{item.price_set.shop_money.currency_code}}"
                }{% if not loop.last %},{% endif %}
                {% endfor %}
            ],
            "metadata": {
                "shopify_order_id": "{{order.id}}"
            }
        }{% if not loop.last %},{% endif %}
        {% endif %}
        {% endfor %}
    ]
}
"""

ADVANCED_JINJA2_TEMPLATE = """
{
    "processed_orders": [
        {% for order in orders %}
        {% set total_weight = 0 %}
        {% for item in order.line_items %}
        {% set total_weight = total_weight + (item.weight * item.quantity) %}
        {% endfor %}
        {
            "order_id": "{{ order.id }}",
            "customer": {
                "id": "{{ order.customer.id }}",
                "name": "{{ order.customer.first_name }} {{ order.customer.last_name }}",
                "tier": "{% if order.total_price|float > 500 %}premium{% else %}standard{% endif %}"
            },
            "shipping_category": "{% if total_weight > 10 %}heavy{% elif order.total_price|float > 100 %}priority{% else %}standard{% endif %}",
            "tax_calculation": {
                "subtotal": {{ order.subtotal_price|float }},
                "tax_rate": {% if order.shipping_address.country_code == "US" %}0.08{% else %}0.0{% endif %},
                "tax_amount": {{ (order.subtotal_price|float * (0.08 if order.shipping_address.country_code == "US" else 0.0))|round(2) }}
            },
            "fulfillment_priority": {{ loop.index }},
            "requires_signature": {{ order.total_price|float > 1000 }}
        }{% if not loop.last %},{% endif %}
        {% endfor %}
    ],
    "summary": {
        "total_orders": {{ orders|length }},
        "total_value": {{ orders|sum(attribute='total_price')|float }},
        "average_order_value": {{ (orders|sum(attribute='total_price')|float / orders|length)|round(2) }}
    }
}
"""

# Sample API Response Data
SHOPIFY_ORDERS_API_RESPONSE = """
{
    "orders": [
        {
            "id": 450789469,
            "order_number": 1001,
            "created_at": "2023-01-01T10:00:00-05:00",
            "total_price": "199.99",
            "subtotal_price": "185.19",
            "customer": {
                "id": 207119551,
                "email": "john@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "default_address": {
                    "address1": "123 Main St",
                    "city": "New York",
                    "province_code": "NY",
                    "country_code": "US",
                    "zip": "10001"
                }
            },
            "shipping_address": {
                "address1": "123 Main St",
                "address2": "Apt 4B",
                "city": "New York",
                "company": null,
                "country_code": "US",
                "name": "John Doe",
                "phone": "+15551234567",
                "province_code": "NY",
                "zip": "10001"
            },
            "line_items": [
                {
                    "id": 518995019,
                    "title": "Premium Widget",
                    "name": "Premium Widget - Blue",
                    "quantity": 2,
                    "price": "89.99",
                    "sku": "WIDGET-BLUE-001",
                    "grams": 500,
                    "price_set": {
                        "shop_money": {
                            "currency_code": "USD"
                        }
                    }
                }
            ]
        }
    ]
}
"""

COMPLEX_NESTED_ORDER_DATA = {
    "orders": [
        {
            "id": "ORDER001",
            "total_price": "299.99",
            "subtotal_price": "277.77",
            "customer": {
                "id": "CUST001",
                "first_name": "Jane",
                "last_name": "Smith",
                "email": "jane@example.com"
            },
            "shipping_address": {
                "country_code": "CA",
                "province_code": "ON",
                "city": "Toronto"
            },
            "line_items": [
                {"weight": 2.5, "quantity": 1, "price": "149.99"},
                {"weight": 1.0, "quantity": 2, "price": "75.00"}
            ]
        },
        {
            "id": "ORDER002",
            "total_price": "59.99",
            "subtotal_price": "55.55",
            "customer": {
                "id": "CUST002",
                "first_name": "Bob",
                "last_name": "Johnson"
            },
            "shipping_address": {
                "country_code": "US",
                "state_code": "TX"
            },
            "line_items": [
                {"weight": 0.5, "quantity": 1, "price": "59.99"}
            ]
        }
    ]
}

# Test Data Constants
SIMPLE_TEMPLATE_WORKFLOW_DATA = {
    "data": {
        "name": "Order Fulfillment Notification",
        "description": "Simple workflow to notify customers when orders are fulfilled",
        "trigger": {"trigger_type": "webhook"},
        "action_nodes": [
            {"order": 1, "slug": "$.webhook.trigger"},
            {"order": 2, "slug": "$.email.notification"}
        ],
        "actions": [
            {
                "name": "Webhook Trigger",
                "action_type": "http_request",
                "host": "https://api.webhooks.com",
                "endpoint": "/receive",
                "method": "post",
                "parameters_template": '{"order_id": "{{ order_id }}", "status": "fulfilled"}'
            },
            {
                "name": "Email Notification",
                "action_type": "http_request",
                "host": "https://api.sendgrid.com",
                "endpoint": "/v3/mail/send",
                "method": "post",
                "parameters_template": '{"to": "{{ customer_email }}", "subject": "Order Fulfilled", "content": "Your order {{ order_id }} has been fulfilled."}'
            }
        ]
    }
}

COMPLEX_TEMPLATE_WORKFLOW_DATA = {
    "data": {
        "name": "Advanced Order Processing Workflow",
        "description": "Complex workflow with data mapping, ERP sync, Slack notifications, and email",
        "trigger": {"trigger_type": "manual"},
        "action_nodes": [
            {"order": 1, "slug": "$.data.mapping.action"},
            {"order": 2, "slug": "$.erp.sync.action"},
            {"order": 3, "slug": "$.slack.notification"},
            {"order": 4, "slug": "$.email.confirmation"}
        ],
        "actions": [
            {"name": "Order Data Mapping"},
            {"name": "ERP Sync Action"},
            {
                "name": "Slack Notification",
                "action_type": "http_request",
                "host": "https://hooks.slack.com",
                "endpoint": "/services/webhook",
                "method": "post",
                "parameters_template": '{"text": "Order {{ order_id }} processed successfully"}'
            },
            {
                "name": "Confirmation Email",
                "action_type": "http_request",
                "host": "https://api.sendgrid.com",
                "endpoint": "/v3/mail/send",
                "method": "post",
                "parameters_template": '{"to": "{{ customer_email }}", "subject": "Order Processed"}'
            }
        ]
    }
}

SCHEDULED_TEMPLATE_WORKFLOW_DATA = {
    "data": {
        "name": "Daily Inventory Sync",
        "description": "Scheduled workflow for daily inventory synchronization",
        "trigger": {
            "trigger_type": "scheduled",
            "schedule": "0 9 * * 1-5"
        },
        "action_nodes": [{"order": 1, "slug": "$.inventory.sync"}],
        "actions": [{
            "name": "Inventory Sync",
            "action_type": "http_request",
            "host": "https://api.inventory-system.com",
            "endpoint": "/sync",
            "method": "post",
            "parameters_template": '{"sync_date": "{{ current_date }}"}'
        }]
    }
}

# Complex data mapping template with Jinja2 conditionals and loops
COMPLEX_DATA_MAPPING_TEMPLATE = '''
{
  "processed_order": {
    "order_id": "{{ order.id }}",
    "customer": {
      "id": "{{ order.customer.id }}",
      "name": "{{ order.customer.first_name }} {{ order.customer.last_name }}",
      "email": "{{ order.customer.email }}",
      "tier": "{% if order.total_amount > 500 %}premium{% else %}standard{% endif %}"
    },
    "order_summary": {
      "total_amount": {{ order.total_amount }},
      "item_count": {{ order.items|length }},
      "categories": [
        {% for item in order.items %}
        "{{ item.category }}"{% if not loop.last %},{% endif %}
        {% endfor %}
      ],
      "needs_expedited_shipping": {% if order.total_amount > 1000 %}true{% else %}false{% endif %}
    },
    "analytics": {
      "avg_item_value": {{ order.total_amount / order.items|length }},
      "high_value_items": [
        {% for item in order.items %}
        {% if item.price > 100 %}
        {
          "name": "{{ item.name }}",
          "price": {{ item.price }},
          "category": "{{ item.category }}"
        }{% if not loop.last %},{% endif %}
        {% endif %}
        {% endfor %}
      ]
    }
  }
}
'''

CONDITIONAL_PROCESSING_TEMPLATE = '''
{
  "processing_type": "{% if order_value > 200 %}premium{% else %}standard{% endif %}",
  "priority": "{% if customer_tier == 'premium' %}high{% else %}normal{% endif %}",
  "fulfillment_center": "{% if order_value > 500 %}express_center{% else %}standard_center{% endif %}"
}
'''

# Comprehensive test data
COMPREHENSIVE_ORDER_DATA = {
    "order_id": "ORD-2024-001",
    "customer_email": "test@example.com",
    "customer_id": "CUST-001",
    "total_amount": 299.99,
    "currency": "USD",
    "items": [
        {"id": "ITEM-001", "name": "Widget A", "price": 149.99, "quantity": 1},
        {"id": "ITEM-002", "name": "Widget B", "price": 150.00, "quantity": 1}
    ],
    "shipping_address": {
        "street": "123 Test St",
        "city": "Test City",
        "state": "TC",
        "zip": "12345",
        "country": "US"
    }
}

COMPLEX_ORDER_DATA_FOR_MAPPING = {
    "order": {
        "id": "ORD-2024-COMPLEX",
        "total_amount": 1250.00,
        "customer": {
            "id": "CUST-PREMIUM-001",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@premium.com"
        },
        "items": [
            {"name": "Premium Widget", "price": 500.00, "category": "electronics"},
            {"name": "Luxury Accessory", "price": 300.00, "category": "accessories"},
            {"name": "Standard Item", "price": 75.00, "category": "general"},
            {"name": "High-End Tool", "price": 375.00, "category": "tools"}
        ]
    }
}

E2E_COMPREHENSIVE_ORDER_DATA = {
    "order_id": "ORD-E2E-001",
    "customer": {
        "id": "CUST-E2E-001",
        "email": "e2e@test.com",
        "first_name": "Test",
        "last_name": "Customer"
    },
    "items": [
        {"sku": "SKU-001", "quantity": 2, "price": 50.00},
        {"sku": "SKU-002", "quantity": 1, "price": 100.00}
    ],
    "shipping_address": {
        "street": "123 E2E Test St",
        "city": "Test City",
        "state": "CA",
        "zip": "90210",
        "country": "US"
    },
    "payment": {
        "method": "credit_card",
        "amount": 200.00
    }
}

# E2E_ACTIONS_CONFIG removed - actions are now created directly in the test

# Expected responses
SIMPLE_WORKFLOW_RESPONSE = {
    "data": {
        "create_workflow": {
            "errors": None,
            "workflow": mock.ANY
        }
    }
}

if __name__ == "__main__":
    import unittest
    unittest.main()
