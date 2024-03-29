# Generated by Django 3.2.12 on 2022-03-23 15:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('providers', '0027_auto_20220304_1340'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='labeltemplate',
            name='alias',
        ),
        migrations.RemoveField(
            model_name='labeltemplate',
            name='description',
        ),
        migrations.AddField(
            model_name='labeltemplate',
            name='shipment_sample',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AddField(
            model_name='labeltemplate',
            name='slug',
            field=models.SlugField(default='SVG_TPL', max_length=30, validators=[django.core.validators.RegexValidator('^[a-z0-9_]+$')]),
            preserve_default=False,
        ),
    ]
