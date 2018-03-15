# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-28 20:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.migrations.operations.special
from django.utils.text import slugify


# NOTE: the slug field added below is adjusted from the original 0026_frequentlyaskedquestion_slug to
# fix a migration issue relating to the Django 1.11 upgrade. Since this migration should only run for brand new
# installations


def gen_unique_slug(apps, schema_editor):
    FrequentlyAskedQuestion = apps.get_model('cms', 'FrequentlyAskedQuestion')
    for row in FrequentlyAskedQuestion.objects.all():
        if not row.slug:
            max_length = FrequentlyAskedQuestion._meta.get_field('slug').max_length
            slug = orig_slug = slugify(row.question)[:max_length]
            slug_is_unique = not FrequentlyAskedQuestion.objects.filter(slug=orig_slug).exists()
            count = 1
            while not slug_is_unique:
                slug = "{orig}-{count}".format(
                    orig=orig_slug[:max_length - len(str(count)) - 1],
                    count=count)
                slug_is_unique = not FrequentlyAskedQuestion.objects.filter(slug=slug).exists()
                count += 1
            row.slug = slug
            row.save()


class Migration(migrations.Migration):

    replaces = [('cms', '0026_frequentlyaskedquestion_slug')]

    dependencies = [
        ('cms', '0025_infolinks'),
    ]

    operations = [
        migrations.AddField(
            model_name='frequentlyaskedquestion',
            name='slug',
            field=models.SlugField(blank=True, default=None, unique=True),
        ),
        migrations.RunPython(
            code=gen_unique_slug,
            reverse_code=django.db.migrations.operations.special.RunPython.noop,
        ),
    ]