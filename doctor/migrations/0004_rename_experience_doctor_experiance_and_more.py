# Generated by Django 4.2.7 on 2023-11-28 12:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0003_rename_experiance_doctor_experience_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='doctor',
            old_name='experience',
            new_name='experiance',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='languages_spoken',
        ),
    ]
