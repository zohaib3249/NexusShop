# Generated by Django 4.0.2 on 2022-06-24 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_rename_minamount_coupon_min_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='Shippingfee',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='item',
            name='saleTax',
            field=models.IntegerField(default=0),
        ),
    ]
