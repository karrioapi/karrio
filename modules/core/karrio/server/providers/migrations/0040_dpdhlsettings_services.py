# Generated by Django 3.2.14 on 2022-09-06 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('providers', '0039_auto_20220906_0612'),
    ]

    operations = [
        migrations.AddField(
            model_name='dpdhlsettings',
            name='services',
            field=models.ManyToManyField(blank=True, to='providers.ServiceLevel'),
        ),
    ]
