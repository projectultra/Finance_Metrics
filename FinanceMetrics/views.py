import keras
#import tensorflow as tf
#import pandas as pd
import numpy as np
import requests
import django
import os
import json
import datetime
from FinanceMetrics.models import EconomicIndicators
from FinanceMetrics.models import METAstock
from FinanceMetrics.models import AAPLstock
from FinanceMetrics.models import AMZNstock
from FinanceMetrics.models import NFLXstock
from FinanceMetrics.models import GOOGstock
from django.shortcuts import render
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FM.settings')
django.setup()
# Create your views here.
def DisplayStock(request):
    tdapi_key=os.environ.get('TWELVEDATAAPI_KEY')
    FetchEconomicIndicators()
    FetchMETAstock(tdapi_key)
    FetchAAPLStock(tdapi_key)
    FetchAMZNStock(tdapi_key)
    FetchNFLXStock(tdapi_key)
    FetchGOOGStock(tdapi_key)
    METAstock.close_price = Predictstock(METAstock)
    AAPLstock.close_price = Predictstock(AAPLstock)
    AMZNstock.close_price = Predictstock(AMZNstock)
    NFLXstock.close_price = Predictstock(NFLXstock)
    GOOGstock.close_price = Predictstock(GOOGstock)
    context = {'METAstock': float(METAstock.close_price),
                'AAPLstock': float(AAPLstock.close_price),
                'AMZNstock': float(AMZNstock.close_price),
                'NFLXstock': float(NFLXstock.close_price),
                'GOOGstock': float(GOOGstock.close_price),}
    return render(request, 'FinanceMetrics/Templates/Mainpage.html',context)
def FetchMETAstock(tdapi_key):
    url='https://api.twelvedata.com/time_series?symbol=META&interval=1min&outputsize=1&format=CSV&apikey='+tdapi_key
    response = requests.get(url)
    data = response.text.split("\n")  # split the text by line
    values = data[1].split(";")
    METAstock.open_price=values[1]
    METAstock.high_price=values[2]
    METAstock.low_price=values[3]
    METAstock.close_price=values[4]
    METAstock.volume=values[5]
def FetchAAPLStock(tdapi_key):
    url='https://api.twelvedata.com/time_series?symbol=AAPL&interval=1min&outputsize=1&format=CSV&apikey='+tdapi_key
    response = requests.get(url)
    data = response.text.split("\n")  # split the text by line
    values = data[1].split(";")
    AAPLstock.open_price=values[1]
    AAPLstock.high_price=values[2]
    AAPLstock.low_price=values[3]
    AAPLstock.close_price=values[4]
    AAPLstock.volume=values[5]
def FetchAMZNStock(tdapi_key):
    url='https://api.twelvedata.com/time_series?symbol=AMZN&interval=1min&outputsize=1&format=CSV&apikey='+tdapi_key
    response = requests.get(url)
    data = response.text.split("\n")  # split the text by line
    values = data[1].split(";")
    AMZNstock.open_price=values[1]
    AMZNstock.high_price=values[2]
    AMZNstock.low_price=values[3]
    AMZNstock.close_price=values[4]
    AMZNstock.volume=values[5]
def FetchNFLXStock(tdapi_key):
    url='https://api.twelvedata.com/time_series?symbol=NFLX&interval=1min&outputsize=1&format=CSV&apikey='+tdapi_key
    response = requests.get(url)
    data = response.text.split("\n")  # split the text by line
    values = data[1].split(";")
    NFLXstock.open_price=values[1]
    NFLXstock.high_price=values[2]
    NFLXstock.low_price=values[3]
    NFLXstock.close_price=values[4]
    NFLXstock.volume=values[5]
def FetchGOOGStock(tdapi_key):
    url='https://api.twelvedata.com/time_series?symbol=GOOG&interval=1min&outputsize=1&format=CSV&apikey='+tdapi_key
    response = requests.get(url)
    data = response.text.split("\n")  # split the text by line
    values = data[1].split(";")
    GOOGstock.open_price=values[1]
    GOOGstock.high_price=values[2]
    GOOGstock.low_price=values[3]
    GOOGstock.close_price=values[4]
    GOOGstock.volume=values[5]
def FetchEconomicIndicators():
    api_key=os.environ.get('API_KEY')
    country = 'United States'
    
    url = 'https://api.api-ninjas.com/v1/inflation?country={}'.format(country)
    r = requests.get(url, headers={'X-Api-Key': os.environ.get('NINJAAPI_KEY')})
    EconomicIndicators.inflation = json.loads(r.text)[0]['yearly_rate_pct']
    
    url = 'https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE&interval=daily&datatype=csv&apikey='+api_key
    r = requests.get(url)
    lines = r.text.strip().split('\n')
    EconomicIndicators.interest_rate = lines[1].split(',')[1]
    
    url = 'https://api.api-ninjas.com/v1/convertcurrency?want=GBP&have=USD&amount=1'
    r = requests.get(url, headers={'X-Api-Key': os.environ.get('NINJAAPI_KEY')})
    EconomicIndicators.currency = json.loads(r.text)['new_amount']
def Predictstock(Stock):
    # load model
    if Stock==METAstock:
        model=keras.models.load_model(r'META/METAmodel')
        new_input = np.array([float(Stock.high_price),
                             float(Stock.low_price),
                             float(Stock.open_price),
                             float(EconomicIndicators.interest_rate),
                             float(EconomicIndicators.currency),
                             float(EconomicIndicators.inflation),
                             int(datetime.date.today().strftime("%d")),
                             int(datetime.date.today().strftime("%m"))])
    elif Stock==AAPLstock:
        model=keras.models.load_model(r'APPLE/AAPLmodel')
        new_input = np.array([float(Stock.high_price),
                                float(Stock.low_price),
                                float(Stock.open_price),
                                float(EconomicIndicators.interest_rate),
                                float(EconomicIndicators.currency),
                                float(EconomicIndicators.inflation),
                                int(datetime.date.today().strftime("%m")),
                                int(datetime.date.today().strftime("%d"))])
    elif Stock==AMZNstock:
        model=keras.models.load_model(r'AMAZON/AMZNmodel')
        new_input = np.array([float(Stock.high_price),
                                float(Stock.low_price),
                                float(Stock.open_price),
                                float(EconomicIndicators.interest_rate),
                                float(EconomicIndicators.currency),
                                float(EconomicIndicators.inflation),
                                int(datetime.date.today().strftime("%d")),
                                int(datetime.date.today().strftime("%m"))])
    elif Stock==NFLXstock:
        model=keras.models.load_model(r'NETFLIX/NFLXmodel')
        new_input = np.array([float(Stock.open_price),
                                float(Stock.high_price),
                                float(Stock.low_price),
                                float(EconomicIndicators.interest_rate),
                                float(EconomicIndicators.currency),
                                float(EconomicIndicators.inflation),
                                int(datetime.date.today().strftime("%d")),
                                int(datetime.date.today().strftime("%m"))])
    elif Stock==GOOGstock:
        model=keras.models.load_model(r'GOOGLE/GOOGmodel')
        new_input = np.array([float(Stock.open_price),
                                float(Stock.high_price),
                                float(Stock.low_price),
                                float(EconomicIndicators.interest_rate),
                                float(EconomicIndicators.currency),
                                float(EconomicIndicators.inflation),
                                int(datetime.date.today().strftime("%d")),
                                int(datetime.date.today().strftime("%m"))])
    
    # make prediction
    new_input=new_input.round(2).astype(np.float64)
    new_input=new_input.reshape(1,8)
    Stock.prediction = model.predict(new_input)
    return Stock.prediction