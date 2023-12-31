# Generated by Django 4.2 on 2023-07-12 15:49

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("checkout", "0005_alter_order_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="country",
            field=models.CharField(
                choices=[
                    ("US", "United States"),
                    ("DE", "Germany"),
                    ("TR", "Turkey"),
                    ("AE", "United Arab Emirates"),
                    ("TH", "Thailand"),
                    ("JP", "Japan"),
                ],
                default="US",
                max_length=255,
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("Not paid", "Not paid"),
                    ("Pending", "Pending"),
                    ("Approved", "Approved"),
                    ("In transit", "In transit"),
                    ("Shipped", "Shipped"),
                ],
                default="Not paid",
                max_length=255,
            ),
        ),
    ]
