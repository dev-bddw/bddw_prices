# Generated by Django 3.2.12 on 2022-09-06 18:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0013_alter_category_pricelist_ignore"),
    ]

    operations = [
        migrations.AlterField(
            model_name="catseriesitem",
            name="opt_series_item_display",
            field=models.CharField(
                blank=True,
                default=None,
                help_text="Display alternate series item string?",
                max_length=200,
                null=True,
            ),
        ),
    ]
