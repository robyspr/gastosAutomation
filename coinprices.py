import requests

from dotenv import dotenv_values

config = dotenv_values()

def getData(item):
    # return item['id'], item['current_price']
    return item['current_price']

def getCoinsData():

  url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin,ethereum,dogecoin,shiba-inu&precision=9"

  payload = {}
  headers = {
    'x_cg_demo_api_key': config.get('X_CG_DEMO_API_KEY')
  }

  response = requests.request("GET", url, headers=headers, data=payload)
  data = response.json()

  # bitcoin, ethereum, doge, shiba  = [getData(x) for x in data]
  return [[getData(x)] for x in data]
