"""
Management command for rotating secrets from one KEK version to another.

Usage:
    karrio rotate_secrets --old-version 1 --new-version 2
    karrio rotate_secrets --old-version 1 --new-version 2 --batch-size 50
"""
from django.core.management.base import BaseCommand, CommandError
from karrio.server.providers.rotation import rotate_all_secrets
from karrio.server.providers.secret_manager import get_secret_manager


class Command(BaseCommand):
    help = 'Rotate encrypted secrets from one KEK version to another'

    def add_arguments(self, parser):
        parser.add_argument(
            '--old-version',
            type=int,
            required=True,
            help='Current KEK version to rotate from',
        )
        parser.add_argument(
            '--new-version',
            type=int,
            required=True,
            help='Target KEK version to rotate to',
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=100,
            help='Number of secrets to process per batch (default: 100)',
        )
        parser.add_argument(
            '--max-iterations',
            type=int,
            default=None,
            help='Maximum number of batches to process (default: unlimited)',
        )

    def handle(self, *args, **options):
        old_version = options['old_version']
        new_version = options['new_version']
        batch_size = options['batch_size']
        max_iterations = options['max_iterations']

        self.stdout.write(
            self.style.WARNING(
                f'Starting rotation from KEK v{old_version} to v{new_version}...'
            )
        )

        try:
            secret_manager = get_secret_manager()
            if secret_manager is None:
                raise CommandError(
                    'Secret encryption is not enabled. '
                    'Set ACTIVE_KEK_VERSIONS to enable encryption before rotating.'
                )

            # Validate versions exist
            if old_version not in secret_manager.kek_registry:
                raise CommandError(
                    f'Old KEK version {old_version} not found in registry. '
                    f'Available versions: {list(secret_manager.kek_registry.keys())}'
                )
            if new_version not in secret_manager.kek_registry:
                raise CommandError(
                    f'New KEK version {new_version} not found in registry. '
                    f'Available versions: {list(secret_manager.kek_registry.keys())}'
                )

            # Run rotation
            result = rotate_all_secrets(
                secret_manager=secret_manager,
                old_version=old_version,
                new_version=new_version,
                batch_size=batch_size,
                max_iterations=max_iterations,
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f'\nRotation complete!\n'
                    f'  Total rotated: {result["total_rotated"]}\n'
                    f'  Batches processed: {result["batches_processed"]}'
                )
            )

        except Exception as e:
            raise CommandError(f'Rotation failed: {e}') from e

