# Generated by Django 3.2.7 on 2021-11-09 04:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0009_auto_20211109_0436'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expense',
            old_name='Category',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='income',
            old_name='Category',
            new_name='category',
        ),
    ]
