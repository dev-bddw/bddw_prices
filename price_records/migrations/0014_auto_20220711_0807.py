# Generated by Django 3.2.12 on 2022-07-11 13:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("price_records", "0013_alter_pricerecord_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="formulapricelistpricerecord",
            name="updated_on",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name="pricelistpricerecord",
            name="updated_on",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
