# Generated by Django 4.2.5 on 2023-11-18 18:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_rename_nouveaux_messages_customuser_nouveau_message'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='nouveau_message',
            new_name='lu',
        ),
    ]