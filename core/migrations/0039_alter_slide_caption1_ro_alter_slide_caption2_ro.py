# Generated by Django 4.0.2 on 2022-06-25 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_rename_caption1_slide_caption1_en_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slide',
            name='caption1_ro',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='slide',
            name='caption2_ro',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
