# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-10-25 15:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0025_remove_unused_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='should_display_progress',
            field=models.BooleanField(default=True),
        ),
    ]