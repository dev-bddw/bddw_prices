# Generated migration for TearSheetPriceRecord model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("tear_sheets", "0001_initial"),
        ("price_records", "0032_auto_20230717_1239"),
    ]

    operations = [
        migrations.CreateModel(
            name="TearSheetPriceRecord",
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
                (
                    "display_order",
                    models.IntegerField(
                        default=0,
                        help_text="Custom ordering for this record on this tearsheet",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="If False, this record is hidden on the tearsheet",
                    ),
                ),
                (
                    "formula_price_record",
                    models.ForeignKey(
                        blank=True,
                        help_text="Formula-based price record (null if using price_record)",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tearsheet_selections",
                        to="price_records.formulapricerecord",
                    ),
                ),
                (
                    "price_record",
                    models.ForeignKey(
                        blank=True,
                        help_text="Regular price record (null if using formula_price_record)",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tearsheet_selections",
                        to="price_records.pricerecord",
                    ),
                ),
                (
                    "tear_sheet",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="price_record_selections",
                        to="tear_sheets.tearsheet",
                    ),
                ),
            ],
            options={
                "ordering": ["display_order", "id"],
            },
        ),
    ]
