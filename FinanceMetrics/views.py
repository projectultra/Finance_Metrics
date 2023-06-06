import json
import datetime
import os
import keras
import pandas as pd
import numpy as np
import requests
import yfinance as yf
import django
from django.shortcuts import render
from FinanceMetrics.models import EconomicIndicators,commodities,currency
from FinanceMetrics.models import METAstock,AAPLstock,AMZNstock,NFLXstock,GOOGstock,MSFTstock,TSLAstock
from FinanceMetrics.models import news1,news2,news3,news4,news5,news6
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FM.settings')
django.setup()
# Create your views here.

prevdate=pd.read_csv(r'FinanceMetrics/LivePrices/PredictedStock.csv')['date']
def DisplayStock(request):
    tdapi_key=os.environ.get('TWELVEDATAAPI_KEY')
    if((datetime.datetime.date(datetime.datetime.today()))!=(pd.to_datetime(prevdate).dt.date[0])):
        FetchEconomicIndicators()
        Fetchstock(tdapi_key)
        get_news()
        get_currency()
        get_stocks()
        get_commodities()
        storeprices(datetime.datetime.today())
    else:
        fetchprices()
    context=compiledata()
    return render(request,'FinanceMetrics/Templates/index.html',context)

def Fetchstock(tdapi_key):
    model=keras.models.load_model(r'Stock Data/models')
    url='https://api.twelvedata.com/time_series?symbol=META&interval=1day&outputsize=14&format=CSV&apikey='+tdapi_key
    response = requests.get(url)
    METAstock.predicted_price=model.predict(conversion(response).reshape(1,14,9))
    url='https://api.twelvedata.com/time_series?symbol=AAPL&interval=1day&outputsize=14&format=CSV&apikey='+tdapi_key
    response = requests.get(url)
    AAPLstock.predicted_price=model.predict(conversion(response).reshape(1,14,9))
    url='https://api.twelvedata.com/time_series?symbol=AMZN&interval=1day&outputsize=14&format=CSV&apikey='+tdapi_key
    response = requests.get(url)
    AMZNstock.predicted_price=model.predict(conversion(response).reshape(1,14,9))
    url='https://api.twelvedata.com/time_series?symbol=NFLX&interval=1day&outputsize=14&format=CSV&apikey='+tdapi_key
    response = requests.get(url)
    NFLXstock.predicted_price=model.predict(conversion(response).reshape(1,14,9))
    url='https://api.twelvedata.com/time_series?symbol=GOOG&interval=1day&outputsize=14&format=CSV&apikey='+tdapi_key
    response = requests.get(url)
    GOOGstock.predicted_price=model.predict(conversion(response).reshape(1,14,9))
    url='https://api.twelvedata.com/time_series?symbol=MSFT&interval=1day&outputsize=14&format=CSV&apikey='+tdapi_key
    response = requests.get(url)
    MSFTstock.predicted_price=model.predict(conversion(response).reshape(1,14,9))
    url='https://api.twelvedata.com/time_series?symbol=TSLA&interval=1day&outputsize=14&format=CSV&apikey='+tdapi_key
    response = requests.get(url)
    TSLAstock.predicted_price=model.predict(conversion(response).reshape(1,14,9))

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

def storeprices(lastdate):
    PredictedStock = pd.DataFrame({
        'AAPL':[float(AAPLstock.predicted_price),
                AAPLstock.live_price,
                AAPLstock.open_price,
                AAPLstock.high_price,
                AAPLstock.low_price,
                int(AAPLstock.volume),
                AAPLstock.price_change,
                AAPLstock.previous_close],
        'AMZN':[float(AMZNstock.predicted_price),
                AMZNstock.live_price,
                AMZNstock.open_price,
                AMZNstock.high_price,
                AMZNstock.low_price,
                int(AMZNstock.volume),
                AMZNstock.price_change,
                AMZNstock.previous_close],
        'GOOG':[float(GOOGstock.predicted_price),
                GOOGstock.live_price,
                GOOGstock.open_price,
                GOOGstock.high_price,
                GOOGstock.low_price,
                int(GOOGstock.volume),
                GOOGstock.price_change,
                GOOGstock.previous_close],
        'META':[float(METAstock.predicted_price),   
                METAstock.live_price,
                METAstock.open_price,
                METAstock.high_price,
                METAstock.low_price,
                int(METAstock.volume),
                METAstock.price_change,
                METAstock.previous_close],
        'MSFT':[float(MSFTstock.predicted_price),
                MSFTstock.live_price,
                MSFTstock.open_price,
                MSFTstock.high_price,
                MSFTstock.low_price,
                int(MSFTstock.volume),
                MSFTstock.price_change,
                MSFTstock.previous_close],
        'NFLX':[float(NFLXstock.predicted_price),
                NFLXstock.live_price,
                NFLXstock.open_price,
                NFLXstock.high_price,
                NFLXstock.low_price,
                int(NFLXstock.volume),
                NFLXstock.price_change,
                NFLXstock.previous_close],
        'TSLA':[float(TSLAstock.predicted_price),
                TSLAstock.live_price,
                TSLAstock.open_price,
                TSLAstock.high_price,
                TSLAstock.low_price,
                int(TSLAstock.volume),
                TSLAstock.price_change,
                TSLAstock.previous_close]
    })

    NewsData = pd.DataFrame({
        'News1': [news1.title,
                  news1.url,
                  news1.author,
                  news1.summary,
                  news1.urlToImage,
                  news1.source],
        'News2': [news2.title,
                    news2.url,
                    news2.author,
                    news2.summary,
                    news2.urlToImage,
                    news2.source],
        'News3': [news3.title,
                    news3.url,
                    news3.author,
                    news3.summary,
                    news3.urlToImage,
                    news3.source],
        'News4': [news4.title,
                    news4.url,
                    news4.author,
                    news4.summary,
                    news4.urlToImage,
                    news4.source],
        'News5': [news5.title,
                    news5.url,
                    news5.author,
                    news5.summary,
                    news5.urlToImage,
                    news5.source],
        'News6': [news6.title,
                    news6.url,
                    news6.author,
                    news6.summary,
                    news6.urlToImage,
                    news6.source],
        })           

    curr_commod = pd.DataFrame({
        'currency':[currency.EUR,
                    currency.GBP,
                    currency.JPY,
                    currency.CAD,
                    currency.INR],
        'commodities':[  commodities.oil,
                    commodities.gold,
                    commodities.silver,
                    commodities.aluminum,
                    commodities.petrol],})
    
    date = pd.DataFrame({'date':[lastdate]})
    PredStock = pd.concat([PredictedStock , NewsData, curr_commod,date],axis=1)
    PredStock.to_csv('FinanceMetrics/LivePrices/PredictedStock.csv', index=False)

def fetchprices():
    cachedata=pd.read_csv('FinanceMetrics/LivePrices/PredictedStock.csv')
    AAPLstock.predicted_price=cachedata['AAPL'][0]
    AAPLstock.live_price=cachedata['AAPL'][1]
    AAPLstock.open_price=cachedata['AAPL'][2]
    AAPLstock.high_price=cachedata['AAPL'][3]
    AAPLstock.low_price=cachedata['AAPL'][4]
    AAPLstock.volume=cachedata['AAPL'][5]
    AAPLstock.price_change=cachedata['AAPL'][6]
    AAPLstock.previous_close=cachedata['AAPL'][7]
    
    AMZNstock.predicted_price=cachedata['AMZN'][0]
    AMZNstock.live_price=cachedata['AMZN'][1]
    AMZNstock.open_price=cachedata['AMZN'][2]
    AMZNstock.high_price=cachedata['AMZN'][3]
    AMZNstock.low_price=cachedata['AMZN'][4]
    AMZNstock.volume=cachedata['AMZN'][5]
    AMZNstock.price_change=cachedata['AMZN'][6]
    AMZNstock.previous_close=cachedata['AMZN'][7]
    
    GOOGstock.predicted_price=cachedata['GOOG'][0]
    GOOGstock.live_price=cachedata['GOOG'][1]
    GOOGstock.open_price=cachedata['GOOG'][2]
    GOOGstock.high_price=cachedata['GOOG'][3]
    GOOGstock.low_price=cachedata['GOOG'][4]
    GOOGstock.volume=cachedata['GOOG'][5]
    GOOGstock.price_change=cachedata['GOOG'][6]
    GOOGstock.previous_close=cachedata['GOOG'][7]
    
    METAstock.predicted_price=cachedata['META'][0]
    METAstock.live_price=cachedata['META'][1]
    METAstock.open_price=cachedata['META'][2]
    METAstock.high_price=cachedata['META'][3]
    METAstock.low_price=cachedata['META'][4]
    METAstock.volume=cachedata['META'][5]
    METAstock.price_change=cachedata['META'][6]
    METAstock.previous_close=cachedata['META'][7]
    
    MSFTstock.predicted_price=cachedata['MSFT'][0]
    MSFTstock.live_price=cachedata['MSFT'][1]
    MSFTstock.open_price=cachedata['MSFT'][2]
    MSFTstock.high_price=cachedata['MSFT'][3]
    MSFTstock.low_price=cachedata['MSFT'][4]
    MSFTstock.volume=cachedata['MSFT'][5]
    MSFTstock.price_change=cachedata['MSFT'][6]
    MSFTstock.previous_close=cachedata['MSFT'][7]
    
    NFLXstock.predicted_price=cachedata['NFLX'][0]
    NFLXstock.live_price=cachedata['NFLX'][1]
    NFLXstock.open_price=cachedata['NFLX'][2]
    NFLXstock.high_price=cachedata['NFLX'][3]
    NFLXstock.low_price=cachedata['NFLX'][4]
    NFLXstock.volume=cachedata['NFLX'][5]
    NFLXstock.price_change=cachedata['NFLX'][6]
    NFLXstock.previous_close=cachedata['NFLX'][7]
    
    TSLAstock.predicted_price=cachedata['TSLA'][0]
    TSLAstock.live_price=cachedata['TSLA'][1]
    TSLAstock.open_price=cachedata['TSLA'][2]
    TSLAstock.high_price=cachedata['TSLA'][3]
    TSLAstock.low_price=cachedata['TSLA'][4]
    TSLAstock.volume=cachedata['TSLA'][5]
    TSLAstock.price_change=cachedata['TSLA'][6]
    TSLAstock.previous_close=cachedata['TSLA'][7]
    
    news1.title=cachedata['News1'][0]
    news1.url=cachedata['News1'][1]
    news1.author=cachedata['News1'][2]
    news1.summary=cachedata['News1'][3]
    news1.urlToImage=cachedata['News1'][4]
    news1.source=cachedata['News1'][5]
    
    news2.title=cachedata['News2'][0]
    news2.url=cachedata['News2'][1]
    news2.author=cachedata['News2'][2]
    news2.summary=cachedata['News2'][3]
    news2.urlToImage=cachedata['News2'][4]
    news2.source=cachedata['News2'][5]
    
    news3.title=cachedata['News3'][0]
    news3.url=cachedata['News3'][1]
    news3.author=cachedata['News3'][2]
    news3.summary=cachedata['News3'][3]
    news3.urlToImage=cachedata['News3'][4]
    news3.source=cachedata['News3'][5]
    
    news4.title=cachedata['News4'][0]
    news4.url=cachedata['News4'][1]
    news4.author=cachedata['News4'][2]
    news4.summary=cachedata['News4'][3]
    news4.urlToImage=cachedata['News4'][4]
    news4.source=cachedata['News4'][5]
    
    news5.title=cachedata['News5'][0]
    news5.url=cachedata['News5'][1]
    news5.author=cachedata['News5'][2]
    news5.summary=cachedata['News5'][3]
    news5.urlToImage=cachedata['News5'][4]
    news5.source=cachedata['News5'][5]
    
    currency.EUR=cachedata['currency'][0]
    currency.GBP=cachedata['currency'][1]
    currency.JPY=cachedata['currency'][2]
    currency.CAD=cachedata['currency'][3]
    currency.INR=cachedata['currency'][4]
    
    commodities.oil=cachedata['commodities'][0]
    commodities.gold=cachedata['commodities'][1]
    commodities.silver=cachedata['commodities'][2]
    commodities.aluminum=cachedata['commodities'][3]
    commodities.petrol=cachedata['commodities'][4]

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
            int(date.month),]
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
    AAPLstock.volume = int(data['Global Quote']['06. volume'])
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
    AMZNstock.volume = int(data['Global Quote']['06. volume'])
    AMZNstock.previous_close = data['Global Quote']['08. previous close']
    AMZNstock.price_change = data['Global Quote']['09. change']
    AMZNstock.percent_change = data['Global Quote']['10. change percent']

    endpoint = 'https://finnhub.io/api/v1/quote'
    params = {'symbol': 'MSFT',
              'token': stocks2_api_key}
    response = requests.get(endpoint, params=params)
    data = response.json()
    MSFTstock.open_price = data['o']
    MSFTstock.high_price = data['h']
    MSFTstock.low_price = data['l']
    MSFTstock.live_price = data['c']
    MSFTstock.volume = int(data['t'])
    MSFTstock.previous_close = data['pc']
    MSFTstock.percent_change = data['dp']
    MSFTstock.price_change = data['d']

    params = {'symbol': 'META',
                'token': stocks2_api_key}
    response = requests.get(endpoint, params=params)
    data = response.json()
    METAstock.open_price = data['o']
    METAstock.high_price = data['h']
    METAstock.low_price = data['l']
    METAstock.live_price = data['c']
    METAstock.volume = int(data['t'])
    METAstock.previous_close = data['pc']
    METAstock.percent_change = data['dp']
    METAstock.price_change = data['d']
    
    params = {'symbol': 'NFLX',
              'token': stocks2_api_key}
    response = requests.get(endpoint, params=params)
    data = response.json()
    NFLXstock.open_price = data['o']
    NFLXstock.high_price = data['h']
    NFLXstock.low_price = data['l']
    NFLXstock.live_price = data['c']
    NFLXstock.volume = int(data['t'])
    NFLXstock.previous_close = data['pc']
    NFLXstock.percent_change = data['dp']
    NFLXstock.price_change = data['d']
    
    symbol = 'GOOG'
    params = {'symbol': 'GOOG',
                'token': stocks2_api_key}
    response = requests.get(endpoint, params=params)
    data = response.json()
    GOOGstock.open_price = data['o']
    GOOGstock.high_price = data['h']
    GOOGstock.low_price = data['l']
    GOOGstock.live_price = data['c']
    GOOGstock.volume = int(data['t'])
    GOOGstock.previous_close = data['pc']
    GOOGstock.percent_change = data['dp']
    GOOGstock.price_change = data['d']
    
    symbol = 'TSLA'
    params = {'symbol': 'TSLA',
                'token': stocks2_api_key}
    response = requests.get(endpoint, params=params)
    data = response.json()
    TSLAstock.open_price = data['o']
    TSLAstock.high_price = data['h']
    TSLAstock.low_price = data['l']
    TSLAstock.live_price = data['c']
    TSLAstock.volume = int(data['t'])
    TSLAstock.previous_close = data['pc']
    TSLAstock.percent_change = data['dp']
    TSLAstock.price_change = data['d']
    
def get_commodities():
    commodity_ticker = yf.Ticker("GC=F")
    commodities.gold = commodity_ticker.history(period="5d")["Close"].iloc[-1]
    
    commodity_ticker = yf.Ticker("SI=F")
    commodities.silver = commodity_ticker.history(period="5d")["Close"].iloc[-1]
    
    commodity_ticker = yf.Ticker("ALI=F")
    commodities.aluminum = commodity_ticker.history(period="5d")["Close"].iloc[-1]
    
    commodity_ticker = yf.Ticker("CL=F")
    commodities.oil = commodity_ticker.history(period="5d")["Close"].iloc[-1]
    
    commodity_ticker = yf.Ticker("RB=F")
    commodities.petrol = commodity_ticker.history(period="5d")["Close"].iloc[-1]

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
    news1.source = data['feed'][1]['source']
    
    news2.title = data['feed'][1]['title']
    news2.url = data['feed'][1]['url']
    news2.author = data['feed'][1]['authors']
    news2.summary = data['feed'][1]['summary']
    news2.urlToImage = data['feed'][1]['banner_image']
    news2.source = data['feed'][1]['source']
    
    news3.title = data['feed'][2]['title']
    news3.url = data['feed'][2]['url']
    news3.author = data['feed'][2]['authors']
    news3.summary = data['feed'][2]['summary']
    news3.urlToImage = data['feed'][2]['banner_image']
    news3.source = data['feed'][2]['source']
    
    news4.title = data['feed'][3]['title']
    news4.url = data['feed'][3]['url']
    news4.author = data['feed'][3]['authors']
    news4.summary = data['feed'][3]['summary']
    news4.urlToImage = data['feed'][3]['banner_image']
    news4.source = data['feed'][3]['source']
    
    news5.title = data['feed'][4]['title']
    news5.url = data['feed'][4]['url']
    news5.author = data['feed'][4]['authors']
    news5.summary = data['feed'][4]['summary']
    news5.urlToImage = data['feed'][4]['banner_image']
    news5.source = data['feed'][4]['source']
    
    news6.title = data['feed'][5]['title']
    news6.url = data['feed'][5]['url']
    news6.author = data['feed'][5]['authors']
    news6.summary = data['feed'][5]['summary']
    news6.urlToImage = data['feed'][5]['banner_image']
    news6.source = data['feed'][5]['source']
    
def compiledata():
    AMZNstock_data = {
    'prediction':round(float(AMZNstock.predicted_price),2),
    'live_price':AMZNstock.live_price,
    'open_price':AMZNstock.open_price,
    'high_price':AMZNstock.high_price,
    'low_price':AMZNstock.low_price,
    'percent_change':AMZNstock.percent_change,
    'price_change':AMZNstock.price_change,
    'previous_close':AMZNstock.previous_close,
    'volume':AMZNstock.volume}
    AAPLstock_data = {
    'prediction':round(float(AAPLstock.predicted_price),2),
    'live_price':AAPLstock.live_price,
    'open_price':AAPLstock.open_price,
    'high_price':AAPLstock.high_price,
    'low_price':AAPLstock.low_price,
    'percent_change':AAPLstock.percent_change,
    'price_change':AAPLstock.price_change,
    'previous_close':AAPLstock.previous_close,
    'volume':AAPLstock.volume}
    METAstock_data = {
    'prediction':round(float(METAstock.predicted_price),2),
    'live_price':METAstock.live_price,
    'open_price':METAstock.open_price,
    'high_price':METAstock.high_price,
    'low_price':METAstock.low_price,
    'percent_change':METAstock.percent_change,
    'price_change':METAstock.price_change,
    'previous_close':METAstock.previous_close,
    'volume':METAstock.volume}
    NFLXstock_data = {
    'prediction':round(float(NFLXstock.predicted_price),2),
    'live_price':NFLXstock.live_price,
    'open_price':NFLXstock.open_price,
    'high_price':NFLXstock.high_price,
    'low_price':NFLXstock.low_price,
    'percent_change':NFLXstock.percent_change,
    'price_change':NFLXstock.price_change,
    'previous_close':NFLXstock.previous_close,
    'volume':NFLXstock.volume}
    GOOGstock_data = {
    'prediction':round(float(GOOGstock.predicted_price),2),
    'live_price':GOOGstock.live_price,
    'open_price':GOOGstock.open_price,
    'high_price':GOOGstock.high_price,
    'low_price':GOOGstock.low_price,
    'percent_change':GOOGstock.percent_change,
    'price_change':GOOGstock.price_change,
    'previous_close':GOOGstock.previous_close,
    'volume':GOOGstock.volume}
    TSLAstock_data = {
    'prediction':round(float(TSLAstock.predicted_price),2),
    'live_price':TSLAstock.live_price,
    'open_price':TSLAstock.open_price,
    'high_price':TSLAstock.high_price,
    'low_price':TSLAstock.low_price,
    'percent_change':TSLAstock.percent_change,
    'price_change':TSLAstock.price_change,
    'previous_close':TSLAstock.previous_close,
    'volume':TSLAstock.volume}
    MSFTstock_data = {
    'prediction':round(float(MSFTstock.predicted_price),2),
    'live_price':MSFTstock.live_price,
    'open_price':MSFTstock.open_price,
    'high_price':MSFTstock.high_price,
    'low_price':MSFTstock.low_price,
    'percent_change':MSFTstock.percent_change,
    'price_change':MSFTstock.price_change,
    'previous_close':MSFTstock.previous_close,
    'volume':MSFTstock.volume}
    livecurrency_data = {
    'EUR':round(currency.EUR,2),
    'GBP':round(currency.GBP,2),
    'JPY':round(currency.JPY,2),
    'CAD':round(currency.CAD,2),
    'INR':round(currency.INR,2)}
    livecommodity_data = {
    'GOLD':round(commodities.gold,2),
    'OIL':round(commodities.oil,2),
    'SILVER':round(commodities.silver,2),
    'PETROL':round(commodities.petrol,2),
    'ALUMINIUM':round(commodities.aluminum,2)}
    news1_data = {
    'title':news1.title,
    'url':news1.url,
    'author':news1.author,
    'summary':news1.summary,
    'urlToImage':news1.urlToImage,
    'source':news1.source}
    news2_data = {
    'title':news2.title,
    'url':news2.url,
    'author':news2.author,
    'summary':news2.summary,
    'urlToImage':news2.urlToImage,
    'source':news2.source}
    news3_data = {
    'title':news3.title,
    'url':news3.url,
    'author':news3.author,
    'summary':news3.summary,
    'urlToImage':news3.urlToImage,
    'source':news3.source}
    news4_data = {
    'title':news4.title,
    'url':news4.url,
    'author':news4.author,
    'summary':news4.summary,
    'urlToImage':news4.urlToImage,
    'source':news4.source}
    news5_data = {
    'title':news5.title,
    'url':news5.url,
    'author':news5.author,
    'summary':news5.summary,
    'urlToImage':news5.urlToImage,
    'source':news5.source}
    news6_data = {
        'title':news6.title,
        'url':news6.url,
        'author':news6.author,
        'summary':news6.summary,
        'urlToImage':news6.urlToImage,
        'source':news6.source}
    
    context = {'AMZNstock_data': AMZNstock_data,
               'AAPLstock_data': AAPLstock_data,
               'METAstock_data': METAstock_data,
               'NFLXstock_data': NFLXstock_data,
               'GOOGstock_data': GOOGstock_data,
               'TSLAstock_data': TSLAstock_data,
               'MSFTstock_data': MSFTstock_data,
               'livecurrency_data': livecurrency_data,
               'commod': livecommodity_data,
               'news1_data': news1_data,
               'news2_data': news2_data,
               'news3_data': news3_data,
               'news4_data': news4_data,
               'news5_data': news5_data,
               'news6_data': news6_data,}
    return context

def get_currency():
    API_KEY = os.environ.get('CURRENCY_API_KEY')
    currencies = ['EUR', 'GBP', 'JPY', 'CAD','INR']
    request_url = f"https://openexchangerates.org/api/latest.json?app_id={API_KEY}&symbols={','.join(currencies)}"
    response = requests.get(request_url)
    data = response.json()
    rates = data['rates']
    currency.EUR=rates['EUR']
    currency.GBP=rates['GBP']
    currency.JPY=rates['JPY']
    currency.CAD=rates['CAD']
    currency.INR=rates['INR']