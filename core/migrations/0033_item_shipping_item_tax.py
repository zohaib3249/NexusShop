# Generated by Django 4.0.2 on 2022-06-24 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_remove_item_shipping_remove_item_tax'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='Shipping',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='item',
            name='Tax',
            field=models.IntegerField(default=0),
        ),
    ]
