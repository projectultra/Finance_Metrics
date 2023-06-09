import requests
import os
stocks_api_key=os.environ.get('STOCKS_API_KEY')
symbol = 'MSFT'
url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={stocks_api_key}'
response = requests.get(url)   
data = response.json() 
#loads data into stock object
print(int(data['Global Quote']['06. volume']))


symbol = 'TSLA'
url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={stocks_api_key}'
response = requests.get(url)   
data = response.json() 
#loads data into stock object
print(int(data['Global Quote']['06. volume']))

symbol = 'META'
url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={stocks_api_key}'
response = requests.get(url)   
data = response.json() 
#loads data into stock object
print(int(data['Global Quote']['06. volume']))

symbol = 'NFLX'
url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={stocks_api_key}'
response = requests.get(url)   
data = response.json() 
#loads data into stock object
print(int(data['Global Quote']['06. volume']))

symbol = 'GOOG'
url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={stocks_api_key}'
response = requests.get(url)   
data = response.json() 
#loads data into stock object
print(int(data['Global Quote']['06. volume']))