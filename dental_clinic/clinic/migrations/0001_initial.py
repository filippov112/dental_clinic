# Generated by Django 5.1.2 on 2024-10-13 21:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Region', models.CharField(max_length=100)),
                ('City', models.CharField(max_length=100)),
                ('Street', models.CharField(max_length=100)),
                ('House', models.IntegerField()),
                ('Letter', models.CharField(blank=True, max_length=10, null=True)),
                ('Building', models.IntegerField(blank=True, null=True)),
                ('Apartment', models.IntegerField(blank=True, null=True)),
                ('ZipCode', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Photo', models.ImageField(blank=True, null=True, upload_to='photos/doctor/')),
                ('LastName', models.CharField(max_length=100)),
                ('FirstName', models.CharField(max_length=100)),
                ('MiddleName', models.CharField(blank=True, max_length=100, null=True)),
                ('WorkSchedule', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='DoctorCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='DoctorSpecialization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ChangeSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Absence', models.BooleanField(default=False)),
                ('StartDate', models.DateField()),
                ('EndDate', models.DateField()),
                ('StartTime', models.TimeField(blank=True, null=True)),
                ('EndTime', models.TimeField(blank=True, null=True)),
                ('Doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic.doctor')),
            ],
        ),
        migrations.AddField(
            model_name='doctor',
            name='Category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='clinic.doctorcategory'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='Specialization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='clinic.doctorspecialization'),
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('LastName', models.CharField(max_length=100)),
                ('FirstName', models.CharField(max_length=100)),
                ('MiddleName', models.CharField(blank=True, max_length=100, null=True)),
                ('BirthDate', models.DateField()),
                ('Address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='clinic.address')),
            ],
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Phone', models.CharField(max_length=15)),
                ('Note', models.CharField(blank=True, max_length=255, null=True)),
                ('Doctor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='clinic.doctor')),
                ('Patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='clinic.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=255)),
                ('Description', models.TextField()),
                ('Specialization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic.doctorspecialization')),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateField()),
                ('Time', models.TimeField()),
                ('Author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('Doctor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='clinic.doctor')),
                ('Patient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='clinic.patient')),
                ('Service', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='clinic.service')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceCost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Cost', models.IntegerField()),
                ('Category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='clinic.doctorcategory')),
                ('Service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic.service')),
            ],
        ),
        migrations.CreateModel(
            name='RenderedService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Record', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='clinic.record')),
                ('ServiceCost', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='clinic.servicecost')),
            ],
        ),
    ]
