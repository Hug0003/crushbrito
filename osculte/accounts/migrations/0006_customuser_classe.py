# Generated by Django 4.2.5 on 2023-09-18 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_customuser_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='classe',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
    ]
