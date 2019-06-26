#!/usr/bin/env python
# bubble-burst-sell.py
# 
# Bubble Burst Crypto Seller
# Keith Irwin 2019
# 
# Sells crypto when the bubble bursts
# 


# Imports
import os, coinbase
from dotenv import load_dotenv


# Load API credentials from .env
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

