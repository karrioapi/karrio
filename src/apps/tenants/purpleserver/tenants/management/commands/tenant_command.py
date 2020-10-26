from tenant_schemas.management.commands.tenant_command import Command as BaseCommand


class Command(BaseCommand):
    requires_system_checks = []
