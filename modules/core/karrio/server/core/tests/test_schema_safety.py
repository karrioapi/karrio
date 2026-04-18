from django.test import SimpleTestCase
from django.core.management import call_command


class TestRollingDeploySafetyCheck(SimpleTestCase):
    """End-to-end test that the `database` system checks pass cleanly.

    This is the guard that would have caught the ``is_archived`` regression
    shipped in 2026.1.27: a NOT NULL field added via AddField with only a
    Python-level default trips the NOT NULL constraint for any writer that
    omits the column (e.g., stale pods during a rolling deploy).
    """

    def test_database_system_checks_pass(self):
        # ``--fail-level ERROR`` raises SystemCheckError if any E-level issue
        # is raised. Warnings (stale baseline entries) are allowed through so
        # they don't gate CI, but are surfaced to developers locally.
        call_command("check", "--tag", "database", "--fail-level", "ERROR")
