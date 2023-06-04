from django.db import models

# Create your models here.
class EconomicIndicators(models.Model):
    inflation=models.FloatField()
    currency=models.FloatField()
    interest_rate=models.FloatField()
class METAstock(models.Model):
    predicted_price=models.FloatField()
    live_price = models.FloatField(null=True, blank=True)
    percent_change = models.FloatField(null=True, blank=True)
    open_price=models.FloatField(null=True,blank=True)
    close_price=models.FloatField(null=True,blank=True)
    high_price=models.FloatField(null=True,blank=True)
    low_price=models.FloatField(null=True,blank=True)
    volume=models.BigIntegerField(null=True,blank=True)
    price_change=models.FloatField(null=True,blank=True)
    previous_close=models.FloatField(null=True,blank=True)

class MSFTstock(models.Model):
    predicted_price=models.FloatField()
    live_price = models.FloatField(null=True, blank=True)
    percent_change = models.FloatField(null=True, blank=True)
    open_price=models.FloatField(null=True,blank=True)
    close_price=models.FloatField(null=True,blank=True)
    high_price=models.FloatField(null=True,blank=True)
    low_price=models.FloatField(null=True,blank=True)
    volume=models.BigIntegerField(null=True,blank=True)
    price_change=models.FloatField(null=True,blank=True)
    previous_close=models.FloatField(null=True,blank=True)

class TSLAstock(models.Model):
    predicted_price=models.FloatField()
    live_price = models.FloatField(null=True, blank=True)
    percent_change = models.FloatField(null=True, blank=True)
    open_price=models.FloatField(null=True,blank=True)
    close_price=models.FloatField(null=True,blank=True)
    high_price=models.FloatField(null=True,blank=True)
    low_price=models.FloatField(null=True,blank=True)
    volume=models.BigIntegerField(null=True,blank=True)
    price_change=models.FloatField(null=True,blank=True)
    previous_close=models.FloatField(null=True,blank=True)

class AAPLstock(models.Model):
    predicted_price=models.FloatField()
    live_price = models.FloatField(null=True, blank=True)
    percent_change = models.FloatField(null=True, blank=True)
    open_price=models.FloatField(null=True,blank=True)
    close_price=models.FloatField(null=True,blank=True)
    high_price=models.FloatField(null=True,blank=True)
    low_price=models.FloatField(null=True,blank=True)
    volume=models.BigIntegerField(null=True,blank=True)
    price_change=models.FloatField(null=True,blank=True)
    previous_close=models.FloatField(null=True,blank=True)

class AMZNstock(models.Model):
    predicted_price=models.FloatField()
    live_price = models.FloatField(null=True, blank=True)
    percent_change = models.FloatField(null=True, blank=True)
    open_price=models.FloatField(null=True,blank=True)
    close_price=models.FloatField(null=True,blank=True)
    high_price=models.FloatField(null=True,blank=True)
    low_price=models.FloatField(null=True,blank=True)
    volume=models.BigIntegerField(null=True,blank=True)
    price_change=models.FloatField(null=True,blank=True)
    previous_close=models.FloatField(null=True,blank=True)

class NFLXstock(models.Model):
    predicted_price=models.FloatField()
    live_price = models.FloatField(null=True, blank=True)
    percent_change = models.FloatField(null=True, blank=True)
    open_price=models.FloatField(null=True,blank=True)
    close_price=models.FloatField(null=True,blank=True)
    high_price=models.FloatField(null=True,blank=True)
    low_price=models.FloatField(null=True,blank=True)
    volume=models.BigIntegerField(null=True,blank=True)
    price_change=models.FloatField(null=True,blank=True)
    previous_close=models.FloatField(null=True,blank=True)

class GOOGstock(models.Model):
    predicted_price=models.FloatField()
    live_price = models.FloatField(null=True,blank=True)
    percent_change = models.FloatField(null=True,blank=True)
    open_price=models.FloatField(null=True,blank=True)
    close_price=models.FloatField(null=True,blank=True)
    high_price=models.FloatField(null=True,blank=True)
    low_price=models.FloatField(null=True,blank=True)
    volume=models.BigIntegerField(null=True,blank=True)
    price_change=models.FloatField(null=True,blank=True)
    previous_close=models.FloatField(null=True,blank=True)

class commodities(models.Model):
    oil=models.FloatField()
    gold=models.FloatField()
    silver=models.FloatField()
    aluminum=models.FloatField()
    petrol=models.FloatField()

class news1(models.Model):
    title=models.CharField(max_length=1000)
    url=models.CharField(max_length=1000)
    author=models.CharField(max_length=1000)
    summary=models.CharField(max_length=1000)
    urlToImage=models.CharField(max_length=1000)
    source=models.CharField(max_length=1000)
class news2(models.Model):
    title=models.CharField(max_length=1000)
    url=models.CharField(max_length=1000)
    author=models.CharField(max_length=1000)
    summary=models.CharField(max_length=1000)
    urlToImage=models.CharField(max_length=1000)
    source=models.CharField(max_length=1000)
    
class news3(models.Model):
    title=models.CharField(max_length=1000)
    url=models.CharField(max_length=1000)
    author=models.CharField(max_length=1000)
    summary=models.CharField(max_length=1000)
    urlToImage=models.CharField(max_length=1000)
    source=models.CharField(max_length=1000)
    
class news4(models.Model):
    title=models.CharField(max_length=1000)
    url=models.CharField(max_length=1000)
    author=models.CharField(max_length=1000)
    summary=models.CharField(max_length=1000)
    urlToImage=models.CharField(max_length=1000)
    source=models.CharField(max_length=1000)
    
class news5(models.Model):
    title=models.CharField(max_length=1000)
    url=models.CharField(max_length=1000)
    author=models.CharField(max_length=1000)
    summary=models.CharField(max_length=1000)
    urlToImage=models.CharField(max_length=1000)
    source=models.CharField(max_length=1000)

class currency(models.Model):
    EUR=models.FloatField()
    GBP=models.FloatField()
    JPY=models.FloatField()
    CAD=models.FloatField()
    INR=models.FloatField()