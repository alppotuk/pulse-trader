import os
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi

load_dotenv("config/.env")

API_KEY = os.getenv("ALPACA_API_KEY")
API_SECRET = os.getenv("ALPACA_API_SECRET")
BASE_URL = os.getenv("ALPACA_API_ENDPOINT")

api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

account = api.get_account()
print(f"Account status: {account.status}, Cash available: {account.cash}")
