# Generated by Django 4.2.5 on 2023-12-02 11:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_remove_detail_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Detail',
        ),
    ]