import requests
import yfinance as yf
news_api_key = '5CHD55L89CLKRMBT'
stocks_api_key = 'PLS4G5EWBHRPJGN5'
com_api_key = 'TWKRAM873PSNZYPV'


def get_news():
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&apikey={news_api_key}&topics=finance'
    response = requests.get(url)
    data=response.json()
    NEWS=[]
    #data = json.loads(n)
    for feed_item in data['feed']:
        title = feed_item['title']
        url = feed_item['url']
        authors = feed_item['authors']
        summary = feed_item['summary']
        banner_image = feed_item['banner_image']
        source = feed_item['source']
		    
	    # Append the extracted fields as a new list to the feed_data list
        NEWS.append([title, url, authors, summary, banner_image, source])
    print(NEWS)

def get_stocks():
    stocks=[]
    stock=yf.Ticker("MSFT")
    data=stock.history(period="1d")
    y=data["Close"]
    for close in y:
        stocks.append(close)
        print("Microsoft:",close)
    stock=yf.Ticker("AAPL")
    data=stock.history(period="1d")
    y=data["Close"]
    for close in y:
        stocks.append(close)
        print("Apple:",close)
    stock=yf.Ticker("TSLA")
    data=stock.history(period="1d")
    y=data["Close"]
    for close in y:
        stocks.append(close)
        print("Tesla:",close)
    stock=yf.Ticker("AMZN")
    data=stock.history(period="1d")
    y=data["Close"]
    for close in y:
        stocks.append(close)
        print("Amazon:",close)
    stock=yf.Ticker("GOOG")
    data=stock.history(period="1d")
    y=data["Close"]
    for close in y:
        stocks.append(close)
        print("Google:",close)


def get_commodities():
	commodity=[]
	comm = 'COFFEE'
	url = f'https://www.alphavantage.co/query?function={comm}&apikey={news_api_key}&interval=monthly'
	response = requests.get(url)
	data = response.json()
	commodity.append(data['data'][0]['value'])
	
	comm = 'NATURAL_GAS'
	url = f'https://www.alphavantage.co/query?function={comm}&apikey={news_api_key}&interval=monthly'
	response = requests.get(url)
	data = response.json()
	commodity.append(data['data'][0]['value'])
	
	
	comm = 'BRENT' #(oil)
	url = f'https://www.alphavantage.co/query?function={comm}&apikey={stocks_api_key}&interval=monthly'
	response = requests.get(url)
	data = response.json()
	commodity.append(data['data'][0]['value'])
	
	comm = 'SUGAR'
	url = f'https://www.alphavantage.co/query?function={comm}&apikey={com_api_key}&interval=monthly'
	response = requests.get(url)
	data = response.json()
	commodity.append(data['data'][0]['value'])
	
	print(commodity)

def get_currency():
    # Replace 'YOUR_API_KEY' with your actual API key from OpenExchangeRates
    currency=[]
    API_KEY = '940623d4fbfc46a9a69116069ef4cc7d'
    BASE_URL = 'https://openexchangerates.org/api/latest.json'
    currencies = ['USD', 'EUR', 'GBP', 'JPY', 'CAD']
    request_url = f"{BASE_URL}?app_id={API_KEY}&symbols={','.join(currencies)}"
    response = requests.get(request_url)
    data = response.json()
    rates = data['rates']
    for c in currencies:
        currency.append(rates[c])
        print(f"1 {data['base']} = {rates[c]} {c}")


get_news()
get_commodities()
get_stocks()
get_currency()