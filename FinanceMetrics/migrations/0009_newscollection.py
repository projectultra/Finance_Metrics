# Generated by Django 4.2.1 on 2023-05-31 12:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("FinanceMetrics", "0008_news"),
    ]

    operations = [
        migrations.CreateModel(
            name="NewsCollection",
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
                ("articles", models.ManyToManyField(to="FinanceMetrics.news")),
            ],
        ),
    ]