# Generated by Django 4.0.2 on 2022-02-15 21:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('first_name', models.CharField(max_length=254, verbose_name='Nombre')),
                ('last_name', models.CharField(max_length=254, verbose_name='Apellidos')),
                ('is_lander', models.BooleanField(default=False, verbose_name='Es lender')),
                ('is_borrower', models.BooleanField(default=False, verbose_name='Es borrower')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.CreateModel(
            name='LenderProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money', models.IntegerField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'LenderProfile',
                'verbose_name_plural': 'LanderProfiles',
            },
        ),
        migrations.CreateModel(
            name='BorrowerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('need_money_for', models.CharField(max_length=100, verbose_name='Need money for')),
                ('description', models.CharField(max_length=5000, unique=True, verbose_name='Description')),
                ('amount_need', models.IntegerField(verbose_name='Amount need')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'BorrowerProfile',
                'verbose_name_plural': 'BorrowerProfiles',
            },
        ),
    ]
