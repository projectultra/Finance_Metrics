from django.test import TestCase

# Create your tests here.
import json
import datetime
import os
import keras
import pandas as pd
import numpy as np
import requests
import django
#from FinanceMetrics.models import EconomicIndicators
from FinanceMetrics.models import METAstock
from FinanceMetrics.models import AAPLstock
from FinanceMetrics.models import AMZNstock
from FinanceMetrics.models import NFLXstock
from FinanceMetrics.models import GOOGstock
from FinanceMetrics.models import MSFTstock
from FinanceMetrics.models import TSLAstock
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FM.settings')
django.setup()
#from django.conf import settings
#settings.configure()
prevdate=pd.read_csv(r'FinanceMetrics/LivePrices/PredictedStock.csv')['LastDate']
interest_rate=0.0
inflation_rate=0.0
currency_rate=0.0
def DisplayStock():
    tdapi_key=os.environ.get('TWELVEDATAAPI_KEY')
    if((datetime.datetime.date(datetime.datetime.today()))!=(pd.to_datetime(prevdate).dt.date[0])):
        FetchEconomicIndicators()
        FetchMETAstock(tdapi_key)
        FetchAAPLStock(tdapi_key)
        FetchAMZNStock(tdapi_key)
        FetchNFLXStock(tdapi_key)
        FetchGOOGStock(tdapi_key)
        FetchTSLAStock(tdapi_key)
        FetchMSFTStock(tdapi_key)
        storeprices(datetime.datetime.today())
def FetchMETAstock(tdapi_key):
    url='https://api.twelvedata.com/time_series?symbol=META&interval=1day&outputsize=7&format=CSV&apikey='+tdapi_key
    response = requests.get(url)
    METAstock.predicted_price=Predictstock(METAstock,conversion(response))
    print('Meta:',METAstock.predicted_price)

def FetchAAPLStock(tdapi_key):
    url='https://api.twelvedata.com/time_series?symbol=AAPL&interval=1day&outputsize=7&format=CSV&apikey='+tdapi_key
    response = requests.get(url)
    AAPLstock.predicted_price=Predictstock(AAPLstock,conversion(response))
    print('Apple:',AAPLstock.predicted_price)

def FetchAMZNStock(tdapi_key):
    url='https://api.twelvedata.com/time_series?symbol=AMZN&interval=1day&outputsize=7&format=CSV&apikey='+tdapi_key
    response = requests.get(url)
    AMZNstock.predicted_price=Predictstock(AMZNstock,conversion(response))
    print('Amazon:',AMZNstock.predicted_price)

def FetchNFLXStock(tdapi_key):
    url='https://api.twelvedata.com/time_series?symbol=NFLX&interval=1day&outputsize=7&format=CSV&apikey='+tdapi_key
    response = requests.get(url)
    NFLXstock.predicted_price=Predictstock(NFLXstock,conversion(response))
    print('Netflix:',NFLXstock.predicted_price)

def FetchGOOGStock(tdapi_key):
    url='https://api.twelvedata.com/time_series?symbol=GOOG&interval=1day&outputsize=7&format=CSV&apikey='+tdapi_key
    response = requests.get(url)
    GOOGstock.predicted_price=Predictstock(GOOGstock,conversion(response))
    print('Google:',GOOGstock.predicted_price)

def FetchMSFTStock(tdapi_key):
    url='https://api.twelvedata.com/time_series?symbol=MSFT&interval=1day&outputsize=7&format=CSV&apikey='+tdapi_key
    response = requests.get(url)
    MSFTstock.predicted_price=Predictstock(MSFTstock,conversion(response))
    print('Microsoft:',MSFTstock.predicted_price)

def FetchTSLAStock(tdapi_key):
    url='https://api.twelvedata.com/time_series?symbol=TSLA&interval=1day&outputsize=7&format=CSV&apikey='+tdapi_key
    response = requests.get(url)
    TSLAstock.predicted_price=Predictstock(TSLAstock,conversion(response))
    print('Tesla:',TSLAstock.predicted_price)

def FetchEconomicIndicators():
    api_key=os.environ.get('API_KEY')
    country = 'United States'

    url = 'https://api.api-ninjas.com/v1/inflation?country={}'.format(country)
    r = requests.get(url, headers={'X-Api-Key': os.environ.get('NINJAAPI_KEY')})
    print(json.loads(r.text)[0]['yearly_rate_pct'])

    url = 'https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE&interval=daily&datatype=csv&apikey='+api_key
    r = requests.get(url)
    lines = r.text.strip().split('\n')
    print(lines[1].split(',')[1])

    url = 'https://api.api-ninjas.com/v1/convertcurrency?want=GBP&have=USD&amount=1'
    r = requests.get(url, headers={'X-Api-Key': os.environ.get('NINJAAPI_KEY')})
    print(json.loads(r.text)['new_amount'])

def Predictstock(Stock,data_array):

    if Stock==METAstock:
        model=keras.models.load_model(r'Stock Data/META/METAmodel')

    elif Stock==AAPLstock:
        model=keras.models.load_model(r'Stock Data/APPLE/AAPLmodel')

    elif Stock==AMZNstock:
        model=keras.models.load_model(r'Stock Data/AMAZON/AMZNmodel')

    elif Stock==NFLXstock:
        model=keras.models.load_model(r'Stock Data/NETFLIX/NFLXmodel')

    elif Stock==GOOGstock:
        model=keras.models.load_model(r'Stock Data/GOOGLE/GOOGmodel')

    elif Stock==TSLAstock:
        model=keras.models.load_model(r'Stock Data/TESLA/TSLAmodel')

    elif Stock==MSFTstock:
        model=keras.models.load_model(r'Stock Data/MICROSOFT/MSFTmodel')
    Stock.prediction = model.predict(data_array.reshape(1,7,9))
    return Stock.prediction

def storeprices(lastdate):
    PredictedStock = pd.DataFrame({'Apple': [float(AAPLstock.predicted_price)],
                                   'Amazon': [float(AMZNstock.predicted_price)],
                                   'Meta': [float(METAstock.predicted_price)], 
                                   'Netflix': [float(NFLXstock.predicted_price)],
                                   'Google': [float(GOOGstock.predicted_price)],
                                   'Tesla': [float(TSLAstock.predicted_price)],
                                   'Microsoft': [float(MSFTstock.predicted_price)],
                                   'LastDate': [lastdate]})
    PredictedStock = pd.concat([PredictedStock], ignore_index=True)
    PredictedStock.to_csv(r'FinanceMetrics/LivePrices/PredictedStock.csv',index=False)

def conversion(response):
    lines = response.text.split("\n")[1:-1]
    data_rows = []
    for line in lines:
        values = line.split(";")
        date_string = values[0]
        date = datetime.datetime.strptime(date_string,'%Y-%m-%d')
        row = [
            float(values[1]),  # open
            float(values[2]),  # high
            float(values[3]),  # low
            float(values[4]),  # close
            float(interest_rate),
            float(currency_rate),
            float(inflation_rate),
            int(date.day),
            int(date.month),
        ]
        data_rows.append(row)
    return(np.array(data_rows))
DisplayStock()
print('Apple:',pd.read_csv(r'FinanceMetrics/LivePrices/PredictedStock.csv')['Apple'][0],
      'Amazon',pd.read_csv(r'FinanceMetrics/LivePrices/PredictedStock.csv')['Amazon'][0],
      'Meta',pd.read_csv(r'FinanceMetrics/LivePrices/PredictedStock.csv')['Meta'][0],
      'Netflix',pd.read_csv(r'FinanceMetrics/LivePrices/PredictedStock.csv')['Netflix'][0],
      'Google',pd.read_csv(r'FinanceMetrics/LivePrices/PredictedStock.csv')['Google'][0],
      'Tesla',pd.read_csv(r'FinanceMetrics/LivePrices/PredictedStock.csv')['Tesla'][0],
      'Microsoft',pd.read_csv(r'FinanceMetrics/LivePrices/PredictedStock.csv')['Microsoft'][0])