# Generated by Django 4.2.5 on 2023-09-18 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_remove_customuser_nom_remove_customuser_prenom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='age',
            field=models.CharField(max_length=3),
        ),
    ]