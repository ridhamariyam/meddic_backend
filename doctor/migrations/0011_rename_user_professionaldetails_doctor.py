# Generated by Django 4.2.7 on 2023-12-04 08:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0010_alter_professionaldetails_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='professionaldetails',
            old_name='user',
            new_name='doctor',
        ),
    ]
