# Generated migration for TearSheetFormatting model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("tear_sheets", "0011_alter_tearsheet_sdata"),
    ]

    operations = [
        migrations.CreateModel(
            name="TearSheetFormatting",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("last_updated", models.DateTimeField(auto_now=True)),
                (
                    "formatting_data",
                    models.JSONField(
                        default=dict,
                        help_text="Stores sdata, gbp_sdata, template choices, and other formatting preferences",
                    ),
                ),
                (
                    "tear_sheet",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="formatting_snapshot",
                        to="tear_sheets.tearsheet",
                    ),
                ),
            ],
            options={
                "verbose_name": "Tearsheet Formatting Snapshot",
                "verbose_name_plural": "Tearsheet Formatting Snapshots",
            },
        ),
    ]
