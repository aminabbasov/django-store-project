# Generated by Django 4.2 on 2023-07-12 13:25

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("checkout", "0004_remove_order_updated_remove_orderitem_color_and_more"),
    ]

    operations = [
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
                max_length=30,
            ),
        ),
    ]
