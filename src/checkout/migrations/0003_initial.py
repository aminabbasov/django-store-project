# Generated by Django 4.2 on 2023-06-28 17:04

from django.conf import settings
from django.db import migrations
from django.db import models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("checkout", "0002_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="address",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
