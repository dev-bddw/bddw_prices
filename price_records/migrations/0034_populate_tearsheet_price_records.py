# Data migration to populate TearSheetPriceRecord from existing data

from django.db import migrations


def populate_tearsheet_price_records(apps, schema_editor):
    """
    For each TearSheet, create TearSheetPriceRecord entries for all its CatSeriesItem's price records.
    Set initial display_order from existing order field.
    """
    TearSheet = apps.get_model("tear_sheets", "TearSheet")
    CatSeriesItem = apps.get_model("products", "CatSeriesItem")
    PriceRecord = apps.get_model("price_records", "PriceRecord")
    FormulaPriceRecord = apps.get_model("price_records", "FormulaPriceRecord")
    TearSheetPriceRecord = apps.get_model("price_records", "TearSheetPriceRecord")

    for tearsheet in TearSheet.objects.all():
        # Get all CatSeriesItems for this tearsheet
        cat_series_items = CatSeriesItem.objects.filter(tear_sheet=tearsheet)

        for csi in cat_series_items:
            # Get all price records for this CatSeriesItem
            price_records = PriceRecord.objects.filter(cat_series_item=csi)
            formula_price_records = FormulaPriceRecord.objects.filter(
                cat_series_item=csi
            )

            # Create TearSheetPriceRecord entries for regular price records
            for pr in price_records:
                TearSheetPriceRecord.objects.get_or_create(
                    tear_sheet=tearsheet,
                    price_record=pr,
                    defaults={
                        "display_order": pr.order if pr.order else 0,
                        "is_active": True,
                    },
                )

            # Create TearSheetPriceRecord entries for formula price records
            for fpr in formula_price_records:
                TearSheetPriceRecord.objects.get_or_create(
                    tear_sheet=tearsheet,
                    formula_price_record=fpr,
                    defaults={
                        "display_order": fpr.order if fpr.order else 0,
                        "is_active": True,
                    },
                )


def reverse_populate_tearsheet_price_records(apps, schema_editor):
    """Reverse migration - delete all TearSheetPriceRecord entries"""
    TearSheetPriceRecord = apps.get_model("price_records", "TearSheetPriceRecord")
    TearSheetPriceRecord.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("price_records", "0033_tearsheetpricerecord"),
        ("tear_sheets", "0001_initial"),
        ("products", "0014_alter_catseriesitem_opt_series_item_display"),
    ]

    operations = [
        migrations.RunPython(
            populate_tearsheet_price_records,
            reverse_populate_tearsheet_price_records,
        ),
    ]
