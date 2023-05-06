from django.db import models

# Create your models here.
class EconomicIndicators(models.Model):
    inflation=models.FloatField()
    currency=models.FloatField()
    interest_rate=models.FloatField()
class METAstock(models.Model):
    predicted_price=models.FloatField()

class MSFTstock(models.Model):
    predicted_price=models.FloatField()

class TSLAstock(models.Model):
    predicted_price=models.FloatField()

class AAPLstock(models.Model):
    predicted_price=models.FloatField()

class AMZNstock(models.Model):
    predicted_price=models.FloatField()

class NFLXstock(models.Model):
    predicted_price=models.FloatField()

class GOOGstock(models.Model):
    predicted_price=models.FloatField()