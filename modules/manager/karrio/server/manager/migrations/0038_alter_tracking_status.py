# Generated by Django 3.2.13 on 2022-07-16 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0037_auto_20220710_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tracking',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('in_transit', 'in_transit'), ('incident', 'incident'), ('delivered', 'delivered'), ('unknown', 'unknown')], default='pending', max_length=25),
        ),
    ]
