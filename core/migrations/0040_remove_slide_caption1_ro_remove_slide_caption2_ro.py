# Generated by Django 4.0.2 on 2022-06-25 18:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0039_alter_slide_caption1_ro_alter_slide_caption2_ro'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='slide',
            name='caption1_ro',
        ),
        migrations.RemoveField(
            model_name='slide',
            name='caption2_ro',
        ),
    ]
