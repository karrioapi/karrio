from django.core.management import BaseCommand
from strawberry.printer import print_schema

from karrio.server.graph.schema import schema

class Command(BaseCommand):
    help = 'Exports the strawberry graphql schema'
    def handle(self, *args, **options):
        print(print_schema(schema))
