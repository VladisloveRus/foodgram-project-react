# Generated by Django 3.2.15 on 2022-10-15 10:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_rename_hex_code_tag_color'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='time',
            new_name='cooking_time',
        ),
    ]