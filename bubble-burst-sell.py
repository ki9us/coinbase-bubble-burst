#!/usr/bin/env python
# bubble-burst-sell.py
# 
# Bubble Burst Crypto Seller
# Keith Irwin 2019
# 
# Sells crypto when the bubble bursts
# 


# Imports
import json
from os import getenv
from dotenv import load_dotenv
from coinbase.wallet.client import Client

# Load API credentials
load_dotenv()
API_KEY = getenv("API_KEY")
API_SECRET = getenv("API_SECRET")

# Authenticate with Coinbase
client = Client(API_KEY, API_SECRET)
user = client.get_current_user()
print("Logged into Coinbase as {}".format(user.name))
