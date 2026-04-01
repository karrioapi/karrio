"""
Management command to check KEK version usage.

Usage:
    karrio check_kek_usage
    karrio check_kek_usage --version 1
"""
from django.core.management.base import BaseCommand
from karrio.server.providers.secret_manager import (
    get_secret_manager,
    check_kek_in_use,
    get_kek_usage_stats,
)


class Command(BaseCommand):
    help = 'Check which KEK versions are in use by secrets'

    def add_arguments(self, parser):
        parser.add_argument(
            '--version',
            type=int,
            default=None,
            help='Check specific KEK version (if not provided, shows all)',
        )

    def handle(self, *args, **options):
        version = options['version']

        try:
            secret_manager = get_secret_manager()
            if secret_manager is None:
                self.stdout.write(
                    self.style.WARNING(
                        'Secret encryption is not enabled. '
                        'Set ACTIVE_KEK_VERSIONS to enable encryption.'
                    )
                )
                return

            stats = get_kek_usage_stats()

            if version is not None:
                # Check specific version
                in_use = check_kek_in_use(version)
                count = stats.get(version, 0)

                if version not in secret_manager.kek_registry:
                    self.stdout.write(
                        self.style.ERROR(
                            f'KEK version {version} not found in registry'
                        )
                    )
                elif in_use:
                    self.stdout.write(
                        self.style.WARNING(
                            f'KEK version {version} is IN USE by {count} secret(s)'
                        )
                    )
                    self.stdout.write(
                        '  [WARNING] Do NOT remove this KEK from registry until all secrets are rotated'
                    )
                else:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'KEK version {version} is NOT in use (safe to remove)'
                        )
                    )
            else:
                # Show all versions
                self.stdout.write(self.style.SUCCESS('KEK Usage Statistics:\n'))

                # Show configured KEKs
                configured_versions = sorted(secret_manager.kek_registry.keys())
                current_version = max(configured_versions)

                self.stdout.write('Configured KEK versions:')
                for v in configured_versions:
                    marker = ' (current)' if v == current_version else ''
                    count = stats.get(v, 0)
                    status = '[OK]' if count == 0 else '[!]'
                    style = self.style.SUCCESS if count == 0 else self.style.WARNING

                    self.stdout.write(
                        style(f'  {status} KEK_V{v}: {count} secret(s) using it{marker}')
                    )

                # Show versions in use but not configured (orphaned)
                orphaned = set(stats.keys()) - set(configured_versions)
                if orphaned:
                    self.stdout.write(
                        self.style.ERROR(
                            f'\n[WARNING] Found secrets using KEK versions not in registry: {sorted(orphaned)}'
                        )
                    )
                    self.stdout.write(
                        '   These secrets cannot be decrypted! Add these KEKs to your registry.'
                    )

                # Summary
                total_secrets = sum(stats.values())
                self.stdout.write(f'\nTotal secrets: {total_secrets}')

                # Safety check
                old_versions = [v for v in configured_versions if v < current_version]
                old_in_use = [v for v in old_versions if stats.get(v, 0) > 0]

                if old_in_use:
                    self.stdout.write(
                        self.style.WARNING(
                            f'\n[WARNING] Old KEK versions still in use: {old_in_use}'
                        )
                    )
                    self.stdout.write(
                        '   Consider running rotation to migrate these secrets to the current version.'
                    )
                elif old_versions:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'\nAll old KEK versions ({old_versions}) are safe to remove'
                        )
                    )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))

