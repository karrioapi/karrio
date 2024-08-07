# Generated by Django 4.2.14 on 2024-07-27 13:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("providers", "0075_haypostsettings"),
    ]

    operations = [
        migrations.RenameField(
            model_name="uspsinternationalsettings",
            old_name="customer_registration_id",
            new_name="account_number",
        ),
        migrations.RenameField(
            model_name="uspsinternationalsettings",
            old_name="logistics_manager_mailer_id",
            new_name="account_type",
        ),
        migrations.RemoveField(
            model_name="uspsinternationalsettings",
            name="mailer_id",
        ),
        migrations.RemoveField(
            model_name="uspsinternationalsettings",
            name="password",
        ),
        migrations.RemoveField(
            model_name="uspsinternationalsettings",
            name="username",
        ),
        migrations.RemoveField(
            model_name="uspssettings",
            name="customer_registration_id",
        ),
        migrations.RemoveField(
            model_name="uspssettings",
            name="logistics_manager_mailer_id",
        ),
        migrations.RemoveField(
            model_name="uspssettings",
            name="mailer_id",
        ),
        migrations.RemoveField(
            model_name="uspssettings",
            name="password",
        ),
        migrations.RemoveField(
            model_name="uspssettings",
            name="username",
        ),
        migrations.AddField(
            model_name="uspsinternationalsettings",
            name="client_id",
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="uspsinternationalsettings",
            name="client_secret",
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="uspssettings",
            name="account_number",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="uspssettings",
            name="account_type",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="uspssettings",
            name="client_id",
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="uspssettings",
            name="client_secret",
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
    ]
