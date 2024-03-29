# Generated by Django 3.2.11 on 2022-03-03 12:10

from django.db import migrations, models
import functools
import karrio.server.core.models.base


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='webhook',
            name='secret',
            field=models.CharField(default=functools.partial(karrio.server.core.models.base.uuid, *(), **{'prefix': 'whsec_'}), max_length=100),
        ),
        migrations.AlterField(
            model_name='webhook',
            name='id',
            field=models.CharField(default=functools.partial(karrio.server.core.models.base.uuid, *(), **{'prefix': 'weh_'}), editable=False, max_length=50, primary_key=True, serialize=False),
        ),
    ]
