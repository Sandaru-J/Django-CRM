# Generated by Django 4.2.13 on 2024-08-09 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_order_useremail'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock_name', models.CharField(max_length=255)),
                ('supplier_email', models.EmailField(max_length=254)),
                ('quantity', models.PositiveBigIntegerField()),
                ('status', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('date_needed', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='product_ID',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='stockID',
            field=models.IntegerField(null=True),
        ),
    ]
