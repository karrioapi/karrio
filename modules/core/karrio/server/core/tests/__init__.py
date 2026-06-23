# Backward-compatible exports for karrio.server.core.tests
# This allows existing imports like:
#   from karrio.server.core.tests import APITestCase
# to continue working

import logging

logging.disable(logging.CRITICAL)

# Import test classes explicitly to enable Django's test discovery
# Import our custom APITestCase (must be last to avoid being overridden)
from karrio.server.core.tests.base import APITestCase
from karrio.server.core.tests.test_apply_rate_selection import (
    TestApplyRateSelectionVariantDisambiguation,
)
from karrio.server.core.tests.test_authentication_middleware import (
    TestAuthenticationMiddlewareLazyOrgFailure,
    TestSessionContextTelemetryLazyOrgFailure,
)
from karrio.server.core.tests.test_carrier_plugin_visibility import (
    TestCarrierPluginVisibility,
)
from karrio.server.core.tests.test_exception_level import (
    TestAPIException,
    TestErrorDatatype,
    TestErrorLevelDefaults,
    TestGetDefaultLevel,
    TestIndexedAPIException,
)
from karrio.server.core.tests.test_health_status import TestHealthStatus
from karrio.server.core.tests.test_password_hashers import TestPasswordHasherLogin
from karrio.server.core.tests.test_public_ids import (
    TestEncryptId,
    TestEncryptIdRotation,
    TestEncryptToken,
    TestRedactRateMeta,
    TestResolveRateRef,
)
from karrio.server.core.tests.test_rate_dispatcher import TestDispatchRatesPartition
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
from karrio.server.core.tests.test_telemetry_scrubbing import (
    TestFallbackAndCaps,
    TestNoLeakGuard,
    TestOperationalPreserved,
    TestRegressionAndEdges,
    TestScrubSpanData,
    TestStructuralNames,
    TestUrl,
    TestValueShapedPII,
)
from karrio.server.core.tests.test_telemetry_scrubbing_hook import (
    TestSentryBeforeSendTransaction,
    TestWawiDiagnosticLogging,
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
    "TestApplyRateSelectionVariantDisambiguation",
    "TestAuthenticationMiddlewareLazyOrgFailure",
    "TestSessionContextTelemetryLazyOrgFailure",
    "TestHealthStatus",
    "TestPasswordHasherLogin",
    "TestDispatchRatesPartition",
    "TestEncryptId",
    "TestEncryptIdRotation",
    "TestEncryptToken",
    "TestRedactRateMeta",
    "TestResolveRateRef",
    "TestValueShapedPII",
    "TestStructuralNames",
    "TestNoLeakGuard",
    "TestOperationalPreserved",
    "TestUrl",
    "TestFallbackAndCaps",
    "TestRegressionAndEdges",
    "TestScrubSpanData",
    "TestSentryBeforeSendTransaction",
    "TestWawiDiagnosticLogging",
    "TestCarrierPluginVisibility",
]
