# Generated by Django 3.2.25 on 2024-04-24 15:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_recipe'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='price',
            new_name='preco',
        ),
    ]
