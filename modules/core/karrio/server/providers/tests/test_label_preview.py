from unittest import mock

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

import karrio.server.providers.models as providers
from karrio.server.user.models import Token
from karrio.server.core.middleware import CreatorAccess
from karrio.server.core.tests import APITestCase
from karrio.server.core.utils import ResourceAccessToken
from karrio.server.providers.views.carriers import CarrierLabelPreview, LABEL_PREVIEW_FAILED


class TestCarrierLabelPreviewAccess(APITestCase):
    """The label template preview of a generic connection is reached only by its owner,
    or through a resource token the owner minted. The test default access filter
    (`WideAccess`) filters nothing, so a per-owner filter is patched in.

    Rendering itself is broken for every connection on this version (it reads
    `carrier.label_template` and `carrier.custom_carrier_name`, which the connection
    no longer has), so the owner's request is asserted to reach rendering and to end
    in the fixed failure body, not in a PDF.
    """

    def setUp(self) -> None:
        super().setUp()
        self.victim = get_user_model().objects.create_user("victim@example.com", "test")
        self.intruder = get_user_model().objects.create_user("intruder@example.com", "test")
        self.connection = providers.CarrierConnection.objects.create(
            carrier_code="generic",
            carrier_id="victim-custom",
            test_mode=True,
            active=True,
            created_by=self.victim,
            credentials=dict(display_name="Victim Carrier", custom_carrier_name="victim_carrier"),
        )
        self.path = f"/v1/carriers/{self.connection.id}/label.pdf"
        self.client = APIClient()

        access = mock.patch("karrio.server.core.models.base.get_access_filter", CreatorAccess())
        access.start()
        self.addCleanup(access.stop)
        # Spy on rendering without changing it: shows whether a request got past the checks.
        render = mock.patch.object(
            CarrierLabelPreview, "_generate_label", autospec=True, side_effect=CarrierLabelPreview._generate_label
        )
        self.render = render.start()
        self.addCleanup(render.stop)

    def _as(self, user) -> None:
        token = Token.objects.create(user=user, test_mode=True)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def _mint(self):
        return self.client.post(
            "/api/tokens",
            {"resource_type": "carrier", "resource_ids": [self.connection.id], "access": ["label_preview"]},
            format="json",
        )

    def test_only_the_owner_reaches_rendering(self):
        self.client.credentials()
        anonymous = self.client.get(self.path)
        self._as(self.intruder)
        intruder = self.client.get(self.path)
        rendered_before_owner = self.render.call_count
        self._as(self.victim)
        owner = self.client.get(self.path)

        self.assertEqual(
            (anonymous.status_code, intruder.status_code, rendered_before_owner, self.render.call_count),
            (status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND, 0, 1),
        )
        self.assertEqual((owner.status_code, owner.json()), (status.HTTP_409_CONFLICT, LABEL_PREVIEW_FAILED))

    def test_a_failed_render_does_not_echo_the_exception(self):
        self._as(self.victim)
        with mock.patch.object(
            CarrierLabelPreview, "_generate_label", side_effect=RuntimeError("internal detail /etc/secret")
        ):
            response = self.client.get(self.path)

        self.assertEqual((response.status_code, response.json()), (status.HTTP_409_CONFLICT, LABEL_PREVIEW_FAILED))

    def test_a_token_minted_by_the_owner_reaches_rendering(self):
        self._as(self.victim)
        minted = self._mint()
        url = minted.data["resource_urls"][self.connection.id]

        self.client.credentials()
        response = self.client.get(url)

        self.assertEqual(
            (minted.status_code, response.status_code, self.render.call_count),
            (status.HTTP_201_CREATED, status.HTTP_409_CONFLICT, 1),
        )

    def test_another_tenant_cannot_mint_a_preview_token(self):
        self._as(self.intruder)

        self.assertEqual(self._mint().status_code, status.HTTP_404_NOT_FOUND)

    def test_a_token_for_another_resource_does_not_open_the_preview(self):
        token = ResourceAccessToken.for_resource(
            user=self.victim, resource_type="document", resource_ids=[self.connection.id], access=["batch_labels"]
        )

        self.client.credentials()
        response = self.client.get(self.path, {"token": str(token)})

        self.assertEqual((response.status_code, self.render.call_count), (status.HTTP_403_FORBIDDEN, 0))
