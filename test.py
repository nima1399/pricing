import requests

btc_usdt = requests.get('https://api.nobitex.ir/v2/orderbook/BTCUSDT')
btc_usdt = btc_usdt
print(btc_usdt.json()["lastTradePrice"])