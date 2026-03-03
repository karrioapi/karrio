"""
Add secret storage tables for encrypted credential storage.

This migration creates:
- secrets: System-wide encrypted secret storage
- carrier_secret_refs: Reference table linking CarrierConnection to encrypted secrets
- system_secret_refs: Reference table linking SystemConnection to encrypted secrets

When unapplying this migration, encrypted secrets are automatically decrypted
and restored to the credentials JSONField before tables are dropped, preventing data loss.
"""
import uuid
import logging
from django.db import migrations, models
import django.db.models.deletion
import karrio.server.core.models
import karrio.server.core.models.base

logger = logging.getLogger(__name__)


def restore_plaintext_credentials(apps, schema_editor):
    """
    Restore plaintext credentials to JSONField before dropping secret tables.
    
    When unapplying this migration, decrypt all secrets and put them back
    into the credentials JSONField on the connections.
    """
    from karrio.server.providers.secret_manager import get_secret_manager
    
    Secret = apps.get_model('providers', 'Secret')
    SystemSecretRef = apps.get_model('providers', 'SystemSecretRef')
    CarrierSecretRef = apps.get_model('providers', 'CarrierSecretRef')
    SystemConnection = apps.get_model('providers', 'SystemConnection')
    CarrierConnection = apps.get_model('providers', 'CarrierConnection')
    
    secret_manager = get_secret_manager()
    restored_count = 0
    
    # Restore system connection credentials
    for ref in SystemSecretRef.objects.select_related('secret', 'system_connection').all():
        try:
            # Decrypt the secret
            plaintext = secret_manager.read_secret(ref.secret_id)
            credential_value = plaintext.decode('utf-8')
            
            # Get current credentials and update with decrypted value
            conn = ref.system_connection
            credentials = conn.credentials or {}
            credentials[ref.name] = credential_value
            
            # Update the connection
            SystemConnection.objects.filter(id=conn.id).update(credentials=credentials)
            restored_count += 1
        except Exception as e:
            logger.warning(f"Failed to restore credential '{ref.name}' for system connection {ref.system_connection_id}: {e}")
    
    # Restore carrier connection credentials
    for ref in CarrierSecretRef.objects.select_related('secret', 'carrier').all():
        try:
            # Decrypt the secret
            plaintext = secret_manager.read_secret(ref.secret_id)
            credential_value = plaintext.decode('utf-8')
            
            # Get current credentials and update with decrypted value
            conn = ref.carrier
            credentials = conn.credentials or {}
            credentials[ref.name] = credential_value
            
            # Update the connection
            CarrierConnection.objects.filter(id=conn.id).update(credentials=credentials)
            restored_count += 1
        except Exception as e:
            logger.warning(f"Failed to restore credential '{ref.name}' for carrier connection {ref.carrier_id}: {e}")
    
    logger.info(f"Restored {restored_count} encrypted credentials to plaintext in JSONField")


class Migration(migrations.Migration):

    dependencies = [
        ('providers', '0101_add_pickup_capability_to_dhl_parcel_de'),
    ]

    operations = [
        migrations.CreateModel(
            name='Secret',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, help_text='Unique identifier for the secret')),
                ('name', models.TextField(db_index=True, help_text="Unique logical identifier for the secret (e.g., 'carrier:uuid:api_key')", unique=True)),
                ('ciphertext', models.BinaryField(help_text='Encrypted secret value (nonce || encrypted_data || auth_tag)')),
                ('dek_wrapped', models.BinaryField(help_text='Encrypted DEK (nonce || encrypted_dek || auth_tag)')),
                ('key_version', models.IntegerField(db_index=True, help_text='KEK version used for encryption')),
                ('rotated_at', models.DateTimeField(blank=True, help_text='Timestamp when secret was last rotated (key version changed)', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Secret',
                'verbose_name_plural': 'Secrets',
                'db_table': 'secrets',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='CarrierSecretRef',
            fields=[
                ('id', models.CharField(default=karrio.server.core.models.base.uuid, editable=False, max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text="Credential field name (e.g., 'api_key', 'secret_key')", max_length=255)),
                ('carrier', models.ForeignKey(help_text='Carrier connection owning this credential', on_delete=django.db.models.deletion.CASCADE, related_name='secret_refs', to='providers.carrierconnection')),
                ('secret', models.ForeignKey(help_text='Encrypted secret value', on_delete=django.db.models.deletion.CASCADE, related_name='carrier_refs', to='providers.secret')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Carrier Secret Reference',
                'verbose_name_plural': 'Carrier Secret References',
                'db_table': 'carrier_secret_refs',
            },
        ),
        migrations.AddIndex(
            model_name='secret',
            index=models.Index(fields=['name'], name='secrets_name_idx'),
        ),
        migrations.AddIndex(
            model_name='secret',
            index=models.Index(fields=['key_version'], name='secrets_key_version_idx'),
        ),
        migrations.AddIndex(
            model_name='carriersecretref',
            index=models.Index(fields=['carrier', 'name'], name='carrier_secret_refs_carrier_name_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='carriersecretref',
            unique_together={('carrier', 'name')},
        ),
        migrations.CreateModel(
            name='SystemSecretRef',
            fields=[
                ('id', models.CharField(default=karrio.server.core.models.base.uuid, editable=False, max_length=50, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text="Credential field name (e.g., 'api_key', 'secret_key', 'password')", max_length=255)),
                ('system_connection', models.ForeignKey(help_text='System connection owning this credential', on_delete=django.db.models.deletion.CASCADE, related_name='secret_refs', to='providers.systemconnection')),
                ('secret', models.ForeignKey(help_text='Encrypted secret value', on_delete=django.db.models.deletion.CASCADE, related_name='system_refs', to='providers.secret')),
            ],
            options={
                'verbose_name': 'System Secret Reference',
                'verbose_name_plural': 'System Secret References',
                'db_table': 'system_secret_refs',
            },
        ),
        migrations.AddIndex(
            model_name='systemsecretref',
            index=models.Index(fields=['system_connection', 'name'], name='system_secr_system__e79c7e_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='systemsecretref',
            unique_together={('system_connection', 'name')},
        ),
        # Data migration to restore plaintext credentials when unapplying
        # Forward: No-op (tables are being created, no data to restore)
        # Reverse: Decrypt secrets and restore plaintext to credentials JSONField before dropping tables
        migrations.RunPython(
            code=migrations.RunPython.noop,  # No-op when applying (tables are being created)
            reverse_code=restore_plaintext_credentials,  # Restore plaintext before dropping tables
        ),
    ]
