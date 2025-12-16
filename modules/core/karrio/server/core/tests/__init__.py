# Backward-compatible exports for karrio.server.core.tests
# This allows existing imports like:
#   from karrio.server.core.tests import APITestCase
# to continue working

import logging

logging.disable(logging.CRITICAL)

# Import test classes explicitly to enable Django's test discovery
from karrio.server.core.tests.test_exception_level import (
    TestGetDefaultLevel,
    TestAPIException,
    TestIndexedAPIException,
    TestErrorLevelDefaults,
    TestErrorDatatype,
)
from karrio.server.core.tests.test_resource_token import (
    TestResourceAccessTokenUnit,
    TestResourceTokenAPI,
    TestDocumentDownloadWithAPIToken,
)

# Import our custom APITestCase (must be last to avoid being overridden)
from karrio.server.core.tests.base import APITestCase

__all__ = ["APITestCase"]
