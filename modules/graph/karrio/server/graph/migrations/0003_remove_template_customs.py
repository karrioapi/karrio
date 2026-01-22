from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("graph", "0002_auto_20210512_1353"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="template",
            name="customs",
        ),
    ]
