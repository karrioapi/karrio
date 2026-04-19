# Backward-compatible exports for karrio.server.core.tests
# This allows existing imports like:
#   from karrio.server.core.tests import APITestCase
# to continue working

import logging

logging.disable(logging.CRITICAL)

# Import test classes explicitly to enable Django's test discovery
# Import our custom APITestCase (must be last to avoid being overridden)
from karrio.server.core.tests.base import APITestCase
from karrio.server.core.tests.test_exception_level import (
    TestAPIException,
    TestErrorDatatype,
    TestErrorLevelDefaults,
    TestGetDefaultLevel,
    TestIndexedAPIException,
)
from karrio.server.core.tests.test_request_id import (
    TestRequestIDInAPI,
    TestRequestIDMiddleware,
    TestRequestIDValidation,
)
from karrio.server.core.tests.test_resource_token import (
    TestDocumentDownloadWithAPIToken,
    TestResourceAccessTokenUnit,
    TestResourceTokenAPI,
)

__all__ = [
    "APITestCase",
    "TestGetDefaultLevel",
    "TestAPIException",
    "TestIndexedAPIException",
    "TestErrorLevelDefaults",
    "TestErrorDatatype",
    "TestResourceAccessTokenUnit",
    "TestResourceTokenAPI",
    "TestDocumentDownloadWithAPIToken",
    "TestRequestIDValidation",
    "TestRequestIDMiddleware",
    "TestRequestIDInAPI",
]
