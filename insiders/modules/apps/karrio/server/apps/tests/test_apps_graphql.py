from unittest.mock import ANY

import karrio.lib as lib
from oauth2_provider.models import Application
from karrio.server.graph.tests.base import GraphTestCase
from karrio.server.apps.models import OAuthApp, AppInstallation


class TestOAuthAppGraphQLAPI(GraphTestCase):
    """Test suite for OAuth App GraphQL CRUD operations."""

    def test_create_oauth_app(self):
        """Test OAuth app creation via GraphQL mutation."""
        response = self.query(
            CREATE_OAUTH_APP_MUTATION,
            operation_name="create_oauth_app",
            variables=CREATE_OAUTH_APP_VARIABLES,
        )

        self.assertResponseNoErrors(response)
        self.assertDictEqual(
            lib.to_dict(response.data),
            CREATE_OAUTH_APP_RESPONSE,
        )

        # Verify OAuth2 application was created with correct settings
        oauth_app = OAuthApp.objects.get(display_name="Test OAuth App")
        oauth2_app = oauth_app.registration
        self.assertEqual(
            oauth2_app.authorization_grant_type, Application.GRANT_AUTHORIZATION_CODE
        )
        self.assertEqual(oauth2_app.client_type, Application.CLIENT_CONFIDENTIAL)
        self.assertFalse(oauth2_app.skip_authorization)

    def test_query_oauth_apps(self):
        """Test querying OAuth apps."""
        # Create an OAuth app first
        self.query(CREATE_OAUTH_APP_MUTATION, variables=CREATE_OAUTH_APP_VARIABLES)

        response = self.query(
            QUERY_OAUTH_APPS,
            operation_name="query_oauth_apps",
        )

        self.assertResponseNoErrors(response)
        self.assertDictEqual(
            lib.to_dict(response.data),
            QUERY_OAUTH_APPS_RESPONSE,
        )

    def test_update_oauth_app(self):
        """Test updating an OAuth app."""
        # Create OAuth app first
        create_response = self.query(
            CREATE_OAUTH_APP_MUTATION, variables=CREATE_OAUTH_APP_VARIABLES
        )
        app_id = create_response.data["data"]["create_oauth_app"]["oauth_app"]["id"]

        # Update the OAuth app
        update_variables = {
            "data": {
                "id": app_id,
                "display_name": "Updated Test OAuth App",
                "launch_url": "https://updated.example.com/launch",
            }
        }

        response = self.query(
            UPDATE_OAUTH_APP_MUTATION,
            operation_name="update_oauth_app",
            variables=update_variables,
        )

        self.assertResponseNoErrors(response)
        self.assertDictEqual(
            lib.to_dict(response.data),
            UPDATE_OAUTH_APP_RESPONSE,
        )

    def test_delete_oauth_app(self):
        """Test deleting an OAuth app."""
        # Create OAuth app first
        create_response = self.query(
            CREATE_OAUTH_APP_MUTATION, variables=CREATE_OAUTH_APP_VARIABLES
        )
        app_id = create_response.data["data"]["create_oauth_app"]["oauth_app"]["id"]

        # Delete the OAuth app
        delete_variables = {"data": {"id": app_id}}

        response = self.query(
            DELETE_OAUTH_APP_MUTATION,
            operation_name="delete_oauth_app",
            variables=delete_variables,
        )

        self.assertResponseNoErrors(response)
        self.assertDictEqual(
            lib.to_dict(response.data),
            DELETE_OAUTH_APP_RESPONSE,
        )

        # Verify OAuth app is deleted
        self.assertFalse(OAuthApp.objects.filter(id=app_id).exists())


class TestAppInstallationGraphQLAPI(GraphTestCase):
    """Test suite for App Installation GraphQL CRUD operations."""

    def test_install_builtin_app(self):
        """Test installing a built-in app."""
        response = self.query(
            INSTALL_APP_MUTATION,
            operation_name="install_app",
            variables=INSTALL_BUILTIN_APP_VARIABLES,
        )

        self.assertResponseNoErrors(response)
        self.assertDictEqual(
            lib.to_dict(response.data),
            INSTALL_BUILTIN_APP_RESPONSE,
        )

        # Verify installation exists in database
        installation = AppInstallation.objects.get(app_id="shipping-optimizer")
        self.assertEqual(installation.app_type, "builtin")
        self.assertTrue(installation.is_active)
        self.assertIsNone(installation.oauth_app)

    def test_install_marketplace_app(self):
        """Test installing a marketplace app."""
        response = self.query(
            INSTALL_APP_MUTATION,
            operation_name="install_app",
            variables=INSTALL_MARKETPLACE_APP_VARIABLES,
        )

        self.assertResponseNoErrors(response)
        self.assertDictEqual(
            lib.to_dict(response.data),
            INSTALL_MARKETPLACE_APP_RESPONSE,
        )

    def test_install_private_app_with_oauth(self):
        """Test installing a private app that requires OAuth."""
        response = self.query(
            INSTALL_APP_MUTATION,
            operation_name="install_app",
            variables=INSTALL_PRIVATE_APP_WITH_OAUTH_VARIABLES,
        )

        self.assertResponseNoErrors(response)
        self.assertDictEqual(
            lib.to_dict(response.data),
            INSTALL_PRIVATE_APP_WITH_OAUTH_RESPONSE,
        )

        # Verify OAuth app was created
        installation = AppInstallation.objects.get(app_id="custom-integration")
        self.assertIsNotNone(installation.oauth_app)
        self.assertEqual(
            installation.oauth_app.display_name, "Custom Integration OAuth"
        )

    def test_query_app_installations(self):
        """Test querying app installations."""
        # Install a few apps
        self.query(INSTALL_APP_MUTATION, variables=INSTALL_BUILTIN_APP_VARIABLES)
        self.query(INSTALL_APP_MUTATION, variables=INSTALL_MARKETPLACE_APP_VARIABLES)

        response = self.query(
            QUERY_APP_INSTALLATIONS,
            operation_name="query_app_installations",
        )

        self.assertResponseNoErrors(response)
        self.assertDictEqual(
            lib.to_dict(response.data),
            QUERY_APP_INSTALLATIONS_RESPONSE,
        )

    def test_uninstall_app(self):
        """Test uninstalling an app."""
        # Install app first
        self.query(INSTALL_APP_MUTATION, variables=INSTALL_BUILTIN_APP_VARIABLES)

        # Uninstall the app
        uninstall_variables = {"data": {"app_id": "shipping-optimizer"}}

        response = self.query(
            UNINSTALL_APP_MUTATION,
            operation_name="uninstall_app",
            variables=uninstall_variables,
        )

        self.assertResponseNoErrors(response)
        self.assertDictEqual(
            lib.to_dict(response.data),
            UNINSTALL_APP_RESPONSE,
        )

        # Verify installation is completely deleted
        self.assertFalse(
            AppInstallation.objects.filter(
                app_id="shipping-optimizer", created_by=self.user
            ).exists()
        )

    def test_uninstall_app_by_installation_id(self):
        """Test uninstalling an app by installation ID."""
        # Install app first
        install_response = self.query(INSTALL_APP_MUTATION, variables=INSTALL_BUILTIN_APP_VARIABLES)
        installation_id = install_response.data["data"]["install_app"]["installation"]["id"]

        # Uninstall the app by installation_id
        uninstall_variables = {"data": {"installation_id": installation_id}}

        response = self.query(
            UNINSTALL_APP_MUTATION,
            operation_name="uninstall_app",
            variables=uninstall_variables,
        )

        self.assertResponseNoErrors(response)
        self.assertDictEqual(
            lib.to_dict(response.data),
            UNINSTALL_APP_RESPONSE,
        )

        # Verify installation is completely deleted
        self.assertFalse(
            AppInstallation.objects.filter(id=installation_id).exists()
        )

    def test_disable_enable_app_installation(self):
        """Test disabling and enabling an app installation (using is_active flag)."""
        # Install app first
        install_response = self.query(INSTALL_APP_MUTATION, variables=INSTALL_BUILTIN_APP_VARIABLES)
        installation_id = install_response.data["data"]["install_app"]["installation"]["id"]

        # Disable the app (set is_active = False)
        disable_variables = {
            "data": {
                "id": installation_id,
                "is_active": False
            }
        }

        response = self.query(
            UPDATE_APP_INSTALLATION_MUTATION,
            operation_name="update_app_installation",
            variables=disable_variables,
        )

        self.assertResponseNoErrors(response)

        # Verify installation is disabled but still exists
        installation = AppInstallation.objects.get(id=installation_id)
        self.assertFalse(installation.is_active)

        # Re-enable the app (set is_active = True)
        enable_variables = {
            "data": {
                "id": installation_id,
                "is_active": True
            }
        }

        response = self.query(
            UPDATE_APP_INSTALLATION_MUTATION,
            operation_name="update_app_installation",
            variables=enable_variables,
        )

        self.assertResponseNoErrors(response)

        # Verify installation is re-enabled
        installation.refresh_from_db()
        self.assertTrue(installation.is_active)

    def test_uninstall_app_validation_error(self):
        """Test uninstall validation - requires either app_id or installation_id."""
        # Try to uninstall without providing either app_id or installation_id
        uninstall_variables = {"data": {}}

        response = self.query(
            UNINSTALL_APP_MUTATION,
            operation_name="uninstall_app",
            variables=uninstall_variables,
        )

        # Should have validation error
        self.assertIn("errors", response.data["data"]["uninstall_app"])
        errors = response.data["data"]["uninstall_app"]["errors"]
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["field"], "input")
        self.assertIn("Either app_id or installation_id must be provided", errors[0]["messages"][0])

    def test_install_app_with_metafields(self):
        """Test installing an app with metafields configuration."""
        response = self.query(
            INSTALL_APP_WITH_METAFIELDS_MUTATION,
            operation_name="install_app_with_metafields",
            variables=INSTALL_APP_WITH_METAFIELDS_VARIABLES,
        )

        self.assertResponseNoErrors(response)

        # Verify installation was created with metafields
        installation = AppInstallation.objects.get(app_id="shipment-tracker")
        self.assertTrue(installation.is_active)

        # Verify metafields were created
        metafields = installation.metafields.all()
        self.assertEqual(len(metafields), 2)

        # Check metafield values
        metafield_dict = {mf.key: mf.value for mf in metafields}
        self.assertEqual(metafield_dict["api_key"], "test-api-key-123")
        self.assertEqual(metafield_dict["webhook_url"], "https://example.com/webhook")

    def test_update_app_installation_with_metafields(self):
        """Test updating an app installation with metafields."""
        # First install the app
        install_response = self.query(
            INSTALL_APP_MUTATION,
            variables=INSTALL_MARKETPLACE_APP_VARIABLES,
        )
        self.assertResponseNoErrors(install_response)

        installation_id = install_response.data["data"]["install_app"]["installation"]["id"]

        # Update with metafields
        update_variables = {
            "data": {
                "id": installation_id,
                "metafields": [
                    {
                        "key": "api_key",
                        "value": "updated-api-key-456",
                        "is_required": True,
                        "type": "text"
                    },
                    {
                        "key": "max_retries",
                        "value": "5",
                        "is_required": False,
                        "type": "number"
                    }
                ]
            }
        }

        response = self.query(
            UPDATE_APP_INSTALLATION_MUTATION,
            operation_name="update_app_installation",
            variables=update_variables,
        )

        self.assertResponseNoErrors(response)

        # Verify metafields were updated
        installation = AppInstallation.objects.get(id=installation_id)
        metafields = installation.metafields.all()
        metafield_dict = {mf.key: mf.value for mf in metafields}
        self.assertEqual(metafield_dict["api_key"], "updated-api-key-456")
        self.assertEqual(metafield_dict["max_retries"], "5")

    def test_app_installation_api_key_auto_generation(self):
        """Test that API key is auto-generated when installing an app."""
        print("Testing API key auto-generation on app installation")

        response = self.query(
            INSTALL_APP_MUTATION,
            operation_name="install_app",
            variables=INSTALL_BUILTIN_APP_VARIABLES,
        )

        self.assertResponseNoErrors(response)

        # Verify API key was auto-generated
        installation_data = response.data["data"]["install_app"]["installation"]
        self.assertIsNotNone(installation_data["api_key"])
        self.assertTrue(installation_data["api_key"].startswith("karrio_app_shipping-optimizer_"))

        # Verify in database
        installation = AppInstallation.objects.get(app_id="shipping-optimizer")
        self.assertIsNotNone(installation.api_key)
        self.assertEqual(installation.api_key, installation_data["api_key"])

    def test_rotate_app_api_key(self):
        """Test rotating an app's API key."""
        print("Testing API key rotation")

        # Install app first
        install_response = self.query(
            INSTALL_APP_MUTATION,
            variables=INSTALL_BUILTIN_APP_VARIABLES,
        )
        self.assertResponseNoErrors(install_response)

        installation_id = install_response.data["data"]["install_app"]["installation"]["id"]
        original_api_key = install_response.data["data"]["install_app"]["installation"]["api_key"]

        # Rotate the API key
        rotate_variables = {"data": {"id": installation_id}}

        response = self.query(
            ROTATE_APP_API_KEY_MUTATION,
            operation_name="rotate_app_api_key",
            variables=rotate_variables,
        )

        self.assertResponseNoErrors(response)

        # Verify new API key is different
        new_api_key = response.data["data"]["rotate_app_api_key"]["installation"]["api_key"]
        self.assertIsNotNone(new_api_key)
        self.assertNotEqual(original_api_key, new_api_key)
        self.assertTrue(new_api_key.startswith("karrio_app_shipping-optimizer_"))

        # Verify in database
        installation = AppInstallation.objects.get(id=installation_id)
        self.assertEqual(installation.api_key, new_api_key)

    def test_ensure_app_api_key_when_missing(self):
        """Test ensuring API key exists when it's missing."""
        print("Testing API key recreation when missing")

        # Install app first
        install_response = self.query(
            INSTALL_APP_MUTATION,
            variables=INSTALL_BUILTIN_APP_VARIABLES,
        )
        self.assertResponseNoErrors(install_response)

        installation_id = install_response.data["data"]["install_app"]["installation"]["id"]

        # Manually remove API key to simulate deletion
        installation = AppInstallation.objects.get(id=installation_id)
        installation.api_key = None
        installation.save()

        # Ensure API key
        ensure_variables = {"data": {"id": installation_id}}

        response = self.query(
            ENSURE_APP_API_KEY_MUTATION,
            operation_name="ensure_app_api_key",
            variables=ensure_variables,
        )

        self.assertResponseNoErrors(response)

        # Verify API key was recreated
        new_api_key = response.data["data"]["ensure_app_api_key"]["installation"]["api_key"]
        self.assertIsNotNone(new_api_key)
        self.assertTrue(new_api_key.startswith("karrio_app_shipping-optimizer_"))

        # Verify in database
        installation.refresh_from_db()
        self.assertEqual(installation.api_key, new_api_key)

    def test_api_key_updates_with_access_scopes(self):
        """Test that API key permissions are updated when access_scopes change."""
        print("Testing API key scope updates")

        # Install app first
        install_response = self.query(
            INSTALL_APP_MUTATION,
            variables=INSTALL_BUILTIN_APP_VARIABLES,
        )
        self.assertResponseNoErrors(install_response)

        installation_id = install_response.data["data"]["install_app"]["installation"]["id"]

        # Update access scopes
        update_variables = {
            "data": {
                "id": installation_id,
                "access_scopes": ["read", "write", "admin"]
            }
        }

        response = self.query(
            UPDATE_APP_INSTALLATION_MUTATION,
            operation_name="update_app_installation",
            variables=update_variables,
        )

        self.assertResponseNoErrors(response)

        # Verify access scopes were updated
        updated_scopes = response.data["data"]["update_app_installation"]["installation"]["access_scopes"]
        self.assertEqual(updated_scopes, ["read", "write", "admin"])

        # Verify in database
        installation = AppInstallation.objects.get(id=installation_id)
        self.assertEqual(installation.access_scopes, ["read", "write", "admin"])

    def test_api_key_uniqueness(self):
        """Test that API keys are unique across installations."""
        print("Testing API key uniqueness")

        # Install first app
        response1 = self.query(
            INSTALL_APP_MUTATION,
            variables=INSTALL_BUILTIN_APP_VARIABLES,
        )
        self.assertResponseNoErrors(response1)

        # Install second app with different app_id
        marketplace_variables = {
            "data": {
                "app_id": "shipment-tracker",
                "app_type": "marketplace",
                "access_scopes": ["read", "write"]
            }
        }

        response2 = self.query(
            INSTALL_APP_MUTATION,
            variables=marketplace_variables,
        )
        self.assertResponseNoErrors(response2)

        # Verify API keys are different
        api_key1 = response1.data["data"]["install_app"]["installation"]["api_key"]
        api_key2 = response2.data["data"]["install_app"]["installation"]["api_key"]

        self.assertNotEqual(api_key1, api_key2)
        self.assertTrue(api_key1.startswith("karrio_app_shipping-optimizer_"))
        self.assertTrue(api_key2.startswith("karrio_app_shipment-tracker_"))

# GraphQL Mutations and Queries

CREATE_OAUTH_APP_MUTATION = """
mutation create_oauth_app($data: CreateOAuthAppMutationInput!) {
    create_oauth_app(input: $data) {
        oauth_app {
            id
            display_name
            description
            launch_url
            redirect_uris
            client_id
            client_secret
            features
            created_at
            created_by {
                email
            }
        }
        errors {
            field
            messages
        }
    }
}
"""

UPDATE_OAUTH_APP_MUTATION = """
mutation update_oauth_app($data: UpdateOAuthAppMutationInput!) {
    update_oauth_app(input: $data) {
        oauth_app {
            id
            display_name
            launch_url
            redirect_uris
            features
        }
        errors {
            field
            messages
        }
    }
}
"""

DELETE_OAUTH_APP_MUTATION = """
mutation delete_oauth_app($data: DeleteOAuthAppMutationInput!) {
    delete_oauth_app(input: $data) {
        success
        errors {
            field
            messages
        }
    }
}
"""

QUERY_OAUTH_APPS = """
query query_oauth_apps {
    oauth_apps {
        edges {
            node {
                id
                display_name
                launch_url
                client_id
                features
                created_at
                created_by {
                    email
                }
            }
        }
    }
}
"""

INSTALL_APP_MUTATION = """
mutation install_app($data: InstallAppMutationInput!) {
    install_app(input: $data) {
        installation {
            id
            app_id
            app_type
            access_scopes
            api_key
            is_active
            requires_oauth
            created_at
        }
        errors {
            field
            messages
        }
    }
}
"""

UNINSTALL_APP_MUTATION = """
mutation uninstall_app($data: UninstallAppMutationInput!) {
    uninstall_app(input: $data) {
        success
        errors {
            field
            messages
        }
    }
}
"""

QUERY_APP_INSTALLATIONS = """
query query_app_installations {
    app_installations {
        edges {
            node {
                id
                app_id
                app_type
                is_active
                requires_oauth
                created_at
            }
        }
    }
}
"""

INSTALL_APP_WITH_METAFIELDS_MUTATION = """
mutation install_app_with_metafields($data: InstallAppMutationInput!) {
    install_app(input: $data) {
        installation {
            id
            app_id
            app_type
            access_scopes
            is_active
            requires_oauth
            created_at
            metafields {
                id
                key
                value
                is_required
                type
            }
        }
        errors {
            field
            messages
        }
    }
}
"""

UPDATE_APP_INSTALLATION_MUTATION = """
mutation update_app_installation($data: UpdateAppInstallationMutationInput!) {
    update_app_installation(input: $data) {
        installation {
            id
            app_id
            app_type
            access_scopes
            api_key
            is_active
            requires_oauth
            created_at
            metafields {
                id
                key
                value
                is_required
                type
            }
        }
        errors {
            field
            messages
        }
    }
}
"""

ROTATE_APP_API_KEY_MUTATION = """
mutation rotate_app_api_key($data: RotateAppApiKeyMutationInput!) {
    rotate_app_api_key(input: $data) {
        installation {
            id
            app_id
            api_key
        }
        errors {
            field
            messages
        }
    }
}
"""

ENSURE_APP_API_KEY_MUTATION = """
mutation ensure_app_api_key($data: EnsureAppApiKeyMutationInput!) {
    ensure_app_api_key(input: $data) {
        installation {
            id
            app_id
            api_key
        }
        errors {
            field
            messages
        }
    }
}
"""

# Test Variables

CREATE_OAUTH_APP_VARIABLES = {
    "data": {
        "display_name": "Test OAuth App",
        "description": "A test OAuth application",
        "launch_url": "https://example.com/launch",
        "redirect_uris": "https://example.com/oauth/callback",
        "features": ["api_access", "webhooks"],
    }
}

INSTALL_BUILTIN_APP_VARIABLES = {
    "data": {
        "app_id": "shipping-optimizer",
        "app_type": "builtin",
        "access_scopes": [],
    }
}

INSTALL_MARKETPLACE_APP_VARIABLES = {
    "data": {
        "app_id": "shipment-tracker",
        "app_type": "marketplace",
        "access_scopes": ["read:shipments"],
    }
}

INSTALL_PRIVATE_APP_WITH_OAUTH_VARIABLES = {
    "data": {
        "app_id": "custom-integration",
        "app_type": "private",
        "requires_oauth": True,
        "access_scopes": ["read:all", "write:all"],
        "oauth_app_data": {
            "display_name": "Custom Integration OAuth",
            "launch_url": "https://custom.example.com/launch",
            "redirect_uris": "https://custom.example.com/oauth/callback",
        },
    }
}

INSTALL_APP_WITH_METAFIELDS_VARIABLES = {
    "data": {
        "app_id": "shipment-tracker",
        "app_type": "marketplace",
        "access_scopes": ["read:shipments"],
        "metafields": [
            {
                "key": "api_key",
                "value": "test-api-key-123",
                "is_required": True,
                "type": "text"
            },
            {
                "key": "webhook_url",
                "value": "https://example.com/webhook",
                "is_required": False,
                "type": "text"
            }
        ]
    }
}

# Expected Responses

CREATE_OAUTH_APP_RESPONSE = {
    "data": {
        "create_oauth_app": {
            "oauth_app": {
                "id": ANY,
                "display_name": "Test OAuth App",
                "description": "A test OAuth application",
                "launch_url": "https://example.com/launch",
                "redirect_uris": "https://example.com/oauth/callback",
                "client_id": ANY,
                "client_secret": ANY,
                "features": ["api_access", "webhooks"],
                "created_at": ANY,
                "created_by": {
                    "email": ANY,
                },
            },
        }
    }
}

QUERY_OAUTH_APPS_RESPONSE = {
    "data": {
        "oauth_apps": {
            "edges": [
                {
                    "node": {
                        "id": ANY,
                        "display_name": "Test OAuth App",
                        "launch_url": "https://example.com/launch",
                        "client_id": ANY,
                        "features": ["api_access", "webhooks"],
                        "created_at": ANY,
                        "created_by": {
                            "email": ANY,
                        },
                    }
                }
            ]
        }
    }
}

UPDATE_OAUTH_APP_RESPONSE = {
    "data": {
        "update_oauth_app": {
            "oauth_app": {
                "id": ANY,
                "display_name": "Updated Test OAuth App",
                "launch_url": "https://updated.example.com/launch",
                "redirect_uris": "https://example.com/oauth/callback",
                "features": ["api_access", "webhooks"],
            },
        }
    }
}

DELETE_OAUTH_APP_RESPONSE = {
    "data": {
        "delete_oauth_app": {
            "success": True,
        }
    }
}

INSTALL_BUILTIN_APP_RESPONSE = {
    "data": {
        "install_app": {
            "installation": {
                "app_id": "shipping-optimizer",
                "app_type": "builtin",
                "api_key": ANY,
                "created_at": ANY,
                "id": ANY,
                "is_active": True,
                "requires_oauth": False,
            }
        }
    }
}

INSTALL_MARKETPLACE_APP_RESPONSE = {
    "data": {
        "install_app": {
            "installation": {
                "id": ANY,
                "app_id": "shipment-tracker",
                "app_type": "marketplace",
                "access_scopes": ["read:shipments"],
                "api_key": ANY,
                "is_active": True,
                "requires_oauth": False,
                "created_at": ANY,
            }
        }
    }
}

INSTALL_PRIVATE_APP_WITH_OAUTH_RESPONSE = {
    "data": {
        "install_app": {
            "installation": {
                "id": ANY,
                "app_id": "custom-integration",
                "app_type": "private",
                "access_scopes": ["read:all", "write:all"],
                "api_key": ANY,
                "is_active": True,
                "requires_oauth": True,
                "created_at": ANY,
            }
        }
    }
}

QUERY_APP_INSTALLATIONS_RESPONSE = {
    "data": {
        "app_installations": {
            "edges": [
                {
                    "node": {
                        "app_id": "shipment-tracker",
                        "app_type": "marketplace",
                        "created_at": ANY,
                        "id": ANY,
                        "is_active": True,
                        "requires_oauth": False,
                    }
                },
                {
                    "node": {
                        "app_id": "shipping-optimizer",
                        "app_type": "builtin",
                        "created_at": ANY,
                        "id": ANY,
                        "is_active": True,
                        "requires_oauth": False,
                    }
                },
            ]
        }
    }
}

UNINSTALL_APP_RESPONSE = {
    "data": {
        "uninstall_app": {
            "success": True,
        }
    }
}
