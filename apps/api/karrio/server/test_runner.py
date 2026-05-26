from django.conf import settings
from django.test.runner import DiscoverRunner


class KarrioTestRunner(DiscoverRunner):
    """Custom Django test runner that overrides settings for the test suite."""

    def setup_test_environment(self, **kwargs):
        super().setup_test_environment(**kwargs)
        # Speed up tests with a fast hasher (PBKDF2 is intentionally slow).
        settings.PASSWORD_HASHERS = [
            "django.contrib.auth.hashers.MD5PasswordHasher",
        ]
