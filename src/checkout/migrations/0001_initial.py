# Generated by Django 4.2 on 2023-06-28 17:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("modified", models.DateTimeField(blank=True, db_index=True, null=True)),
                ("first_name", models.CharField(max_length=255)),
                ("last_name", models.CharField(max_length=255)),
                ("email", models.EmailField(max_length=255)),
                ("phone_number", models.CharField(blank=True, max_length=255)),
                ("address_line_1", models.CharField(max_length=255)),
                ("address_line_2", models.CharField(blank=True, max_length=255)),
                (
                    "country",
                    models.CharField(
                        choices=[
                            ("us", "United States"),
                            ("germany", "Germany"),
                            ("turkey", "Turkey"),
                            ("uae", "United Arab Emirates"),
                            ("thailand", "Thailand"),
                            ("japan", "Japan"),
                        ],
                        default="us",
                        max_length=30,
                    ),
                ),
                ("city", models.CharField(max_length=255)),
                ("state", models.CharField(blank=True, max_length=255)),
                ("zip_code", models.CharField(blank=True, max_length=255)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("price", models.DecimalField(decimal_places=2, max_digits=7)),
                ("paid", models.BooleanField(default=False)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Pending", "Pending"),
                            ("Approved", "Approved"),
                            ("In transit", "In transit"),
                            ("Shipped", "Shipped"),
                        ],
                        default="Pending",
                        max_length=30,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("modified", models.DateTimeField(blank=True, db_index=True, null=True)),
                ("price", models.DecimalField(decimal_places=2, max_digits=7)),
                (
                    "size",
                    models.CharField(
                        choices=[(None, "Select size"), ("XS", "XS"), ("S", "S"), ("M", "M"), ("L", "L"), ("XL", "XL")],
                        max_length=30,
                    ),
                ),
                (
                    "color",
                    models.CharField(
                        choices=[
                            (None, "Select color"),
                            ("black", "Black"),
                            ("white", "White"),
                            ("red", "Red"),
                            ("blue", "Blue"),
                            ("green", "Green"),
                        ],
                        max_length=30,
                    ),
                ),
                ("quantity", models.PositiveIntegerField(default=1)),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="items", to="checkout.order"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
