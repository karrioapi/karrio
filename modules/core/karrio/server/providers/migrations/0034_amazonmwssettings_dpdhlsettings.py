# Generated by Django 3.2.14 on 2022-08-08 08:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('providers', '0033_auto_20220708_1350'),
    ]

    operations = [
        migrations.CreateModel(
            name='AmazonMwsSettings',
            fields=[
                ('carrier_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='providers.carrier')),
                ('seller_id', models.CharField(max_length=50)),
                ('developer_id', models.CharField(max_length=50)),
                ('mws_auth_token', models.CharField(max_length=50)),
                ('aws_region', models.CharField(default='us-east-1', max_length=50)),
            ],
            options={
                'verbose_name': 'AmazonMws Settings',
                'verbose_name_plural': 'AmazonMws Settings',
                'db_table': 'amazon_mws-settings',
            },
            bases=('providers.carrier',),
        ),
        migrations.CreateModel(
            name='DPDHLSettings',
            fields=[
                ('carrier_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='providers.carrier')),
                ('app_id', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('signature', models.CharField(max_length=100)),
                ('account_number', models.CharField(blank=True, default='', max_length=100)),
            ],
            options={
                'verbose_name': 'Deutsche Post DHL Settings',
                'verbose_name_plural': 'Deutsche Post DHL Settings',
                'db_table': 'dpdhl-settings',
            },
            bases=('providers.carrier',),
        ),
    ]
