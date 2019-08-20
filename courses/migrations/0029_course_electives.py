# Generated by Django 2.1.10 on 2019-07-17 19:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0028_program_num_required_courses'),
    ]

    operations = [
        migrations.CreateModel(
            name='ElectiveCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='courses.Course')),
            ],
        ),
        migrations.CreateModel(
            name='ElectivesSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('required_number', models.PositiveSmallIntegerField()),
                ('title', models.CharField(max_length=255)),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Program')),
            ],
        ),
        migrations.AddField(
            model_name='electivecourse',
            name='electives_set',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.ElectivesSet'),
        ),
    ]