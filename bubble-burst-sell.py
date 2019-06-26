#!/usr/bin/env python
# bubble-burst-sell.py
# 
# Bubble Burst Crypto Seller
# Keith Irwin 2019
# 
# Sells crypto when the bubble bursts
# 

# This is the amount the price must drop to be considered a burst
BTC_BURST = 1000.0
# This is how much time the price has to drop that far
BTC_BURST_MINUTES = 60 * 24 * 3
# For example, a drop of $1000 in 3 days is considered a burst


# Imports
import json
from os import getenv
from time import sleep
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

# Get accounts
# (assuming only one account exists)
accounts = client.get_accounts()
for account in accounts.data:
	if account.currency == "USD":
		payout_method = account.id
		print("Loaded USD payout account, currently holding ${}".format(account.balance.amount))
	elif account.currency == "BTC":
		btc_account = account
		print("Loaded BTC account with {} BTC worth {} {}".format(
			account.balance.amount, 
			account.native_balance.amount, 
			account.native_balance.currency
		))
		break

# Get prices every minute
btc_prices = []
btc_max = 0.0
while True:
	sleep(60)
	
	# Get price
	btc_price = float(client.get_spot_price(currency_pair = 'BTC-USD').amount)
	print("Bitcoin currently trading at ${}".format(btc_price))
	btc_prices.append(btc_price)
	
	# Purge list
	if len(btc_prices) > BTC_BURST_MINUTES:
		btc_prices.pop(0)
	
	# Set max price
	if btc_price > btc_max:
		btc_max = btc_price
		print("New maximum BTC price: ${}!".format(btc_max))
	
	# Check for bubble burst
	if btc_price < btc_max - BTC_BURST:
		# SELL! 
		accounts.refresh()
		print("BURST!  Price dropped from ${} to ${}!  Selling all {} BTC now!".format(btc_max, btc_price, account.balance.amount))
		client.sell(
			btc_account.id, 
			total=btc_account.balance.amount,
			currency="BTC",
			payment_method=payout_method
		)
