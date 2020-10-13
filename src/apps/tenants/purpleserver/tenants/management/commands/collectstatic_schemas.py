from tenant_schemas.management.commands.collectstatic_schemas import Command as BaseCommand
from tenant_schemas.management.commands import (
    connection,
    get_public_schema_name,
    get_tenant_model
)


class Command(BaseCommand):
    requires_system_checks = []
    COMMAND_NAME = 'collectstatic'

    def handle(self, *args, **options):
        """
        Iterates a command over all registered schemata.
        """
        arguments = ["schema_name", "skip_public"]
        if options["schema_name"]:
            # only run on a particular schema
            connection.set_schema_to_public()
            self.execute_command(
                get_tenant_model().objects.get(schema_name=options["schema_name"]),
                self.COMMAND_NAME,
                *args,
                **{k: v for k, v in options.items() if k not in arguments}
            )
        else:
            for tenant in get_tenant_model().objects.all():
                if not (
                    options["skip_public"]
                    and tenant.schema_name == get_public_schema_name()
                ):
                    self.execute_command(
                        tenant,
                        self.COMMAND_NAME,
                        *args,
                        **{k: v for k, v in options.items() if k not in arguments}
                    )
