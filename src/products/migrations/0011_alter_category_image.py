# Generated by Django 4.2 on 2023-08-07 05:10

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0010_alter_productoption_values"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="category"),
        ),
    ]