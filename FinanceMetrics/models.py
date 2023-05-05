from django.db import models

# Create your models here.
class EconomicIndicators(models.Model):
    inflation=models.FloatField()
    currency=models.FloatField()
    interest_rate=models.FloatField()

class METAstock(models.Model):
    open_price=models.FloatField()
    high_price=models.FloatField()
    low_price=models.FloatField()
    close_price=models.FloatField()
    predicted_price=models.FloatField()
    volume=models.IntegerField()

class AAPLstock(models.Model):
    open_price=models.FloatField()
    high_price=models.FloatField()
    low_price=models.FloatField()
    close_price=models.FloatField()
    predicted_price=models.FloatField()
    volume=models.IntegerField()

class AMZNstock(models.Model):
    open_price=models.FloatField()
    high_price=models.FloatField()
    low_price=models.FloatField()
    close_price=models.FloatField()
    predicted_price=models.FloatField()
    volume=models.IntegerField()

class NFLXstock(models.Model):
    open_price=models.FloatField()
    high_price=models.FloatField()
    low_price=models.FloatField()
    close_price=models.FloatField()
    predicted_price=models.FloatField()
    volume=models.IntegerField()

class GOOGstock(models.Model):
    open_price=models.FloatField()
    high_price=models.FloatField()
    low_price=models.FloatField()
    close_price=models.FloatField()
    predicted_price=models.FloatField()
    volume=models.IntegerField()