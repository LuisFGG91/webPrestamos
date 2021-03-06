# Generated by Django 4.0.2 on 2022-02-15 21:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Users', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prestamos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_lent', models.IntegerField()),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('borrowerProfile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.borrowerprofile')),
                ('lenderProfile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.lenderprofile')),
            ],
            options={
                'verbose_name': 'prestamo',
                'verbose_name_plural': 'prestamos',
            },
        ),
    ]
