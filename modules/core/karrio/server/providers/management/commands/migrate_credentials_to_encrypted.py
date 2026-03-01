"""
Management command for migrating plaintext credentials from JSONField to encrypted secrets.

This command finds all SystemConnection and CarrierConnection instances with plaintext
sensitive fields in their credentials JSONField, encrypts them, and optionally removes
them from the JSONField.

Usage:
    karrio migrate_credentials_to_encrypted
    karrio migrate_credentials_to_encrypted --dry-run
    karrio migrate_credentials_to_encrypted --remove-from-jsonfield
    karrio migrate_credentials_to_encrypted --connection-type system
    karrio migrate_credentials_to_encrypted --batch-size 50
"""
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from karrio.server.providers.models.connection import SystemConnection
from karrio.server.providers.models.carrier import CarrierConnection
from karrio.server.providers.credential_manager import get_credential_manager
from karrio.server.providers.secret_manager import get_secret_manager


class Command(BaseCommand):
    help = 'Migrate plaintext credentials from JSONField to encrypted secrets table'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be migrated without making changes',
        )
        parser.add_argument(
            '--remove-from-jsonfield',
            action='store_true',
            help='Remove encrypted fields from credentials JSONField after encryption',
        )
        parser.add_argument(
            '--connection-type',
            type=str,
            choices=['system', 'carrier', 'all'],
            default='all',
            help='Type of connections to migrate (default: all)',
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=100,
            help='Number of connections to process per batch (default: 100)',
        )
        parser.add_argument(
            '--connection-id',
            type=str,
            default=None,
            help='Migrate only a specific connection by ID',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        remove_from_jsonfield = options['remove_from_jsonfield']
        connection_type = options['connection_type']
        batch_size = options['batch_size']
        connection_id = options['connection_id']

        # Check if encryption is enabled
        try:
            secret_manager = get_secret_manager()
            if secret_manager is None:
                raise CommandError(
                    'Secret encryption is not enabled. '
                    'Set ACTIVE_KEK_VERSIONS to enable encryption before migrating.'
                )
        except Exception as e:
            raise CommandError(f'Failed to initialize secret manager: {e}') from e

        credential_manager = get_credential_manager()

        # Collect connections to migrate
        system_connections = []
        carrier_connections = []

        if connection_id:
            # Migrate specific connection
            if connection_type in ['system', 'all']:
                try:
                    conn = SystemConnection.objects.get(id=connection_id)
                    system_connections.append(conn)
                except SystemConnection.DoesNotExist:
                    pass

            if connection_type in ['carrier', 'all']:
                try:
                    conn = CarrierConnection.objects.get(id=connection_id)
                    carrier_connections.append(conn)
                except CarrierConnection.DoesNotExist:
                    pass

            if not system_connections and not carrier_connections:
                raise CommandError(f'Connection {connection_id} not found')
        else:
            # Migrate all connections
            if connection_type in ['system', 'all']:
                system_connections = list(SystemConnection.objects.all()[:10000])  # Safety limit

            if connection_type in ['carrier', 'all']:
                carrier_connections = list(CarrierConnection.objects.all()[:10000])  # Safety limit

        total_connections = len(system_connections) + len(carrier_connections)

        if total_connections == 0:
            self.stdout.write(self.style.WARNING('No connections found to migrate.'))
            return

        self.stdout.write(
            self.style.WARNING(
                f'Found {len(system_connections)} system connections and '
                f'{len(carrier_connections)} carrier connections to check.'
            )
        )

        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made\n'))

        # Statistics
        stats = {
            'system_migrated': 0,
            'system_skipped': 0,
            'system_errors': 0,
            'carrier_migrated': 0,
            'carrier_skipped': 0,
            'carrier_errors': 0,
            'total_fields_encrypted': 0,
        }

        # Process system connections
        for i, conn in enumerate(system_connections, 1):
            try:
                result = self._migrate_system_connection(
                    conn,
                    credential_manager,
                    dry_run,
                    remove_from_jsonfield,
                )
                if result['migrated']:
                    stats['system_migrated'] += 1
                    stats['total_fields_encrypted'] += result['fields_count']
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'[{i}/{len(system_connections)}] System {conn.carrier_id}: '
                            f'Encrypted {result["fields_count"]} field(s)'
                        )
                    )
                else:
                    stats['system_skipped'] += 1
                    if result['reason']:
                        self.stdout.write(
                            self.style.WARNING(
                                f'[{i}/{len(system_connections)}] System {conn.carrier_id}: '
                                f'Skipped - {result["reason"]}'
                            )
                        )
            except Exception as e:
                stats['system_errors'] += 1
                self.stdout.write(
                    self.style.ERROR(
                        f'[{i}/{len(system_connections)}] System {conn.carrier_id}: '
                        f'Error - {str(e)}'
                    )
                )

        # Process carrier connections
        for i, conn in enumerate(carrier_connections, 1):
            try:
                result = self._migrate_carrier_connection(
                    conn,
                    credential_manager,
                    dry_run,
                    remove_from_jsonfield,
                )
                if result['migrated']:
                    stats['carrier_migrated'] += 1
                    stats['total_fields_encrypted'] += result['fields_count']
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'[{i}/{len(carrier_connections)}] Carrier {conn.carrier_id}: '
                            f'Encrypted {result["fields_count"]} field(s)'
                        )
                    )
                else:
                    stats['carrier_skipped'] += 1
                    if result['reason']:
                        self.stdout.write(
                            self.style.WARNING(
                                f'[{i}/{len(carrier_connections)}] Carrier {conn.carrier_id}: '
                                f'Skipped - {result["reason"]}'
                            )
                        )
            except Exception as e:
                stats['carrier_errors'] += 1
                self.stdout.write(
                    self.style.ERROR(
                        f'[{i}/{len(carrier_connections)}] Carrier {conn.carrier_id}: '
                        f'Error - {str(e)}'
                    )
                )

        # Summary
        total_migrated = stats['system_migrated'] + stats['carrier_migrated']
        total_skipped = stats['system_skipped'] + stats['carrier_skipped']
        total_errors = stats['system_errors'] + stats['carrier_errors']

        self.stdout.write('\n' + '=' * 60)
        if dry_run:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Dry run complete:\n'
                    f'  System connections: {stats["system_migrated"]} would migrate, '
                    f'{stats["system_skipped"]} skipped, {stats["system_errors"]} errors\n'
                    f'  Carrier connections: {stats["carrier_migrated"]} would migrate, '
                    f'{stats["carrier_skipped"]} skipped, {stats["carrier_errors"]} errors\n'
                    f'  Total fields: {stats["total_fields_encrypted"]} would be encrypted'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Migration complete:\n'
                    f'  System connections: {stats["system_migrated"]} migrated, '
                    f'{stats["system_skipped"]} skipped, {stats["system_errors"]} errors\n'
                    f'  Carrier connections: {stats["carrier_migrated"]} migrated, '
                    f'{stats["carrier_skipped"]} skipped, {stats["carrier_errors"]} errors\n'
                    f'  Total fields encrypted: {stats["total_fields_encrypted"]}'
                )
            )
            if remove_from_jsonfield:
                self.stdout.write(
                    self.style.SUCCESS(
                        '  Encrypted fields have been removed from JSONField'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        '  Encrypted fields remain in JSONField (use --remove-from-jsonfield to remove)'
                    )
                )

    def _migrate_system_connection(
        self,
        conn: SystemConnection,
        credential_manager,
        dry_run: bool,
        remove_from_jsonfield: bool,
    ) -> dict:
        """Migrate a single SystemConnection."""
        # Get sensitive fields for this carrier
        sensitive_fields = conn.get_sensitive_fields()

        if not sensitive_fields:
            return {'migrated': False, 'reason': 'No sensitive fields defined for this carrier'}

        # Get current credentials from JSONField
        credentials = conn.credentials or {}

        # Find sensitive fields that are in plaintext
        plaintext_sensitive = {
            field: credentials[field]
            for field in sensitive_fields
            if field in credentials and credentials[field] and str(credentials[field]).strip()
        }

        if not plaintext_sensitive:
            return {'migrated': False, 'reason': 'No plaintext sensitive fields found'}

        # Check if already encrypted (exists in secrets table)
        from karrio.server.providers.models.secret import SystemSecretRef
        existing_encrypted = set(
            SystemSecretRef.objects.filter(
                system_connection_id=conn.id,
                name__in=plaintext_sensitive.keys()
            ).values_list('name', flat=True)
        )

        # Only migrate fields that aren't already encrypted
        fields_to_migrate = {
            k: v for k, v in plaintext_sensitive.items()
            if k not in existing_encrypted
        }

        if not fields_to_migrate:
            return {'migrated': False, 'reason': 'All sensitive fields already encrypted'}

        if dry_run:
            return {
                'migrated': True,
                'fields_count': len(fields_to_migrate),
                'fields': list(fields_to_migrate.keys())
            }

        # Perform migration
        with transaction.atomic():
            # Get existing credentials (includes already-encrypted fields via get_credentials)
            existing_credentials = conn.get_credentials()
            
            # Merge fields to migrate with existing credentials
            merged_credentials = {**existing_credentials, **fields_to_migrate}
            
            # Encrypt the fields (set_credentials will encrypt sensitive and store non-sensitive)
            conn.set_credentials(merged_credentials)

            # Optionally remove from JSONField
            if remove_from_jsonfield:
                updated_credentials = credentials.copy()
                for field in fields_to_migrate.keys():
                    updated_credentials.pop(field, None)
                SystemConnection.objects.filter(id=conn.id).update(
                    credentials=updated_credentials
                )

        return {
            'migrated': True,
            'fields_count': len(fields_to_migrate),
            'fields': list(fields_to_migrate.keys())
        }

    def _migrate_carrier_connection(
        self,
        conn: CarrierConnection,
        credential_manager,
        dry_run: bool,
        remove_from_jsonfield: bool,
    ) -> dict:
        """Migrate a single CarrierConnection."""
        # Get sensitive fields for this carrier
        sensitive_fields = conn.get_sensitive_fields()

        if not sensitive_fields:
            return {'migrated': False, 'reason': 'No sensitive fields defined for this carrier'}

        # Get current credentials from JSONField
        credentials = conn.credentials or {}

        # Find sensitive fields that are in plaintext
        plaintext_sensitive = {
            field: credentials[field]
            for field in sensitive_fields
            if field in credentials and credentials[field] and str(credentials[field]).strip()
        }

        if not plaintext_sensitive:
            return {'migrated': False, 'reason': 'No plaintext sensitive fields found'}

        # Check if already encrypted (exists in secrets table)
        from karrio.server.providers.models.secret import CarrierSecretRef
        existing_encrypted = set(
            CarrierSecretRef.objects.filter(
                carrier_id=conn.id,
                name__in=plaintext_sensitive.keys()
            ).values_list('name', flat=True)
        )

        # Only migrate fields that aren't already encrypted
        fields_to_migrate = {
            k: v for k, v in plaintext_sensitive.items()
            if k not in existing_encrypted
        }

        if not fields_to_migrate:
            return {'migrated': False, 'reason': 'All sensitive fields already encrypted'}

        if dry_run:
            return {
                'migrated': True,
                'fields_count': len(fields_to_migrate),
                'fields': list(fields_to_migrate.keys())
            }

        # Perform migration
        with transaction.atomic():
            # Get existing credentials (includes already-encrypted fields via get_credentials)
            existing_credentials = conn.get_credentials()
            
            # Merge fields to migrate with existing credentials
            merged_credentials = {**existing_credentials, **fields_to_migrate}
            
            # Encrypt the fields (set_credentials will encrypt sensitive and store non-sensitive)
            conn.set_credentials(merged_credentials)

            # Optionally remove from JSONField
            if remove_from_jsonfield:
                updated_credentials = credentials.copy()
                for field in fields_to_migrate.keys():
                    updated_credentials.pop(field, None)
                CarrierConnection.objects.filter(id=conn.id).update(
                    credentials=updated_credentials
                )

        return {
            'migrated': True,
            'fields_count': len(fields_to_migrate),
            'fields': list(fields_to_migrate.keys())
        }

