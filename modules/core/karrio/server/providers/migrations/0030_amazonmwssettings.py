# Generated by Django 3.2.12 on 2022-04-13 09:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('providers', '0029_easypostsettings'),
    ]

    operations = [
        migrations.CreateModel(
            name='AmazonMwsSettings',
            fields=[
                ('carrier_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='providers.carrier')),
                ('access_key', models.CharField(max_length=200)),
                ('secret_key', models.CharField(max_length=200)),
                ('aws_region', models.CharField(default='us-east-1', max_length=200)),
            ],
            options={
                'verbose_name': 'AmazonMws Settings',
                'verbose_name_plural': 'AmazonMws Settings',
                'db_table': 'amazon_mws-settings',
            },
            bases=('providers.carrier',),
        ),
    ]
