# Generated by Django 3.2.12 on 2022-12-21 20:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("price_records", "0023_alter_formulapricerecord_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="pricerecord",
            name="gbp_no_vat",
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="pricerecord",
            name="gbp_price",
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
    ]
