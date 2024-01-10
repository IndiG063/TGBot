import requests
import json
from config import API_KEY

class APIException(Exception):
    def __init__(self, message):
        self.message = message

class CurrencyConverter:
    @staticmethod
    def get_price(base, quote, amount):
        url = f'https://api.exchangerate-api.com/v4/latest/{base}?apiKey={API_KEY}'
        response = requests.get(url)
        data = json.loads(response.text)

        if 'error' in data:
            raise APIException(f"Ошибка при получении данных: {data['error']['info']}")

        base_rate = data['rates'][quote]
        result = round(amount * base_rate, 2)
        return result
