from tenant_schemas.management.commands.migrate_schemas import Command as MigrateSchemasCommand


class Command(MigrateSchemasCommand):
    requires_system_checks = []
