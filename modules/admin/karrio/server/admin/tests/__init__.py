# ruff: noqa: I001
# Re-export all test classes for backward-compatible discovery.
# `karrio test karrio.server.admin.tests` still works without changes.

from karrio.server.admin.tests.base import AdminGraphTestCase  # noqa: F401
from karrio.server.admin.tests.test_rate_sheets import (  # noqa: F401
    TestAdminRateSheets,
    TestAdminRateSheetCrossAdminAccess,
    TestAdminRateSheetZones,
    TestAdminRateSheetSurcharges,
    TestAdminServiceRates,
    TestAdminServiceAssignments,
    TestAdminRateSheetService,
    TestAdminDeleteServiceRate,
    TestAdminWeightRanges,
    TestAdminRateSheetQueryVerification,
    TestAdminRateSheetEdgeCases,
)
from karrio.server.admin.tests.test_connections import (  # noqa: F401
    TestAdminCarrierConnections,
    TestAdminBrokeredConnections,
)
from karrio.server.admin.tests.test_markups import (  # noqa: F401
    TestAdminMarkups,
    TestMarkupFeatureGating,
)
from karrio.server.admin.tests.test_auth import (  # noqa: F401
    TestAdminUnauthenticated,
    TestAdminNonStaffUser,
    TestAdminRateSheetValidation,
    TestAdminConnectionValidation,
    TestAdminMarkupValidation,
    TestAdminDataIsolation,
)
