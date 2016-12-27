# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-27 21:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import ecommerce.models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('ecommerce', '0009_protect_audit'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_code', models.TextField(blank=True, help_text='The coupon code used for redemption by the purchaser in the user interface.\n    If blank, the purchaser may not redeem this coupon through the user interface,\n    though it may be redeemed in their name by an administrator.', null=True)),
                ('object_id', models.PositiveIntegerField()),
                ('amount_type', models.CharField(choices=[('percent-discount', 'percent-discount'), ('fixed-discount', 'fixed-discount')], help_text='Whether amount is a percent or fixed discount', max_length=30)),
                ('amount', models.DecimalField(decimal_places=2, help_text='Either a number from 0 to 1 representing a percent, or the fixed value for discount', max_digits=20)),
                ('num_coupons_available', models.PositiveIntegerField(help_text='Number of people this coupon can be redeemed by')),
                ('num_redemptions_per_user', models.PositiveIntegerField(help_text='Number of times a person can redeem a coupon')),
                ('expiration_date', models.DateTimeField(help_text='If set, the coupons will not be redeemable after this', null=True)),
                ('activation_date', models.DateTimeField(help_text='If set, the coupons will not be redeemable before this', null=True)),
                ('enabled', models.BooleanField(default=True, help_text='If true, coupons are presently redeemable')),
                ('content_type', models.ForeignKey(help_text='content_object is a link to either a Course, CourseRun, or a Program', null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='RedeemedCoupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ecommerce.Coupon')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ecommerce.Order')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='redeemedcoupon',
            unique_together=set([('order', 'coupon')]),
        ),
    ]
