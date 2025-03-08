from django.core.management.base import BaseCommand
from oauth2_provider.models import Application
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates an OAuth2 client application'

    def add_arguments(self, parser):
        parser.add_argument('--name', required=True)
        parser.add_argument('--client_id', required=True)
        parser.add_argument('--client_secret', required=True)
        parser.add_argument('--redirect_uri', required=True)
        parser.add_argument('--user_email', required=True)

    def handle(self, *args, **options):
        try:
            user = User.objects.get(email=options['user_email'])
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"User with email {options['user_email']} does not exist"))
            return

        # Check if application with this client_id already exists
        app, created = Application.objects.update_or_create(
            client_id=options['client_id'],
            defaults={
                'name': options['name'],
                'user': user,
                'client_type': Application.CLIENT_CONFIDENTIAL,
                'authorization_grant_type': Application.GRANT_AUTHORIZATION_CODE,
                'client_secret': options['client_secret'],
                'redirect_uris': options['redirect_uri'],
                'skip_authorization': True,
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f"Successfully created OAuth2 application: {options['name']}"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Successfully updated OAuth2 application: {options['name']}"))
