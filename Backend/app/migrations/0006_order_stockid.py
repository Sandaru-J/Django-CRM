# Generated by Django 4.2.13 on 2024-08-30 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_stock_order_product_id_product_stockid'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='stockId',
            field=models.IntegerField(null=True),
        ),
    ]