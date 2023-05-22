# Generated by Django 3.2.12 on 2023-05-03 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tear_sheets', '0008_auto_20230502_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='tearsheet',
            name='gbp_template',
            field=models.CharField(choices=[('A', 'ONE COLUMN DISPLAY'), ('B', 'TWO COLUMN DISPLAY'), ('C', 'RULE TYPE ABOVE')], default='B', max_length=1000),
        ),
    ]
