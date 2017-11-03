# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-10-24 15:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('discussions', '0003_channelprogram'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='query',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='channels', to='search.PercolateQuery'),
        ),
    ]