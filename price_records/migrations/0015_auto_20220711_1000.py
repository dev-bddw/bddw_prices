# Generated by Django 3.2.12 on 2022-07-11 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('price_records', '0014_auto_20220711_0807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formulapricelistpricerecord',
            name='updated_on',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='pricelistpricerecord',
            name='updated_on',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
