# Generated by Django 4.1.5 on 2023-02-04 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monthly_bills', '0007_alter_inventory_sheets_model_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory_sheets_model',
            name='data',
            field=models.CharField(max_length=10000),
        ),
    ]
