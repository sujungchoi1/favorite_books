# Generated by Django 2.2.4 on 2020-12-17 07:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_favorites', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='desc',
            new_name='description',
        ),
    ]
