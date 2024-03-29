# Generated by Django 3.2.9 on 2021-11-22 21:00

from django.db import migrations, models


def forwards_func(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    Customs = apps.get_model("manager", "Customs")

    Customs.objects.using(db_alias).filter(delivered=True).update(status="delivered")

    for customs in Customs.objects.using(db_alias).filter(
        models.Q(aes__isnull=False)
        | models.Q(eel_pfc__isnull=False)
        | models.Q(certificate_number__isnull=False)
    ):
        options = customs.options or dict()

        if options.aes is not None:
            options.update(aes=options.aes)
        if options.eel_pfc is not None:
            options.update(aes=options.eel_pfc)
        if options.certificate_number is not None:
            options.update(aes=options.certificate_number)

        customs.options = options
        customs.save()


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("manager", "0021_tracking_estimated_delivery"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customs",
            name="aes",
        ),
        migrations.RemoveField(
            model_name="customs",
            name="certificate_number",
        ),
        migrations.RemoveField(
            model_name="customs",
            name="eel_pfc",
        ),
    ]
