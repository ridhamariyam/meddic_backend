# Generated by Django 4.2.7 on 2023-12-04 07:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0009_alter_professionaldetails_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professionaldetails',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctor.doctor'),
        ),
    ]
