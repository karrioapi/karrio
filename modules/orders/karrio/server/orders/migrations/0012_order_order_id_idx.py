# Generated by Django 3.2.13 on 2022-07-10 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_order_billing_address'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['order_id'], name='order_id_idx'),
        ),
    ]
