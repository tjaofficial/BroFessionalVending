# Generated by Django 4.1.5 on 2023-02-03 22:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monthly_bills', '0003_remove_bills_model_charge_date_1_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RS900_model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business', models.CharField(max_length=30)),
                ('date', models.DateField()),
                ('time_start', models.TimeField()),
                ('time_end', models.TimeField()),
                ('technician', models.CharField(max_length=30)),
                ('condition', models.CharField(choices=[('Needs Maintenance ', 'Needs Maintenance '), ('Very Poor', 'Very Poor'), ('Poor', 'Poor'), ('Satisfactory', 'Satisfactory'), ('Great', 'Great')], max_length=30)),
                ('collected', models.FloatField()),
                ('A1', models.CharField(max_length=300)),
                ('A2', models.CharField(max_length=300)),
                ('A3', models.CharField(max_length=300)),
                ('A4', models.CharField(max_length=300)),
                ('A5', models.CharField(max_length=300)),
                ('B1', models.CharField(max_length=300)),
                ('B2', models.CharField(max_length=300)),
                ('B3', models.CharField(max_length=300)),
                ('B4', models.CharField(max_length=300)),
                ('B5', models.CharField(max_length=300)),
                ('B6', models.CharField(max_length=300)),
                ('C1', models.CharField(max_length=300)),
                ('C2', models.CharField(max_length=300)),
                ('C3', models.CharField(max_length=300)),
                ('C4', models.CharField(max_length=300)),
                ('C5', models.CharField(max_length=300)),
                ('C6', models.CharField(max_length=300)),
                ('C7', models.CharField(max_length=300)),
                ('C8', models.CharField(max_length=300)),
                ('C9', models.CharField(max_length=300)),
                ('C10', models.CharField(max_length=300)),
                ('D1', models.CharField(max_length=300)),
                ('D2', models.CharField(max_length=300)),
                ('D3', models.CharField(max_length=300)),
                ('D4', models.CharField(max_length=300)),
                ('D5', models.CharField(max_length=300)),
                ('D6', models.CharField(max_length=300)),
                ('D7', models.CharField(max_length=300)),
                ('D8', models.CharField(max_length=300)),
                ('id_tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monthly_bills.fleet_model')),
            ],
        ),
    ]
