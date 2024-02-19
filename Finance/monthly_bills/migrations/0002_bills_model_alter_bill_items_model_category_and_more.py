# Generated by Django 4.1.5 on 2023-01-31 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monthly_bills', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='bills_model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('budget_amt', models.DecimalField(decimal_places=2, max_digits=6)),
                ('charge_date_1', models.DateField(blank=True, null=True)),
                ('category', models.CharField(choices=[('Automotive', 'Automotive'), ('Food', 'Food'), ('Phone', 'Phone'), ('Rent', 'Rent'), ('Studio', 'Studio'), ('Music', 'Music'), ('Alcohol', 'Alcohol'), ('Vending', 'Vending'), ('Extra', 'Extra'), ('Personal', 'Personal')], max_length=30)),
                ('billing_period', models.CharField(choices=[('Annually', 'Annually'), ('Semi-Annually', 'Semi-Annually'), ('Quarterly', 'Quarterly'), ('Monthly', 'Monthly'), ('Bi-Monthly', 'Bi-Monthly'), ('Weekly', 'Weekly')], max_length=30)),
                ('charge_date_2', models.DateField(blank=True, null=True)),
                ('source', models.CharField(max_length=30)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('stop_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='bill_items_model',
            name='category',
            field=models.CharField(choices=[('Automotive', 'Automotive'), ('Food', 'Food'), ('Phone', 'Phone'), ('Rent', 'Rent'), ('Studio', 'Studio'), ('Music', 'Music'), ('Alcohol', 'Alcohol'), ('Vending', 'Vending'), ('Extra', 'Extra'), ('Personal', 'Personal')], max_length=30),
        ),
        migrations.AlterField(
            model_name='purchase_model',
            name='category',
            field=models.CharField(choices=[('Automotive', 'Automotive'), ('Food', 'Food'), ('Phone', 'Phone'), ('Rent', 'Rent'), ('Studio', 'Studio'), ('Music', 'Music'), ('Alcohol', 'Alcohol'), ('Vending', 'Vending'), ('Extra', 'Extra'), ('Personal', 'Personal')], max_length=30),
        ),
    ]
