# Generated by Django 3.2.10 on 2022-01-19 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('providers', '0021_auto_20211231_2353'),
    ]

    operations = [
        migrations.AddField(
            model_name='carrier',
            name='metadata',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]
