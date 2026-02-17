"""
Migration: Add meta JSONField to Markup model.

The meta field stores structured categorization metadata:
- type: brokerage-fee | insurance | surcharge | notification | address-validation
- plan: free-form plan/tier name
- show_in_preview: whether to show computed column in rate sheet preview
"""

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pricing", "0079_fee_snapshot_model"),
    ]

    operations = [
        migrations.AddField(
            model_name="markup",
            name="meta",
            field=models.JSONField(
                blank=True,
                default=dict,
                help_text=(
                    'Structured categorization metadata: '
                    '{"type": "brokerage-fee", "plan": "scale", "show_in_preview": true}'
                ),
            ),
        ),
    ]
