# Generated by Django 3.2.12 on 2022-06-16 17:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tear_sheets", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="tearsheet",
            name="updated_on",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
