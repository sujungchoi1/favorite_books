# Generated by Django 2.2.4 on 2020-12-17 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_favorites', '0004_auto_20201217_2122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='desc',
            field=models.TextField(blank=True, null=True),
        ),
    ]
