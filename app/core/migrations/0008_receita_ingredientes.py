# Generated by Django 3.2.25 on 2024-04-26 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_ingrediente'),
    ]

    operations = [
        migrations.AddField(
            model_name='receita',
            name='ingredientes',
            field=models.ManyToManyField(to='core.Ingrediente'),
        ),
    ]
