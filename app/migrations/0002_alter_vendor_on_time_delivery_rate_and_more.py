# Generated by Django 5.0.4 on 2024-05-11 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='on_time_delivery_rate',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='vendorperformance',
            name='on_time_delivery_rate',
            field=models.FloatField(null=True),
        ),
    ]
