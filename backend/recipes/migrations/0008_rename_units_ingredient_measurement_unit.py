# Generated by Django 3.2.15 on 2022-10-16 10:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_auto_20221016_0649'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredient',
            old_name='units',
            new_name='measurement_unit',
        ),
    ]
