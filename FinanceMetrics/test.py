import requests

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
    stock=[]
    symbol = 'IBM'  # Symbol for IBM
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={stocks_api_key}'
    response = requests.get(url)   
    data = response.json() 
    stock.append(data['Global Quote']['05. price'])
   
    
    symbol = 'IBM'  # Symbol for IBM
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={stocks_api_key}'
    response = requests.get(url)   
    data = response.json() 
    stock.append(data['Global Quote']['05. price'])
    
    
    symbol = 'IBM'  # Symbol for IBM
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={stocks_api_key}'
    response = requests.get(url)   
    data = response.json() 
    stock.append(data['Global Quote']['05. price'])
    
    symbol = 'IBM'  # Symbol for IBM
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={stocks_api_key}'
    response = requests.get(url)   
    data = response.json() 
    stock.append(data['Global Quote']['05. price'])
      
    symbol = 'IBM'  # Symbol for IBM
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={stocks_api_key}'
    response = requests.get(url)   
    data = response.json() 
    stock.append(data['Global Quote']['05. price'])
    print(stock)

def get_commodities():
	commodity=[]
	comm = 'COFFEE'
	url = f'https://www.alphavantage.co/query?function={comm}&apikey={com_api_key}&interval=monthly'
	response = requests.get(url)
	data = response.json()
	commodity.append(data['data'][0]['value'])
	
	comm = 'NATURAL_GAS'
	url = f'https://www.alphavantage.co/query?function={comm}&apikey={com_api_key}&interval=monthly'
	response = requests.get(url)
	data = response.json()
	commodity.append(data['data'][0]['value'])
	
	comm = 'ALUMINUM'
	url = f'https://www.alphavantage.co/query?function={comm}&apikey={com_api_key}&interval=monthly'
	response = requests.get(url)
	data = response.json()
	commodity.append(data['data'][0]['value'])
	
	comm = 'BRENT' #(oil)
	url = f'https://www.alphavantage.co/query?function={comm}&apikey={com_api_key}&interval=monthly'
	response = requests.get(url)
	data = response.json()
	commodity.append(data['data'][0]['value'])
	
	comm = 'SUGAR'
	url = f'https://www.alphavantage.co/query?function={comm}&apikey={com_api_key}&interval=monthly'
	response = requests.get(url)
	data = response.json()
	commodity.append(data['data'][0]['value'])
	
	print(commodity)
get_news()
get_commodities()
get_stocks()
