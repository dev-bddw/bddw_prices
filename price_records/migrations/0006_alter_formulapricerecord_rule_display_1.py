# Generated by Django 3.2.12 on 2022-06-20 19:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("price_records", "0005_alter_formulapricerecord_rule_display_2"),
    ]

    operations = [
        migrations.AlterField(
            model_name="formulapricerecord",
            name="rule_display_1",
            field=models.CharField(
                blank=True, help_text="ex. 67 x 19 x 29 H", max_length=200, null=True
            ),
        ),
    ]
