from django.core.management import BaseCommand
from karrio.server.graph.schema import schema
from strawberry.printer import print_schema


class Command(BaseCommand):
    help = "Exports the strawberry graphql schema"

    def handle(self, *args, **options):
        self.stdout.write(print_schema(schema))
