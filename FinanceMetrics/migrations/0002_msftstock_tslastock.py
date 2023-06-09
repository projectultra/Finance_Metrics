# Generated by Django 4.2.1 on 2023-05-06 12:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("FinanceMetrics", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="MSFTstock",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("open_price", models.FloatField()),
                ("high_price", models.FloatField()),
                ("low_price", models.FloatField()),
                ("close_price", models.FloatField()),
                ("predicted_price", models.FloatField()),
                ("volume", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="TSLAstock",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("open_price", models.FloatField()),
                ("high_price", models.FloatField()),
                ("low_price", models.FloatField()),
                ("close_price", models.FloatField()),
                ("predicted_price", models.FloatField()),
                ("volume", models.IntegerField()),
            ],
        ),
    ]
