from django.core.management.base import BaseCommand
from karrio.server.providers.models import RateSheet


class Command(BaseCommand):
    help = 'Migrate existing rate sheets from legacy format to optimized zone reuse structure'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be migrated without making changes',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force migration even if rate sheet already has optimized structure',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        force = options['force']
        
        rate_sheets = RateSheet.objects.all()
        
        if not rate_sheets.exists():
            self.stdout.write(self.style.WARNING('No rate sheets found.'))
            return
        
        migrated_count = 0
        skipped_count = 0
        error_count = 0
        
        for rate_sheet in rate_sheets:
            try:
                # Check if already migrated
                if not force and (rate_sheet.zones or rate_sheet.service_rates):
                    self.stdout.write(
                        self.style.WARNING(f'Skipping {rate_sheet.name} - already has optimized structure')
                    )
                    skipped_count += 1
                    continue
                
                # Check if has services with zones to migrate
                has_zones = any(
                    service.zones for service in rate_sheet.services.all()
                )
                
                if not has_zones:
                    self.stdout.write(
                        self.style.WARNING(f'Skipping {rate_sheet.name} - no zones to migrate')
                    )
                    skipped_count += 1
                    continue
                
                if dry_run:
                    self.stdout.write(
                        self.style.SUCCESS(f'Would migrate: {rate_sheet.name}')
                    )
                    migrated_count += 1
                else:
                    # Perform migration
                    old_zones_count = sum(
                        len(service.zones or []) for service in rate_sheet.services.all()
                    )
                    
                    rate_sheet.migrate_from_legacy_format()
                    
                    new_zones_count = len(rate_sheet.zones or [])
                    new_rates_count = len(rate_sheet.service_rates or [])
                    
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Migrated {rate_sheet.name}: '
                            f'{old_zones_count} duplicated zones → '
                            f'{new_zones_count} shared zones + {new_rates_count} rates'
                        )
                    )
                    migrated_count += 1
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error migrating {rate_sheet.name}: {str(e)}')
                )
                error_count += 1
        
        # Summary
        if dry_run:
            self.stdout.write(
                self.style.SUCCESS(
                    f'\nDry run complete: {migrated_count} rate sheets would be migrated, '
                    f'{skipped_count} skipped, {error_count} errors'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'\nMigration complete: {migrated_count} rate sheets migrated, '
                    f'{skipped_count} skipped, {error_count} errors'
                )
            )