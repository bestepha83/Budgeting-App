import requests

headers = {
    'Contents-Type': 'application/json',
    'Authorization': 'Token 2c31226d73aa45ed9be6d931d20f0e274de6972e'
}

def get_meta_data(ticker):
    url = "https://api.tiingo.com/tiingo/daily/{}".format(ticker)
    response = requests.get(url, headers=headers)
    return response.json()

def get_price_data(ticker):
    url = "https://api.tiingo.com/tiingo/daily/{}/prices".format(ticker)
    response = requests.get(url, headers=headers)
    return response.json()[0]