# Generated by Django 4.1.1 on 2022-10-11 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_order_city_order_country_order_full_name_order_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='coupon',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
