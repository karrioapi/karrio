# Generated by Django 3.2.12 on 2022-05-04 13:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pricing', '0023_auto_20220504_1335'),
        ('manager', '0033_auto_20220504_1335'),
        ('orgs', '0005_auto_20211231_2353'),
        ('providers', '0030_amazonmwssettings'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AmazonMwsSettings',
        ),
    ]