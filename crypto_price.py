import requests
from dotenv import load_dotenv
import os

load_dotenv()

COINMARKETCAP_TOKEN = os.getenv('COINMARKETCAP_TOKEN')


def get_crypto_price(crypto_symbol):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    params = {
        'symbol': crypto_symbol,
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': COINMARKETCAP_TOKEN,
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if response.status_code == 200:
        return data['data'][crypto_symbol]['quote']['USD']['price']
    else:
        print(f"Ошибка при получении данных: {data}")
        return None
    