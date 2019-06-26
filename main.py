#!/usr/bin/env python
# main.py
# 
# Bubble Burst Crypto Seller
# Keith Irwin 2019
# 
# Sells crypto when the bubble bursts


# Imports
import json
from os import getenv
from time import sleep
from dotenv import load_dotenv
from coinbase.wallet.client import Client

# Load environment constants
load_dotenv()
API_KEY = getenv("API_KEY")
API_SECRET = getenv("API_SECRET")
BTC_BURST_AMOUNT = float(getenv("BTC_BURST_AMOUNT"))
BTC_BURST_MINUTES = float(getenv("BTC_BURST_MINUTES"))

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
		print("Loaded USD payout account, currently holding ${}".format(
			account.balance.amount
		))
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
	# Repeat every 30 seconds (coinbase price update time)
	sleep(30)
	# Refresh holdings
	btc_account.refresh()
	
	# For debugging
	#print("btc_prices:",btc_prices)
	#print("btc_max:",btc_max)

	# Get price
	btc_price = float(client.get_spot_price(currency_pair = 'BTC-USD').amount)
	print("Bitcoin currently trading at ${}".format(btc_price))
	btc_prices.append(btc_price)
	
	# Purge list
	if len(btc_prices) > BTC_BURST_MINUTES * 2:
		btc_prices.pop(0)
	
	# Set max price
	btc_new_max = max(btc_prices)
	if btc_new_max > btc_max:
		btc_max = btc_new_max
		print("New maximum BTC price: ${}!".format(btc_max))
	
	# Check for bubble burst
	if btc_price < btc_max - BTC_BURST_AMOUNT:
		# SELL! 
		print("BURST!  Price dropped from ${} to ${}!  Selling all {} BTC now!".format(
			btc_max, btc_price, account.balance.amount
		))
		client.sell(
			btc_account.id, 
			total=btc_account.balance.amount,
			currency="BTC",
			payment_method=payout_method
		)
		break
	else: 
		print("Hodling {} BTC worth ${}...".format(
			account.balance.amount, account.native_balance.amount
		))
