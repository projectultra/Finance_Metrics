# Generated by Django 4.2.1 on 2023-06-06 08:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("FinanceMetrics", "0013_rename_copper_commodities_gold_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="news6",
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
                ("title", models.CharField(max_length=1000)),
                ("url", models.CharField(max_length=1000)),
                ("author", models.CharField(max_length=1000)),
                ("summary", models.CharField(max_length=1000)),
                ("urlToImage", models.CharField(max_length=1000)),
                ("source", models.CharField(max_length=1000)),
            ],
        ),
    ]
