# Generated by Django 5.0.6 on 2024-05-28 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='record',
            old_name='creation_date',
            new_name='date_joined',
        ),
    ]
