# Generated by Django 2.1.11 on 2019-12-11 18:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0040_courseteamtabpage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='programlettersignatory',
            name='organization',
        ),
    ]
