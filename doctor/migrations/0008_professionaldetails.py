# Generated by Django 4.2.7 on 2023-12-04 06:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0007_doctor_bio'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfessionalDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('certificates', models.FileField(blank=True, null=True, upload_to='certificates/')),
                ('clinic_address', models.CharField(blank=True, max_length=255, null=True)),
                ('graduation_year', models.CharField(blank=True, max_length=4, null=True)),
                ('medical_license', models.CharField(blank=True, max_length=20, null=True)),
                ('university', models.CharField(blank=True, max_length=255, null=True)),
                ('consultation_types', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctor.doctor')),
            ],
        ),
    ]
