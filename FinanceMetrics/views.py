import keras
import tensorflow as tf
import pandas as pd
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
from FinanceMetrics.models import MSFTstock
from FinanceMetrics.models import TSLAstock
from django.shortcuts import render
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FM.settings')
django.setup()
# Create your views here.
def DisplayStock(request):
    tdapi_key=os.environ.get('TWELVEDATAAPI_KEY')
    FetchEconomicIndicators()
    firsttime=True
    
    if(firsttime):    
        FetchMETAstock(tdapi_key)
        FetchAAPLStock(tdapi_key)
        FetchAMZNStock(tdapi_key)
        FetchNFLXStock(tdapi_key)
        FetchGOOGStock(tdapi_key)
        FetchTSLAStock(tdapi_key)
        FetchMSFTStock(tdapi_key)
        METAstock.predicted_price = Predictstock(METAstock)
        AAPLstock.predicted_price = Predictstock(AAPLstock)
        AMZNstock.predicted_price = Predictstock(AMZNstock)
        NFLXstock.predicted_price = Predictstock(NFLXstock)
        GOOGstock.predicted_price = Predictstock(GOOGstock)
        MSFTstock.predicted_price = Predictstock(MSFTstock)
        TSLAstock.predicted_price = Predictstock(TSLAstock)
        storeprices()
    else:
        fetchprices()
    
    context = {'METAstock': float(METAstock.close_price),
                'AAPLstock': float(AAPLstock.close_price),
                'AMZNstock': float(AMZNstock.close_price),
                'NFLXstock': float(NFLXstock.close_price),
                'GOOGstock': float(GOOGstock.close_price),
                'MSFTstock': float(MSFTstock.close_price),
                'TSLAstock': float(TSLAstock.close_price),}
    return render(request, 'FinanceMetrics/Templates/Mainpage.html',context)
def FetchMETAstock(tdapi_key):
    url='https://api.twelvedata.com/time_series?symbol=META&interval=1day&outputsize=7&format=CSV&apikey='+tdapi_key
    response = requests.get(url)
    #7 days worth of stock input
    data = response.text.split("\n")  # split the text by line
    values = data[1].split(";")
    METAstock.open_price=values[1]
    METAstock.high_price=values[2]
    METAstock.low_price=values[3]
    METAstock.close_price=values[4]
    METAstock.volume=values[5]
def FetchAAPLStock(tdapi_key):
    url='https://api.twelvedata.com/time_series?symbol=AAPL&interval=1day&outputsize=7&format=CSV&apikey='+tdapi_key
    response = requests.get(url)
    data = response.text.split("\n")  # split the text by line
    values = data[1].split(";")
    AAPLstock.open_price=values[1]
    AAPLstock.high_price=values[2]
    AAPLstock.low_price=values[3]
    AAPLstock.close_price=values[4]
    AAPLstock.volume=values[5]
def FetchAMZNStock(tdapi_key):
    url='https://api.twelvedata.com/time_series?symbol=AMZN&interval=1day&outputsize=7&format=CSV&apikey='+tdapi_key
    response = requests.get(url)
    data = response.text.split("\n")  # split the text by line
    values = data[1].split(";")
    AMZNstock.open_price=values[1]
    AMZNstock.high_price=values[2]
    AMZNstock.low_price=values[3]
    AMZNstock.close_price=values[4]
    AMZNstock.volume=values[5]
def FetchNFLXStock(tdapi_key):
    url='https://api.twelvedata.com/time_series?symbol=NFLX&interval=1day&outputsize=7&format=CSV&apikey='+tdapi_key
    response = requests.get(url)
    data = response.text.split("\n")  # split the text by line
    values = data[1].split(";")
    NFLXstock.open_price=values[1]
    NFLXstock.high_price=values[2]
    NFLXstock.low_price=values[3]
    NFLXstock.close_price=values[4]
    NFLXstock.volume=values[5]
def FetchGOOGStock(tdapi_key):
    url='https://api.twelvedata.com/time_series?symbol=GOOG&interval=1day&outputsize=7&format=CSV&apikey='+tdapi_key
    response = requests.get(url)
    data = response.text.split("\n")  # split the text by line
    values = data[1].split(";")
    GOOGstock.open_price=values[1]
    GOOGstock.high_price=values[2]
    GOOGstock.low_price=values[3]
    GOOGstock.close_price=values[4]
    GOOGstock.volume=values[5]
def FetchMSFTStock(tdapi_key):
    url='https://api.twelvedata.com/time_series?symbol=MSFT&interval=1day&outputsize=7&format=CSV&apikey='+tdapi_key
    response = requests.get(url)
    data = response.text.split("\n")  # split the text by line
    values = data[1].split(";")
    MSFTstock.open_price=values[1]
    MSFTstock.high_price=values[2]
    MSFTstock.low_price=values[3]
    MSFTstock.close_price=values[4]
    MSFTstock.volume=values[5]
def FetchTSLAStock(tdapi_key):
    url='https://api.twelvedata.com/time_series?symbol=TSLA&interval=1day&outputsize=7&format=CSV&apikey='+tdapi_key
    response = requests.get(url)
    data = response.text.split("\n")  # split the text by line
    values = data[1].split(";")
    TSLAstock.open_price=values[1]
    TSLAstock.high_price=values[2]
    TSLAstock.low_price=values[3]
    TSLAstock.close_price=values[4]
    TSLAstock.volume=values[5]

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
        model=keras.models.load_model(r'Stock Data/META/METAmodel')
        new_input = np.array([float(Stock.high_price),
                             float(Stock.low_price),
                             float(Stock.open_price),
                             float(Stock.close_price),
                             float(EconomicIndicators.interest_rate),
                             float(EconomicIndicators.currency),
                             float(EconomicIndicators.inflation),
                             int(datetime.date.today().strftime("%d")),
                             int(datetime.date.today().strftime("%m"))])
    elif Stock==AAPLstock:
        model=keras.models.load_model(r'Stock Data/APPLE/AAPLmodel')
        new_input = np.array([float(Stock.high_price),
                                float(Stock.low_price),
                                float(Stock.open_price),
                                float(Stock.close_price),
                                float(EconomicIndicators.interest_rate),
                                float(EconomicIndicators.currency),
                                float(EconomicIndicators.inflation),
                                int(datetime.date.today().strftime("%m")),
                                int(datetime.date.today().strftime("%d"))])
    elif Stock==AMZNstock:
        model=keras.models.load_model(r'Stock Data/AMAZON/AMZNmodel')
        new_input = np.array([float(Stock.high_price),
                                float(Stock.low_price),
                                float(Stock.open_price),
                                float(Stock.close_price),
                                float(EconomicIndicators.interest_rate),
                                float(EconomicIndicators.currency),
                                float(EconomicIndicators.inflation),
                                int(datetime.date.today().strftime("%d")),
                                int(datetime.date.today().strftime("%m"))])
    elif Stock==NFLXstock:
        model=keras.models.load_model(r'Stock Data/NETFLIX/NFLXmodel')
        new_input = np.array([float(Stock.open_price),
                                float(Stock.high_price),
                                float(Stock.low_price),
                                float(Stock.close_price),
                                float(EconomicIndicators.interest_rate),
                                float(EconomicIndicators.currency),
                                float(EconomicIndicators.inflation),
                                int(datetime.date.today().strftime("%d")),
                                int(datetime.date.today().strftime("%m"))])
    elif Stock==GOOGstock:
        model=keras.models.load_model(r'Stock Data/GOOGLE/GOOGmodel')
        new_input = np.array([float(Stock.open_price),
                                float(Stock.high_price),
                                float(Stock.low_price),
                                float(Stock.close_price),
                                float(EconomicIndicators.interest_rate),
                                float(EconomicIndicators.currency),
                                float(EconomicIndicators.inflation),
                                int(datetime.date.today().strftime("%d")),
                                int(datetime.date.today().strftime("%m"))])
    elif Stock==TSLAstock:
        model=keras.models.load_model(r'Stock Data/TESLA/TSLAmodel')
        new_input = np.array([float(Stock.open_price),
                                float(Stock.high_price),
                                float(Stock.low_price),
                                float(Stock.close_price),
                                float(EconomicIndicators.interest_rate),
                                float(EconomicIndicators.currency),
                                float(EconomicIndicators.inflation),
                                int(datetime.date.today().strftime("%d")),
                                int(datetime.date.today().strftime("%m"))])
    elif Stock==MSFTstock:
        model=keras.models.load_model(r'Stock Data/MICROSOFT/MSFTmodel')
        new_input = np.array([float(Stock.open_price),
                                float(Stock.high_price),
                                float(Stock.low_price),
                                float(Stock.close_price),
                                float(EconomicIndicators.interest_rate),
                                float(EconomicIndicators.currency),
                                float(EconomicIndicators.inflation),
                                int(datetime.date.today().strftime("%d")),
                                int(datetime.date.today().strftime("%m"))])
        
    # make prediction
    new_input=new_input.round(3).astype(np.float64)

    Stock.prediction = model.predict(new_input)
    return Stock.prediction

def storeprices():
    PredictedStock=pd.DataFrame()
    PredictedStock=PredictedStock.append({'Apple':AAPLstock.predicted_price,
                                          'Amazon':AMZNstock.predicted_price,
                                          'Meta':METAstock.predicted_price, 
                                          'Netflix':NFLXstock.predicted_price,
                                          'Google':GOOGstock.predicted_price,
                                          'Tesla':TSLAstock.predicted_price,
                                          'Microsoft':MSFTstock.predicted_price},ignore_index=True)
    PredictedStock.to_csv(r'LivePrices/PredictedStock.csv',index=False)
    
def fetchprices():
    AAPLstock.predicted_price=pd.read_csv(r'LivePrices/PredictedStock.csv')['Apple'][0]
    AMZNstock.predicted_price=pd.read_csv(r'LivePrices/PredictedStock.csv')['Amazon'][0]
    METAstock.predicted_price=pd.read_csv(r'LivePrices/PredictedStock.csv')['Meta'][0]
    NFLXstock.predicted_price=pd.read_csv(r'LivePrices/PredictedStock.csv')['Netflix'][0]
    GOOGstock.predicted_price=pd.read_csv(r'LivePrices/PredictedStock.csv')['Google'][0]
    TSLAstock.predicted_price=pd.read_csv(r'LivePrices/PredictedStock.csv')['Tesla'][0]
    MSFTstock.predicted_price=pd.read_csv(r'LivePrices/PredictedStock.csv')['Microsoft'][0]
