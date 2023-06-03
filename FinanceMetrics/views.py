import json
import datetime
import os
import keras
import pandas as pd
import numpy as np
import requests
import django
from django.shortcuts import render
from FinanceMetrics.models import EconomicIndicators
from FinanceMetrics.models import METAstock
from FinanceMetrics.models import AAPLstock
from FinanceMetrics.models import AMZNstock
from FinanceMetrics.models import NFLXstock
from FinanceMetrics.models import GOOGstock
from FinanceMetrics.models import MSFTstock
from FinanceMetrics.models import TSLAstock
from FinanceMetrics.models import commodities
from FinanceMetrics.models import news1,news2,news3,news4,news5
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FM.settings')
django.setup()
# Create your views here.

prevdate=pd.read_csv(r'FinanceMetrics/LivePrices/PredictedStock.csv')['LastDate']
def DisplayStock(request):
    tdapi_key=os.environ.get('TWELVEDATAAPI_KEY')
    if((datetime.datetime.date(datetime.datetime.today()))!=(pd.to_datetime(prevdate).dt.date[0])):
        FetchEconomicIndicators()
        Fetchstock(tdapi_key)
        get_news()
        storeprices(datetime.datetime.today())
    else:
        fetchprices()
    get_stocks()
    context=compiledata()
    context['news']=news1.objects.all()
    return render(request, 'FinanceMetrics/Templates/Mainpage.html',context)

def Fetchstock(tdapi_key):
    url='https://api.twelvedata.com/time_series?symbol=META&interval=1day&outputsize=7&format=CSV&apikey='+tdapi_key
    response = requests.get(url)
    METAstock.predicted_price=Predictstock(METAstock,conversion(response))
    url='https://api.twelvedata.com/time_series?symbol=AAPL&interval=1day&outputsize=7&format=CSV&apikey='+tdapi_key
    response = requests.get(url)
    AAPLstock.predicted_price=Predictstock(AAPLstock,conversion(response))
    url='https://api.twelvedata.com/time_series?symbol=AMZN&interval=1day&outputsize=7&format=CSV&apikey='+tdapi_key
    response = requests.get(url)
    AMZNstock.predicted_price=Predictstock(AMZNstock,conversion(response))
    url='https://api.twelvedata.com/time_series?symbol=NFLX&interval=1day&outputsize=7&format=CSV&apikey='+tdapi_key
    response = requests.get(url)
    NFLXstock.predicted_price=Predictstock(NFLXstock,conversion(response))
    url='https://api.twelvedata.com/time_series?symbol=GOOG&interval=1day&outputsize=7&format=CSV&apikey='+tdapi_key
    response = requests.get(url)
    GOOGstock.predicted_price=Predictstock(GOOGstock,conversion(response))
    url='https://api.twelvedata.com/time_series?symbol=MSFT&interval=1day&outputsize=7&format=CSV&apikey='+tdapi_key
    response = requests.get(url)
    MSFTstock.predicted_price=Predictstock(MSFTstock,conversion(response))
    url='https://api.twelvedata.com/time_series?symbol=TSLA&interval=1day&outputsize=7&format=CSV&apikey='+tdapi_key
    response = requests.get(url)
    TSLAstock.predicted_price=Predictstock(TSLAstock,conversion(response))

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
                                   'NewsTitle': [news1.title],
                                   'Newsurl': [news1.url],
                                   'Newsauthor': [news1.author],
                                   'Newssummary': [news1.summary],
                                   'NewsurlToImage': [news1.urlToImage],
                                   'Newssource': [news1.source],
                                   'LastDate': [lastdate]})
    PredictedStock = pd.concat([PredictedStock], ignore_index=True)
    PredictedStock.to_csv(r'FinanceMetrics/LivePrices/PredictedStock.csv',index=False)

def fetchprices():
    AAPLstock.predicted_price=pd.read_csv(r'FinanceMetrics/LivePrices/PredictedStock.csv')['Apple'][0]
    AMZNstock.predicted_price=pd.read_csv(r'FinanceMetrics/LivePrices/PredictedStock.csv')['Amazon'][0]
    METAstock.predicted_price=pd.read_csv(r'FinanceMetrics/LivePrices/PredictedStock.csv')['Meta'][0]
    NFLXstock.predicted_price=pd.read_csv(r'FinanceMetrics/LivePrices/PredictedStock.csv')['Netflix'][0]
    GOOGstock.predicted_price=pd.read_csv(r'FinanceMetrics/LivePrices/PredictedStock.csv')['Google'][0]
    TSLAstock.predicted_price=pd.read_csv(r'FinanceMetrics/LivePrices/PredictedStock.csv')['Tesla'][0]
    MSFTstock.predicted_price=pd.read_csv(r'FinanceMetrics/LivePrices/PredictedStock.csv')['Microsoft'][0]
    news1.title=pd.read_csv(r'FinanceMetrics/LivePrices/PredictedStock.csv')['NewsTitle'][0]
    news1.url=pd.read_csv(r'FinanceMetrics/LivePrices/PredictedStock.csv')['Newsurl'][0]
    news1.author=pd.read_csv(r'FinanceMetrics/LivePrices/PredictedStock.csv')['Newsauthor'][0]
    news1.summary=pd.read_csv(r'FinanceMetrics/LivePrices/PredictedStock.csv')['Newssummary'][0]
    news1.urlToImage=pd.read_csv(r'FinanceMetrics/LivePrices/PredictedStock.csv')['NewsurlToImage'][0]
    news1.source=pd.read_csv(r'FinanceMetrics/LivePrices/PredictedStock.csv')['Newssource'][0]

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
            float(EconomicIndicators.interest_rate),
            float(EconomicIndicators.currency),
            float(EconomicIndicators.inflation),
            int(date.day),
            int(date.month),
        ]
        data_rows.append(row)
    return(np.array(data_rows))

def get_stocks():
    stocks_api_key=os.environ.get('STOCKS_API_KEY')
    stocks2_api_key=os.environ.get('STOCKS2_API_KEY')
    symbol = 'AAPL'
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={stocks_api_key}'
    response = requests.get(url)   
    data = response.json() 
    AAPLstock.open_price = data['Global Quote']['02. open']
    AAPLstock.high_price = data['Global Quote']['03. high']
    AAPLstock.low_price = data['Global Quote']['04. low']
    AAPLstock.live_price = data['Global Quote']['05. price']
    AAPLstock.volume = data['Global Quote']['06. volume']
    AAPLstock.previous_close = data['Global Quote']['08. previous close']
    AAPLstock.price_change = data['Global Quote']['09. change']
    AAPLstock.percent_change = data['Global Quote']['10. change percent']

    symbol = 'AMZN'
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={stocks_api_key}'
    response = requests.get(url)   
    data = response.json() 
    AMZNstock.open_price = data['Global Quote']['02. open']
    AMZNstock.high_price = data['Global Quote']['03. high']
    AMZNstock.low_price = data['Global Quote']['04. low']
    AMZNstock.live_price = data['Global Quote']['05. price']
    AMZNstock.volume = data['Global Quote']['06. volume']
    AMZNstock.previous_close = data['Global Quote']['08. previous close']
    AMZNstock.price_change = data['Global Quote']['09. change']
    AMZNstock.percent_change = data['Global Quote']['10. change percent']

    symbol = 'MSFT'  
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={stocks_api_key}'
    response = requests.get(url)   
    data = response.json() 
    MSFTstock.open_price = data['Global Quote']['02. open']
    MSFTstock.high_price = data['Global Quote']['03. high']
    MSFTstock.low_price = data['Global Quote']['04. low']
    MSFTstock.live_price = data['Global Quote']['05. price']
    MSFTstock.volume = data['Global Quote']['06. volume']
    MSFTstock.previous_close = data['Global Quote']['08. previous close']
    MSFTstock.price_change = data['Global Quote']['09. change']
    MSFTstock.percent_change = data['Global Quote']['10. change percent']

    symbol = 'META'
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={stocks_api_key}'
    response = requests.get(url)   
    data = response.json() 
    METAstock.open_price = data['Global Quote']['02. open']
    METAstock.high_price = data['Global Quote']['03. high']
    METAstock.low_price = data['Global Quote']['04. low']
    METAstock.live_price = data['Global Quote']['05. price']
    METAstock.volume = data['Global Quote']['06. volume']
    METAstock.previous_close = data['Global Quote']['08. previous close']
    METAstock.price_change = data['Global Quote']['09. change']
    METAstock.percent_change = data['Global Quote']['10. change percent']
    
    symbol = 'NFLX'
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={stocks_api_key}'
    response = requests.get(url)   
    data = response.json() 
    NFLXstock.open_price = data['Global Quote']['02. open']
    NFLXstock.high_price = data['Global Quote']['03. high']
    NFLXstock.low_price = data['Global Quote']['04. low']
    NFLXstock.live_price = data['Global Quote']['05. price']
    NFLXstock.volume = data['Global Quote']['06. volume']
    NFLXstock.previous_close = data['Global Quote']['08. previous close']
    NFLXstock.price_change = data['Global Quote']['09. change']
    NFLXstock.percent_change = data['Global Quote']['10. change percent']
    
    symbol = 'GOOG'
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={stocks2_api_key}'
    response = requests.get(url) 
    data = response.json() 
    GOOGstock.open_price = data['Global Quote']['02. open']
    GOOGstock.high_price = data['Global Quote']['03. high']
    GOOGstock.low_price = data['Global Quote']['04. low']
    GOOGstock.live_price = data['Global Quote']['05. price']
    GOOGstock.volume = data['Global Quote']['06. volume']
    GOOGstock.previous_close = data['Global Quote']['08. previous close']
    GOOGstock.price_change = data['Global Quote']['09. change']
    GOOGstock.percent_change = data['Global Quote']['10. change percent']
    
    symbol = 'TSLA'
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={stocks2_api_key}'
    response = requests.get(url)   
    data = response.json() 
    TSLAstock.open_price = data['Global Quote']['02. open']
    TSLAstock.high_price = data['Global Quote']['03. high']
    TSLAstock.low_price = data['Global Quote']['04. low']
    TSLAstock.live_price = data['Global Quote']['05. price']
    TSLAstock.volume = data['Global Quote']['06. volume']
    TSLAstock.previous_close = data['Global Quote']['08. previous close']
    TSLAstock.price_change = data['Global Quote']['09. change']
    TSLAstock.percent_change = data['Global Quote']['10. change percent']
    
def get_commodities():
    com_api_key=os.environ.get('COMMODITIES_API_KEY')
    comm = 'COPPER'
    url = f'https://www.alphavantage.co/query?function={comm}&apikey={com_api_key}&interval=monthly'
    response = requests.get(url)
    data = response.json()
    commodities.copper=data['data'][0]['value']

    comm = 'NATURAL_GAS'
    url = f'https://www.alphavantage.co/query?function={comm}&apikey={com_api_key}&interval=monthly'
    response = requests.get(url)
    data = response.json()
    commodities.natgas=data['data'][0]['value']

    comm = 'ALUMINUM'
    url = f'https://www.alphavantage.co/query?function={comm}&apikey={com_api_key}&interval=monthly'
    response = requests.get(url)
    data = response.json()
    commodities.aluminum=data['data'][0]['value']

    comm = 'BRENT' #(oil)
    url = f'https://www.alphavantage.co/query?function={comm}&apikey={com_api_key}&interval=monthly'
    response = requests.get(url)
    data = response.json()
    commodities.crudeoil=data['data'][0]['value']

    comm = 'WHEAT'
    url = f'https://www.alphavantage.co/query?function={comm}&apikey={com_api_key}&interval=monthly'
    response = requests.get(url)
    data = response.json()
    commodities.wheat=data['data'][0]['value']

def get_news():
    news_api_key=os.environ.get('NEWS_API_KEY')
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&apikey={news_api_key}&topics=finance'
    response = requests.get(url)
    data=response.json()
    news1.title = data['feed'][0]['title']
    news1.url = data['feed'][0]['url']
    news1.author = data['feed'][0]['authors']
    news1.summary = data['feed'][0]['summary']
    news1.urlToImage = data['feed'][0]['banner_image']
    news1.source = data['feed'][0]['source']
    
def compiledata():
    AMZNstock_data = {
    'prediction':AMZNstock.predicted_price,
    'live_price':AMZNstock.live_price,
    'open_price':AMZNstock.open_price,
    'high_price':AMZNstock.high_price,
    'low_price':AMZNstock.low_price,
    'percent_change':AMZNstock.percent_change,
    'price_change':AMZNstock.price_change,
    'previous_close':AMZNstock.previous_close,
    'volume':AMZNstock.volume}
    AAPLstock_data = {
    'prediction':AAPLstock.predicted_price,
    'live_price':AAPLstock.live_price,
    'open_price':AAPLstock.open_price,
    'high_price':AAPLstock.high_price,
    'low_price':AAPLstock.low_price,
    'percent_change':AAPLstock.percent_change,
    'price_change':AAPLstock.price_change,
    'previous_close':AAPLstock.previous_close,
    'volume':AAPLstock.volume}
    METAstock_data = {
    'prediction':METAstock.predicted_price,
    'live_price':METAstock.live_price,
    'open_price':METAstock.open_price,
    'high_price':METAstock.high_price,
    'low_price':METAstock.low_price,
    'percent_change':METAstock.percent_change,
    'price_change':METAstock.price_change,
    'previous_close':METAstock.previous_close,
    'volume':METAstock.volume}
    NFLXstock_data = {
    'prediction':NFLXstock.predicted_price,
    'live_price':NFLXstock.live_price,
    'open_price':NFLXstock.open_price,
    'high_price':NFLXstock.high_price,
    'low_price':NFLXstock.low_price,
    'percent_change':NFLXstock.percent_change,
    'price_change':NFLXstock.price_change,
    'previous_close':NFLXstock.previous_close,
    'volume':NFLXstock.volume}
    GOOGstock_data = {
    'prediction':GOOGstock.predicted_price,
    'live_price':GOOGstock.live_price,
    'open_price':GOOGstock.open_price,
    'high_price':GOOGstock.high_price,
    'low_price':GOOGstock.low_price,
    'percent_change':GOOGstock.percent_change,
    'price_change':GOOGstock.price_change,
    'previous_close':GOOGstock.previous_close,
    'volume':GOOGstock.volume}
    TSLAstock_data = {
    'prediction':TSLAstock.predicted_price,
    'live_price':TSLAstock.live_price,
    'open_price':TSLAstock.open_price,
    'high_price':TSLAstock.high_price,
    'low_price':TSLAstock.low_price,
    'percent_change':TSLAstock.percent_change,
    'price_change':TSLAstock.price_change,
    'previous_close':TSLAstock.previous_close,
    'volume':TSLAstock.volume}
    MSFTstock_data = {
    'prediction':MSFTstock.predicted_price,
    'live_price':MSFTstock.live_price,
    'open_price':MSFTstock.open_price,
    'high_price':MSFTstock.high_price,
    'low_price':MSFTstock.low_price,
    'percent_change':MSFTstock.percent_change,
    'price_change':MSFTstock.price_change,
    'previous_close':MSFTstock.previous_close,
    'volume':MSFTstock.volume}
    context = {'AMZNstock_data': AMZNstock_data,
               'AAPLstock_data': AAPLstock_data,
               'METAstock_data': METAstock_data,
               'NFLXstock_data': NFLXstock_data,
               'GOOGstock_data': GOOGstock_data,
               'TSLAstock_data': TSLAstock_data,
               'MSFTstock_data': MSFTstock_data
               }
    return context