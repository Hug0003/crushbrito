# Generated by Django 4.2.5 on 2023-12-01 16:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_detail_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detail',
            name='user',
        ),
    ]
