# Generated by Django 3.2.12 on 2022-06-29 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_catseriesitem_opt_series_item_display'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['order'], 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['order'], 'verbose_name_plural': 'Items'},
        ),
        migrations.AlterModelOptions(
            name='series',
            options={'ordering': ['order'], 'verbose_name_plural': 'Series'},
        ),
        migrations.AddField(
            model_name='category',
            name='order',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='order',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='series',
            name='order',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]