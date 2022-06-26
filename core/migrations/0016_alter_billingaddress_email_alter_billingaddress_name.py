# Generated by Django 4.0.2 on 2022-06-21 19:23

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_billingaddress_email_billingaddress_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billingaddress',
            name='email',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='name',
            field=django_countries.fields.CountryField(default=None, max_length=100, null=True),
        ),
    ]