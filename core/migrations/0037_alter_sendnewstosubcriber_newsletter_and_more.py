# Generated by Django 4.0.2 on 2022-06-25 07:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_rename_dat_subcribers_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sendnewstosubcriber',
            name='NewsLetter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.newsletter'),
        ),
        migrations.AlterField(
            model_name='sendnewstosubcriber',
            name='subcriber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.subcribers'),
        ),
    ]
