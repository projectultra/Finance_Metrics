from pymongo import MongoClient
import pandas as pd
import numpy as np

client = MongoClient('localhost', 27017)
db = client['FinanceMetrics']

Stockdata = pd.DataFrame(list(db['Stocks'].find()))
Stockdata = Stockdata.drop(columns=['_id'])

Currencydata = pd.DataFrame(list(db['Currency'].find()))
Currencydata = Currencydata.drop(columns=['_id'])

Commoditiesdata = pd.DataFrame(list(db['Commodities'].find()))
Commoditiesdata = Commoditiesdata.drop(columns=['_id'])

Newsdata = pd.DataFrame(list(db['News'].find()))
Newsdata = Newsdata.drop(columns=['_id'])

print(Stockdata,Stockdata['Live'][0])
# print(Currencydata)
# print(Commoditiesdata)
# print(Newsdata)
