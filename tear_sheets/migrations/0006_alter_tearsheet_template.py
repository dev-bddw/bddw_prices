# Generated by Django 3.2.12 on 2022-07-14 15:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tear_sheets", "0005_alter_tearsheet_template"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tearsheet",
            name="template",
            field=models.CharField(
                choices=[
                    ("A", "ONE COLUMN DISPLAY"),
                    ("B", "TWO COLUMN DISPLAY"),
                    ("C", "RULE TYPE ABOVE"),
                ],
                default="B",
                max_length=1000,
            ),
        ),
    ]
