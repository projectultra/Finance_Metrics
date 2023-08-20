import json
import datetime
import os
import keras
import pandas as pd
import numpy as np
import requests
import yfinance as yf
import django
from pymongo import MongoClient
from django.shortcuts import render
from FinanceMetrics.models import EconomicIndicators,commodities,currency
from FinanceMetrics.models import METAstock,AAPLstock,AMZNstock,NFLXstock,GOOGstock,MSFTstock,TSLAstock
from FinanceMetrics.models import news1,news2,news3,news4,news5,news6

client=MongoClient('localhost', 27017)
db = client['FinanceMetrics']

DBDate = pd.DataFrame(list(db['Date'].find()))
DBDate = DBDate.drop(columns=['_id'])

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FM.settings')
django.setup()
# Create your views here.

prevdate = DBDate['Date'][0]
def DisplayStock(request):
    tdapi_key=os.environ.get('TWELVEDATAAPI_KEY')
    if((datetime.datetime.date(datetime.datetime.today()))!=(pd.to_datetime(prevdate).dt.date[0])):
        FetchEconomicIndicators() #Fetches Economic Indicators
        Fetchstock(tdapi_key) #Fetches Stock Prices for Neural Network Model for prediction
        get_news() #Fetches News
        get_currency() #Fetches Currency
        get_stocks() #Fetches live Stock Prices
        get_commodities() #Fetches Commodities
        storeprices(datetime.datetime.today()) #Stores Prices in CSV as cache
    else:
        fetchprices() #Fetches Prices from CSV
    context=compiledata() #Compiles Data for Display
    return render(request,'FinanceMetrics/Templates/index.html',context)

def Fetchstock(tdapi_key):
    model=keras.models.load_model(r'Stock Data/models') #Loads Neural Network Model
    url='https://api.twelvedata.com/time_series?symbol=META&interval=1day&outputsize=14&format=CSV&apikey='+tdapi_key
    response = requests.get(url,timeout=10)

    #Predicts Prices for next day
    METAstock.predicted_price=model.predict(conversion(response).reshape(1,14,9))
    url='https://api.twelvedata.com/time_series?symbol=AAPL&interval=1day&outputsize=14&format=CSV&apikey='+tdapi_key
    response = requests.get(url,timeout=10)
    AAPLstock.predicted_price=model.predict(conversion(response).reshape(1,14,9))
    url='https://api.twelvedata.com/time_series?symbol=AMZN&interval=1day&outputsize=14&format=CSV&apikey='+tdapi_key
    response = requests.get(url,timeout=10)
    AMZNstock.predicted_price=model.predict(conversion(response).reshape(1,14,9))
    url='https://api.twelvedata.com/time_series?symbol=NFLX&interval=1day&outputsize=14&format=CSV&apikey='+tdapi_key
    response = requests.get(url,timeout=10)
    NFLXstock.predicted_price=model.predict(conversion(response).reshape(1,14,9))
    url='https://api.twelvedata.com/time_series?symbol=GOOG&interval=1day&outputsize=14&format=CSV&apikey='+tdapi_key
    response = requests.get(url,timeout=10)
    GOOGstock.predicted_price=model.predict(conversion(response).reshape(1,14,9))
    url='https://api.twelvedata.com/time_series?symbol=MSFT&interval=1day&outputsize=14&format=CSV&apikey='+tdapi_key
    response = requests.get(url,timeout=10)
    MSFTstock.predicted_price=model.predict(conversion(response).reshape(1,14,9))
    url='https://api.twelvedata.com/time_series?symbol=TSLA&interval=1day&outputsize=14&format=CSV&apikey='+tdapi_key
    response = requests.get(url,timeout=10)
    TSLAstock.predicted_price=model.predict(conversion(response).reshape(1,14,9))

def FetchEconomicIndicators():
    api_key=os.environ.get('API_KEY')
    country = 'United States'

    url = 'https://api.api-ninjas.com/v1/inflation?country={}'.format(country)
    r = requests.get(url,timeout=10, headers={'X-Api-Key': os.environ.get('NINJAAPI_KEY')})
    EconomicIndicators.inflation = json.loads(r.text)[0]['yearly_rate_pct']

    url = 'https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE&interval=daily&datatype=csv&apikey='+api_key
    r = requests.get(url,timeout=10)
    lines = r.text.strip().split('\n')
    EconomicIndicators.interest_rate = lines[1].split(',')[1]

    url = 'https://api.api-ninjas.com/v1/convertcurrency?want=GBP&have=USD&amount=1'
    r = requests.get(url,timeout=10, headers={'X-Api-Key': os.environ.get('NINJAAPI_KEY')})
    EconomicIndicators.currency = json.loads(r.text)['new_amount']

def storeprices(lastdate):
    
    db['Stocks'].insert_many([
        {   'Stocks':'AAPL',
            'Predicted':float(AAPLstock.predicted_price),
            'Live':AAPLstock.live_price,
            'Open':AAPLstock.open_price,
            'High':AAPLstock.high_price,
            'Low':AAPLstock.low_price,
            'Volume':int(AAPLstock.volume),
            'Change':AAPLstock.price_change,
            'Previous':AAPLstock.previous_close,},
        {   'Stocks':'AMZN',
            'Predicted':float(AMZNstock.predicted_price),
            'Live':AMZNstock.live_price,
            'Open':AMZNstock.open_price,
            'High':AMZNstock.high_price,
            'Low':AMZNstock.low_price,
            'Volume':int(AMZNstock.volume),
            'Change':AMZNstock.price_change,
            'Previous':AMZNstock.previous_close,},
        {   'Stocks':'GOOG',
            'Predicted':float(GOOGstock.predicted_price),
            'Live':GOOGstock.live_price,
            'Open':GOOGstock.open_price,
            'High':GOOGstock.high_price,
            'Low':GOOGstock.low_price,
            'Volume':int(GOOGstock.volume),
            'Change':GOOGstock.price_change,
            'Previous':GOOGstock.previous_close,},
        {
            'Stocks':'MSFT',
            'Predicted':float(MSFTstock.predicted_price),
            'Live':MSFTstock.live_price,
            'Open':MSFTstock.open_price,
            'High':MSFTstock.high_price,
            'Low':MSFTstock.low_price,
            'Volume':int(MSFTstock.volume),
            'Change':MSFTstock.price_change,
            'Previous':MSFTstock.previous_close,},
        {
            'Stocks':'NFLX',
            'Predicted':float(NFLXstock.predicted_price),
            'Live':NFLXstock.live_price,
            'Open':NFLXstock.open_price,
            'High':NFLXstock.high_price,
            'Low':NFLXstock.low_price,
            'Volume':int(NFLXstock.volume),
            'Change':NFLXstock.price_change,
            'Previous':NFLXstock.previous_close,},
        {
            'Stocks':'TSLA',
            'Predicted':float(TSLAstock.predicted_price),
            'Live':TSLAstock.live_price,
            'Open':TSLAstock.open_price,
            'High':TSLAstock.high_price,
            'Low':TSLAstock.low_price,
            'Volume':int(TSLAstock.volume),
            'Change':TSLAstock.price_change,
            'Previous':TSLAstock.previous_close,}])
    
    #Creates Dataframe for storing Prices
    #Creates Dataframe for storing News
    db['News'].insert_many([
        {
            'News': 'News1',
            'Headline': news1.title,
            'Link': news1.url,
            'Author': news1.author,
            'Description': news1.summary,
            'Image': news1.urlToImage,
            'Source': news1.source,},
        {
            'News': 'News2',
            'Headline': news2.title,
            'Link': news2.url,
            'Author': news2.author,
            'Description': news2.summary,
            'Image': news2.urlToImage,
            'Source': news2.source,},
        {
            'News': 'News3',
            'Headline': news3.title,
            'Link': news3.url,
            'Author': news3.author,
            'Description': news3.summary,
            'Image': news3.urlToImage,
            'Source': news3.source,},
        {
            'News': 'News4',
            'Headline': news4.title,
            'Link': news4.url,
            'Author': news4.author,
            'Description': news4.summary,
            'Image': news4.urlToImage,
            'Source': news4.source,},
        {
            'News': 'News5',
            'Headline': news5.title,
            'Link': news5.url,
            'Author': news5.author,
            'Description': news5.summary,
            'Image': news5.urlToImage,
            'Source': news5.source,}
    ])

    db['Commodities'].insert_many([
        {
            'Oil': commodities.oil,
            'Gold': commodities.gold,
            'Silver': commodities.silver,
            'aluminium': commodities.aluminium,
            'Petrol': commodities.petrol,
        }
    ])
    #Creates Dataframe for storing Commodities      
    db['Currency'].insert_many([
        {
            'EUR': currency.EUR,
            'GBP': currency.GBP,
            'JPY': currency.JPY,
            'CAD': currency.CAD,
            'INR': currency.INR,
        }
    ])
    
    db['Date'].insert_one([{ 'Date': datetime.datetime.now()}])
    #Combines all Dataframes into one
    # PredStock = pd.concat([PredictedStock , NewsData, curr_commod,date],axis=1)
    
    # #output statments for logging/debugging
    # print(PredictedStock['AAPL'],PredictedStock['AMZN'],PredictedStock['GOOG'],PredictedStock['META'],PredictedStock['MSFT'],PredictedStock['NFLX'],PredictedStock['TSLA'])
    # print(NewsData['News1'],NewsData['News2'],NewsData['News3'],NewsData['News4'],NewsData['News5'],NewsData['News6'])
    # print(curr_commod)
    # print(date)
    

def fetchprices():
    #Fetches Dataframe from CSV
    Stockdata = pd.DataFrame(list(db['Stocks'].find()))
    Stockdata = Stockdata.drop(columns=['_id'])

    Currencydata = pd.DataFrame(list(db['Currency'].find()))
    Currencydata = Currencydata.drop(columns=['_id'])

    Commoditiesdata = pd.DataFrame(list(db['Commodities'].find()))
    Commoditiesdata = Commoditiesdata.drop(columns=['_id'])

    Newsdata = pd.DataFrame(list(db['News'].find()))
    Newsdata = Newsdata.drop(columns=['_id'])
    #Assigns Dataframe values to Stock Objects
    AAPLstock.predicted_price = Stockdata['Predicted'][0]
    AAPLstock.live_price = Stockdata['Live'][0]
    AAPLstock.open_price = Stockdata['Open'][0]
    AAPLstock.high_price = Stockdata['High'][0]
    AAPLstock.low_price = Stockdata['Low'][0]
    AAPLstock.volume = Stockdata['Volume'][0]
    AAPLstock.price_change = Stockdata['Price Change'][0]
    AAPLstock.previous_close = Stockdata['Previous Close'][0]

    AMZNstock.predicted_price = Stockdata['Predicted'][1]
    AMZNstock.live_price = Stockdata['Live'][1]
    AMZNstock.open_price = Stockdata['Open'][1]
    AMZNstock.high_price = Stockdata['High'][1]
    AMZNstock.low_price = Stockdata['Low'][1]
    AMZNstock.volume = Stockdata['Volume'][1]
    AMZNstock.price_change = Stockdata['Price Change'][1]
    AMZNstock.previous_close = Stockdata['Previous Close'][1]

    GOOGstock.predicted_price = Stockdata['Predicted'][2]
    GOOGstock.live_price = Stockdata['Live'][2]
    GOOGstock.open_price = Stockdata['Open'][2]
    GOOGstock.high_price = Stockdata['High'][2]
    GOOGstock.low_price = Stockdata['Low'][2]
    GOOGstock.volume = Stockdata['Volume'][2]
    GOOGstock.price_change = Stockdata['Price Change'][2]
    GOOGstock.previous_close = Stockdata['Previous Close'][2]

    METAstock.predicted_price = Stockdata['Predicted'][3]
    METAstock.live_price = Stockdata['Live'][3]
    METAstock.open_price = Stockdata['Open'][3]
    METAstock.high_price = Stockdata['High'][3]
    METAstock.low_price = Stockdata['Low'][3]
    METAstock.volume = Stockdata['Volume'][3]
    METAstock.price_change = Stockdata['Price Change'][3]
    METAstock.previous_close = Stockdata['Previous Close'][3]

    MSFTstock.predicted_price = Stockdata['Predicted'][4]
    MSFTstock.live_price = Stockdata['Live'][4]
    MSFTstock.open_price = Stockdata['Open'][4]
    MSFTstock.high_price = Stockdata['High'][4]
    MSFTstock.low_price = Stockdata['Low'][4]
    MSFTstock.volume = Stockdata['Volume'][4]
    MSFTstock.price_change = Stockdata['Price Change'][4]
    MSFTstock.previous_close = Stockdata['Previous Close'][4]
    
    NFLXstock.predicted_price = Stockdata['Predicted'][5]
    NFLXstock.live_price = Stockdata['Live'][5]
    NFLXstock.open_price = Stockdata['Open'][5]
    NFLXstock.high_price = Stockdata['High'][5]
    NFLXstock.low_price = Stockdata['Low'][5]
    NFLXstock.volume = Stockdata['Volume'][5]
    NFLXstock.price_change = Stockdata['Price Change'][5]
    NFLXstock.previous_close = Stockdata['Previous Close'][5]
    
    TSLAstock.predicted_price = Stockdata['Predicted'][6]
    TSLAstock.live_price = Stockdata['Live'][6]
    TSLAstock.open_price = Stockdata['Open'][6]
    TSLAstock.high_price = Stockdata['High'][6]
    TSLAstock.low_price = Stockdata['Low'][6]
    TSLAstock.volume = Stockdata['Volume'][6]
    TSLAstock.price_change = Stockdata['Price Change'][6]
    TSLAstock.previous_close = Stockdata['Previous Close'][6]
    
    #Assigns Dataframe values to News Objects
    news1.title=Newsdata['Headline'][0]
    news1.url=Newsdata['Link'][0]
    news1.author=Newsdata['Author'][0]
    news1.summary=Newsdata['Description'][0]
    news1.urlToImage=Newsdata['Image'][0]
    news1.source=Newsdata['Source'][0]
    
    news2.title=Newsdata['Headline'][1]
    news2.url=Newsdata['Link'][1]
    news2.author=Newsdata['Author'][1]
    news2.summary=Newsdata['Description'][1]
    news2.urlToImage=Newsdata['Image'][1]
    news2.source=Newsdata['Source'][1]
    
    news3.title=Newsdata['Headline'][2]
    news3.url=Newsdata['Link'][2]
    news3.author=Newsdata['Author'][2]
    news3.summary=Newsdata['Description'][2]
    news3.urlToImage=Newsdata['Image'][2]
    news3.source=Newsdata['Source'][2]
    
    news4.title=Newsdata['Headline'][3]
    news4.url=Newsdata['Link'][3]
    news4.author=Newsdata['Author'][3]
    news4.summary=Newsdata['Description'][3]
    news4.urlToImage=Newsdata['Image'][3]
    news4.source=Newsdata['Source'][3]
    
    news5.title=Newsdata['Headline'][4]
    news5.url=Newsdata['Link'][4]
    news5.author=Newsdata['Author'][4]
    news5.summary=Newsdata['Description'][4]
    news5.urlToImage=Newsdata['Image'][4]
    news5.source=Newsdata['Source'][4]
    
    news6.title=Newsdata['Headline'][5]
    news6.url=Newsdata['Link'][5]
    news6.author=Newsdata['Author'][5]
    news6.summary=Newsdata['Description'][5]
    news6.urlToImage=Newsdata['Image'][5]
    news6.source=Newsdata['Source'][5]
    

    #Assigns Dataframe values to Currency Objects
    currency.EUR= Currencydata['EUR']
    currency.GBP= Currencydata['GBP']
    currency.JPY= Currencydata['JPY']
    currency.CAD= Currencydata['CAD']
    currency.INR= Currencydata['INR']
    
    #Assigns Dataframe values to Commodity Objects
    commodities.oil=Commoditiesdata['Oil']
    commodities.gold=Commoditiesdata['Gold']
    commodities.silver=Commoditiesdata['Silver']
    commodities.aluminium=Commoditiesdata['Aluminium']
    commodities.petrol=Commoditiesdata['Petrol']
    
    #output statments for logging/debugging
    print("Cached Data Loaded")
    
#converts the response from the API to feed into neural network
def conversion(response):
    #splits response into lines
    lines = response.text.split("\n")[1:-1]
    data_rows = []
    #Creates sliding window of 14 days
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
    #returns 14x9 dataframe for input to neural network
    return(np.array(data_rows))


def get_stocks():
    stocks_api_key=os.environ.get('STOCKS_API_KEY')
    stocks2_api_key=os.environ.get('STOCKS2_API_KEY')
    symbol = 'AAPL'
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={stocks_api_key}'
    response = requests.get(url,timeout=10)   
    data = response.json() 
    #loads data into stock object
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
    response = requests.get(url,timeout=10)   
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
    #loads data into commodities object
    commodity_ticker = yf.Ticker("GC=F")
    commodities.gold = commodity_ticker.history(period="5d")["Close"].iloc[-1]
    
    commodity_ticker = yf.Ticker("SI=F")
    commodities.silver = commodity_ticker.history(period="5d")["Close"].iloc[-1]
    
    commodity_ticker = yf.Ticker("ALI=F")
    commodities.aluminium = commodity_ticker.history(period="5d")["Close"].iloc[-1]
    
    commodity_ticker = yf.Ticker("CL=F")
    commodities.oil = commodity_ticker.history(period="5d")["Close"].iloc[-1]
    
    commodity_ticker = yf.Ticker("RB=F")
    commodities.petrol = commodity_ticker.history(period="5d")["Close"].iloc[-1]

def get_news():
    #loads data into news object
    news_api_key=os.environ.get('NEWS_API_KEY')
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&apikey={news_api_key}&topics=finance'
    response = requests.get(url,timeout=10)
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

def compiledata():
    #compiles data into a dictionary
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
    'ALUMINIUM':round(commodities.aluminium,2)}
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
    
    #creates a dictionary of all the data to be passed to the html page
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
