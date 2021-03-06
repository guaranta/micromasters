# Generated by Django 2.1.11 on 2019-12-11 20:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0021_image_file_hash'),
        ('cms', '0041_remove_programlettersignatory_organization'),
    ]

    operations = [
        migrations.AddField(
            model_name='programpage',
            name='program_letter_footer',
            field=models.ForeignKey(blank=True, help_text='The logo that will appear at the bottom of the program congratulation letter.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
    ]
