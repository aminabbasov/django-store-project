# Generated by Django 4.2 on 2023-07-13 08:57

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0006_create_single_product_view"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="public_id",
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]