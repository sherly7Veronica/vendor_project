# Generated by Django 5.0.4 on 2024-05-11 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_vendor_on_time_delivery_rate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='quality_rating',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='average_response_time',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='fulfillment_rate',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='quality_rating_avg',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='vendorperformance',
            name='average_response_time',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='vendorperformance',
            name='fulfillment_rate',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='vendorperformance',
            name='quality_rating_avg',
            field=models.FloatField(null=True),
        ),
    ]