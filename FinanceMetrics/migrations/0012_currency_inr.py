# Generated by Django 4.2.1 on 2023-06-03 05:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("FinanceMetrics", "0011_currency"),
    ]

    operations = [
        migrations.AddField(
            model_name="currency",
            name="INR",
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
