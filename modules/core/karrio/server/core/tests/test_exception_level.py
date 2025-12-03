"""Tests for exception handler level classification.

These tests verify the level classification logic in isolation,
without requiring the full Django setup.
"""

import unittest
from unittest.mock import MagicMock
from rest_framework import status


class TestGetDefaultLevel(unittest.TestCase):
    """Tests for get_default_level function."""

    def setUp(self):
        # Import here to avoid Django setup issues
        from karrio.server.core.exceptions import get_default_level, ERROR_LEVEL_DEFAULTS
        self.get_default_level = get_default_level
        self.ERROR_LEVEL_DEFAULTS = ERROR_LEVEL_DEFAULTS

    def test_returns_exception_level_when_set(self):
        exc = MagicMock()
        exc.level = "warning"
        result = self.get_default_level(400, exc)
        self.assertEqual(result, "warning")

    def test_returns_status_code_mapping_for_400(self):
        result = self.get_default_level(400)
        self.assertEqual(result, "error")

    def test_returns_status_code_mapping_for_404(self):
        result = self.get_default_level(404)
        self.assertEqual(result, "warning")

    def test_returns_status_code_mapping_for_429(self):
        result = self.get_default_level(429)
        self.assertEqual(result, "warning")

    def test_returns_status_code_mapping_for_500(self):
        result = self.get_default_level(500)
        self.assertEqual(result, "error")

    def test_returns_status_code_mapping_for_503(self):
        result = self.get_default_level(503)
        self.assertEqual(result, "warning")

    def test_returns_error_for_unmapped_4xx(self):
        result = self.get_default_level(418)  # I'm a teapot
        self.assertEqual(result, "error")

    def test_returns_error_for_unmapped_5xx(self):
        result = self.get_default_level(599)
        self.assertEqual(result, "error")

    def test_returns_info_for_2xx(self):
        result = self.get_default_level(200)
        self.assertEqual(result, "info")

    def test_exception_level_overrides_status_code_default(self):
        exc = MagicMock()
        exc.level = "info"
        result = self.get_default_level(500, exc)  # 500 defaults to "error"
        self.assertEqual(result, "info")

    def test_ignores_none_level_on_exception(self):
        exc = MagicMock()
        exc.level = None
        result = self.get_default_level(404)
        self.assertEqual(result, "warning")


class TestAPIException(unittest.TestCase):
    """Tests for APIException class with level support."""

    def setUp(self):
        from karrio.server.core.exceptions import APIException, IndexedAPIException
        self.APIException = APIException
        self.IndexedAPIException = IndexedAPIException

    def test_default_level_is_none(self):
        exc = self.APIException(detail="Test error")
        self.assertIsNone(exc.level)

    def test_level_can_be_set_in_constructor(self):
        exc = self.APIException(detail="Test error", level="warning")
        self.assertEqual(exc.level, "warning")

    def test_status_code_default(self):
        exc = self.APIException(detail="Test error")
        self.assertEqual(exc.status_code, status.HTTP_400_BAD_REQUEST)

    def test_custom_status_code(self):
        exc = self.APIException(detail="Test error", status_code=500)
        self.assertEqual(exc.status_code, 500)


class TestIndexedAPIException(unittest.TestCase):
    """Tests for IndexedAPIException class."""

    def setUp(self):
        from karrio.server.core.exceptions import IndexedAPIException
        self.IndexedAPIException = IndexedAPIException

    def test_index_is_set(self):
        exc = self.IndexedAPIException(index=5, detail="Test error")
        self.assertEqual(exc.index, 5)

    def test_level_can_be_set(self):
        exc = self.IndexedAPIException(index=0, detail="Test error", level="warning")
        self.assertEqual(exc.level, "warning")


class TestErrorLevelDefaults(unittest.TestCase):
    """Tests for ERROR_LEVEL_DEFAULTS mapping."""

    def setUp(self):
        from karrio.server.core.exceptions import ERROR_LEVEL_DEFAULTS
        self.ERROR_LEVEL_DEFAULTS = ERROR_LEVEL_DEFAULTS

    def test_client_errors_mapped(self):
        self.assertIn(400, self.ERROR_LEVEL_DEFAULTS)
        self.assertIn(401, self.ERROR_LEVEL_DEFAULTS)
        self.assertIn(403, self.ERROR_LEVEL_DEFAULTS)
        self.assertIn(404, self.ERROR_LEVEL_DEFAULTS)
        self.assertIn(422, self.ERROR_LEVEL_DEFAULTS)

    def test_server_errors_mapped(self):
        self.assertIn(500, self.ERROR_LEVEL_DEFAULTS)
        self.assertIn(502, self.ERROR_LEVEL_DEFAULTS)
        self.assertIn(503, self.ERROR_LEVEL_DEFAULTS)
        self.assertIn(504, self.ERROR_LEVEL_DEFAULTS)

    def test_404_is_warning(self):
        self.assertEqual(self.ERROR_LEVEL_DEFAULTS[404], "warning")

    def test_429_is_warning(self):
        self.assertEqual(self.ERROR_LEVEL_DEFAULTS[429], "warning")

    def test_503_is_warning(self):
        self.assertEqual(self.ERROR_LEVEL_DEFAULTS[503], "warning")

    def test_500_is_error(self):
        self.assertEqual(self.ERROR_LEVEL_DEFAULTS[500], "error")


class TestErrorDatatype(unittest.TestCase):
    """Tests for Error datatype with level field."""

    def setUp(self):
        from karrio.server.core.datatypes import Error
        self.Error = Error

    def test_error_has_level_field(self):
        error = self.Error(code="test", message="Test error", level="warning")
        self.assertEqual(error.level, "warning")

    def test_error_level_defaults_to_none(self):
        error = self.Error(code="test", message="Test error")
        self.assertIsNone(error.level)
