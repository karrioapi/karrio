import base64
import contextlib
import hashlib
from unittest import mock

from django.core.cache import cache
from django.db import connection
from django.test import override_settings
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authentication import TokenAuthentication as BaseTokenAuthentication
from rest_framework.test import APIClient, APIRequestFactory, APITestCase

from karrio.server.core.authentication import (
    TOKEN_REVOKED,
    TokenAuthentication,
    TokenBasicAuthentication,
    token_cache_key,
)
from karrio.server.user.models import Token

SHIPMENTS = "/v1/shipments"


@override_settings(TOKEN_AUTH_CACHE_TTL=300)
class TestTokenAuthCacheInvalidation(APITestCase):
    """A cached API-token authentication must not outlive a deactivated user or a
    deleted token. Real signal dispatch: the user and token are saved and deleted
    through the ORM, no handler is called directly."""

    def setUp(self):
        cache.clear()
        self.addCleanup(cache.clear)
        self.user = get_user_model().objects.create_user(email="owner@example.com", password="test")
        self.token = Token.objects.create(user=self.user, test_mode=True, label="test-key-123")
        self.client = APIClient()

    def _as_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def _as_basic(self):
        basic = base64.b64encode(f"{self.token.key}:".encode()).decode()
        self.client.credentials(HTTP_AUTHORIZATION=f"Basic {basic}")

    def _statuses_around(self, change, authenticate):
        authenticate()
        warm = self.client.get(SHIPMENTS).status_code
        change()
        after = self.client.get(SHIPMENTS).status_code
        return warm, after

    def _key(self, prefix="token_auth", token=None):
        return f"{prefix}:{hashlib.sha256((token or self.token).key.encode()).hexdigest()}"

    def _deactivate(self):
        self.user.is_active = False
        self.user.save()

    def _rename(self):
        self.user.full_name = f"{self.user.full_name}x"
        self.user.save()

    def test_a_deactivated_user_is_refused_at_once_with_a_token(self):
        warm, after = self._statuses_around(self._deactivate, self._as_token)

        self.assertEqual(warm, status.HTTP_200_OK)
        self.assertIn(after, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_a_deactivated_user_is_refused_at_once_with_basic_auth(self):
        warm, after = self._statuses_around(self._deactivate, self._as_basic)

        self.assertEqual(warm, status.HTTP_200_OK)
        self.assertIn(after, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_a_deleted_token_is_refused_at_once(self):
        warm, after = self._statuses_around(self.token.delete, self._as_token)

        self.assertEqual(warm, status.HTTP_200_OK)
        self.assertIn(after, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_a_deleted_user_is_refused_at_once(self):
        warm, after = self._statuses_around(self.user.delete, self._as_token)

        self.assertEqual(warm, status.HTTP_200_OK)
        self.assertIn(after, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_an_active_user_keeps_the_cached_authentication(self):
        # The cache still does its job: a login-timestamp-only save evicts nothing.
        self._as_token()
        self.client.get(SHIPMENTS)
        self.user.save(update_fields=["last_login"])

        self.assertIsInstance(cache.get(self._key()), tuple)

    def test_a_token_moved_to_an_inactive_user_stops_authenticating_as_the_old_owner(self):
        inactive = get_user_model().objects.create_user(email="inactive@example.com", password="test")
        inactive.is_active = False
        inactive.save()

        def move():
            self.token.user = inactive
            self.token.save()

        warm, after = self._statuses_around(move, self._as_token)

        self.assertEqual(warm, status.HTTP_200_OK)
        self.assertIn(after, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_a_token_switched_to_test_mode_is_no_longer_served_from_the_cache(self):
        self._as_token()
        self.client.get(SHIPMENTS)
        self.token.test_mode = False
        self.token.save()

        self.assertEqual(cache.get(self._key()), TOKEN_REVOKED)

    def test_a_refill_before_commit_is_evicted_when_the_change_commits(self):
        # Even an unconditional overwrite before the commit is replaced at commit.
        key = self._key()
        with self.captureOnCommitCallbacks(execute=True):
            self.user.is_active = False
            self.user.save()
            cache.set(key, "stale-entry-from-another-worker", 300)

        self.assertEqual(cache.get(key), TOKEN_REVOKED)

    def test_a_request_that_read_the_old_row_cannot_write_it_back_after_commit(self):
        # A request read the token and its still-staff user before the demotion
        # committed, and only fills the cache afterwards. The fill must not land.
        self.user.is_staff = True
        self.user.save()
        cache.clear()  # the promotion's revocation marker has expired
        stale_pair = (self.user, self.token)
        request = APIRequestFactory().get(SHIPMENTS, HTTP_AUTHORIZATION=f"Token {self.token.key}")

        with self.captureOnCommitCallbacks(execute=True):
            self.user.is_staff = False
            self.user.save()

        with mock.patch.object(BaseTokenAuthentication, "authenticate", return_value=stale_pair):
            TokenAuthentication()._authenticate_with_cache(request)

        self.assertEqual(cache.get(self._key()), TOKEN_REVOKED)
        user, _ = TokenAuthentication()._authenticate_with_cache(request)
        self.assertFalse(user.is_staff)

    def test_basic_auth_does_not_overwrite_the_revocation_marker(self):
        self.user.full_name = "Renamed"
        self.user.save()

        user, _ = TokenBasicAuthentication().authenticate_credentials(self.token.key)

        self.assertEqual(user.full_name, "Renamed")
        self.assertEqual(cache.get(self._key("token_basic_auth")), TOKEN_REVOKED)

    def test_the_revocation_marker_is_a_cache_miss_for_an_active_user(self):
        # A change that keeps the user active must not lock them out.
        for authenticate in (self._as_token, self._as_basic):
            with self.subTest(authenticate.__name__):
                warm, after = self._statuses_around(self._rename, authenticate)

                self.assertEqual((warm, after), (status.HTTP_200_OK, status.HTTP_200_OK))

    def test_a_new_token_leaves_no_marker(self):
        token = Token.objects.create(user=self.user, test_mode=False, label="test-key-456")

        self.assertEqual(
            [cache.get(self._key(prefix, token)) for prefix in ("token_auth", "token_basic_auth")],
            [None, None],
        )

    def test_a_demoted_staff_user_does_not_keep_the_cached_flags(self):
        # The cached pair carries is_staff; a demotion must not be served from the cache.
        self.user.is_staff = True
        self.user.save()
        cache.clear()  # the promotion's revocation marker has expired
        self._as_token()
        self.client.get(SHIPMENTS)
        key = self._key()
        self.assertTrue(cache.get(key)[0].is_staff)

        self.user.is_staff = False
        self.user.save()

        self.assertEqual(cache.get(key), TOKEN_REVOKED)


@contextlib.contextmanager
def in_schema(name):
    """Run as a deployment whose connection switches database schema per tenant.
    Nests: leaving restores the schema that was active before."""
    missing = object()
    previous = getattr(connection, "schema_name", missing)
    connection.schema_name = name
    try:
        yield
    finally:
        if previous is missing:
            del connection.schema_name
        else:
            connection.schema_name = previous


@override_settings(TOKEN_AUTH_CACHE_TTL=300)
class TestTokenAuthCachePerSchema(APITestCase):
    """Precaution for deployments that switch schemas per tenant: an entry cached
    under one schema is never read, nor evicted, under another."""

    def setUp(self):
        cache.clear()
        self.addCleanup(cache.clear)
        self.user = get_user_model().objects.create_user(email="owner@example.com", password="test")
        self.other = get_user_model().objects.create_user(email="other@example.com", password="test")
        self.token = Token.objects.create(user=self.user, test_mode=True, label="test-key-123")
        self.request = APIRequestFactory().get(SHIPMENTS, HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def _authenticated_user(self):
        user, _ = TokenAuthentication()._authenticate_with_cache(self.request)
        return user

    def test_an_entry_cached_under_one_schema_is_not_read_under_another(self):
        with in_schema("tenant_a"):
            cache.set(token_cache_key("token_auth", self.token.key), (self.other, self.token), 300)
            served_a = self._authenticated_user()
        with in_schema("tenant_b"):
            served_b = self._authenticated_user()

        self.assertEqual((served_a, served_b), (self.other, self.user))

    def test_eviction_under_one_schema_leaves_the_other_untouched(self):
        keys = {}
        for schema in ("tenant_a", "tenant_b"):
            with in_schema(schema):
                self._authenticated_user()
                keys[schema] = token_cache_key("token_auth", self.token.key)

        with in_schema("tenant_a"):
            self.user.full_name = "Renamed"
            self.user.save()

        self.assertEqual(cache.get(keys["tenant_a"]), TOKEN_REVOKED)
        self.assertIsInstance(cache.get(keys["tenant_b"]), tuple)

    def test_the_eviction_at_commit_uses_the_schema_of_the_change(self):
        # The change is made in tenant_a, then the connection switches to tenant_b
        # before the commit. A refill of tenant_a's entry before the commit must still
        # be replaced at commit, and tenant_b's entry left alone.
        keys = {}
        for schema in ("tenant_a", "tenant_b"):
            with in_schema(schema):
                self._authenticated_user()
                keys[schema] = token_cache_key("token_auth", self.token.key)
        cached_b = cache.get(keys["tenant_b"])

        with in_schema("tenant_b"):
            with self.captureOnCommitCallbacks(execute=True):
                with in_schema("tenant_a"):
                    self.user.is_staff = True
                    self.user.save()
                    cache.set(keys["tenant_a"], (self.user, self.token), 300)

        self.assertEqual(cache.get(keys["tenant_a"]), TOKEN_REVOKED)
        self.assertEqual(cache.get(keys["tenant_b"]), cached_b)

    def test_without_a_schema_the_key_is_unchanged(self):
        digest = hashlib.sha256(self.token.key.encode()).hexdigest()

        self.assertEqual(token_cache_key("token_auth", self.token.key), f"token_auth:{digest}")


@override_settings(TOKEN_AUTH_CACHE_TTL=0)
class TestTokenAuthWithoutCache(APITestCase):
    """TOKEN_AUTH_CACHE_TTL=0 (the default without a shared cache): nothing is cached,
    so a revocation takes effect on the very next request, whatever changed the row."""

    def setUp(self):
        cache.clear()
        self.addCleanup(cache.clear)
        self.user = get_user_model().objects.create_user(email="owner@example.com", password="test")
        self.token = Token.objects.create(user=self.user, test_mode=True, label="test-key-123")
        self.client = APIClient()

    def _keys(self):
        digest = hashlib.sha256(self.token.key.encode()).hexdigest()
        return [f"token_auth:{digest}", f"token_basic_auth:{digest}"]

    def test_no_entry_is_written_for_either_scheme(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        token_status = self.client.get(SHIPMENTS).status_code
        basic = base64.b64encode(f"{self.token.key}:".encode()).decode()
        self.client.credentials(HTTP_AUTHORIZATION=f"Basic {basic}")
        basic_status = self.client.get(SHIPMENTS).status_code

        self.assertEqual((token_status, basic_status), (status.HTTP_200_OK, status.HTTP_200_OK))
        self.assertEqual([cache.get(key) for key in self._keys()], [None, None])

    def test_a_user_change_writes_no_revocation_marker(self):
        self.user.is_staff = True
        self.user.save()
        self.token.test_mode = False
        self.token.save()

        self.assertEqual([cache.get(key) for key in self._keys()], [None, None])

    def test_a_bulk_deactivation_is_refused_on_the_next_request(self):
        # QuerySet.update sends no signal; without a cache that does not matter.
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        warm = self.client.get(SHIPMENTS).status_code
        get_user_model().objects.filter(pk=self.user.pk).update(is_active=False)
        after = self.client.get(SHIPMENTS).status_code

        self.assertEqual(warm, status.HTTP_200_OK)
        self.assertIn(after, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))
