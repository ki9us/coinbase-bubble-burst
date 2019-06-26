# Coinbase Bubble Burster Seller
###### Keith Irwin 2019

A script to sell crypto assets when the bubble bursts.  

I take no responsibility for how you use this script.  I'm not even sure that it works.  

## Installation

Create environment and install dependencies

```
git clone https://github.com/keith24/coinbase-bubble-burst.git
cd coinbase-bubble-burst
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
cp .env-sample .env
```

The edit `.env` with your account's API data from [www.coinbase.com/settings/api](https://www.coinbase.com/settings/api).  

## Usage

Edit `BTC_BURST_AMOUNT` and `BTC_BURST_MINUTES` in `main.py`.  The script will sell all your BTC when the price drops an amount of `BTC_BURST_AMOUNT` within `BTC_BURST_MINUTES`.  

Then simply run `./main.py`.  It will run until the bubble bursts, then sell all your assets and quit.  
