# Generated by Django 4.2.1 on 2023-05-25 23:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organisation_name', models.CharField(max_length=100, unique=True)),
                ('address_line_1', models.CharField(blank=True, max_length=100, null=True)),
                ('address_line_2', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('postcode', models.CharField(blank=True, max_length=10, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('contact_number', models.CharField(blank=True, max_length=100, null=True)),
                ('email_address', models.EmailField(max_length=100, unique=True)),
                ('account_number', models.CharField(blank=True, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('active_start_date', models.DateTimeField()),
                ('active_end_date', models.DateTimeField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrganisationPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.CharField(max_length=100)),
                ('method', models.CharField(max_length=100)),
                ('confirmation_code', models.CharField(max_length=100)),
                ('status', models.TextField(max_length=100)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organisations.organisation')),
            ],
        ),
        migrations.CreateModel(
            name='OrganisationManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organisation_role', models.CharField(choices=[('admin', 'admin'), ('manager', 'manager')], max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organisations.organisation')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Organisation Manager',
                'verbose_name_plural': 'Organisation Managers',
            },
        ),
        migrations.CreateModel(
            name='OrganisationClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('grade', models.CharField(max_length=50)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organisations.organisation')),
            ],
            options={
                'verbose_name': 'Organisation Classroom',
                'verbose_name_plural': 'Organisation Classrooms',
                'unique_together': {('name', 'grade', 'organisation')},
            },
        ),
    ]
