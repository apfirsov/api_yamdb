# Generated by Django 2.2.16 on 2022-08-29 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('titles', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Categorie',
            new_name='Category',
        ),
    ]