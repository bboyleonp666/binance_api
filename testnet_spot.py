#!/usr/bin/env python3

import os
# import time
# import base64
# import requests

from binance_variables import *
from binance_functions import load_private_key, BINANCE_CLIENT, BINANCE_REQUEST
from dotenv import load_dotenv

# Set up the default variables
load_dotenv()
API_KEY = os.getenv('API_KEY')
PRIVATE_KEY_PATH = os.getenv('PRIVATE_KEY_PATH')

import cryptography

type_private_key = cryptography.hazmat.bindings._rust.openssl.ed25519.Ed25519PrivateKey

def main():
    private_key = load_private_key(PRIVATE_KEY_PATH)
    client = BINANCE_CLIENT(api_key=API_KEY, private_key=private_key, futures=False, testnet=True)

    # Set up the request parameters
    data = {
        'symbol':       'BTCUSDT',
        # 'interval':     '1m',
        'side':         'BUY',
        'type':         'LIMIT',
        'timeInForce':  'GTC',
        'quantity':     '1.0000000',
        'price':        '8000',
        'recvWindow':   '5000',
    }

    res = client.send(BINANCE_REQUEST.get_price, data=data)
    # res = client.send(BINANCE_REQUEST.get_open_orders, data=data)
    # res = client.send(BINANCE_REQUEST.get_account)
    # res = client.send(BINANCE_REQUEST.get_open_orders, data=data)
    # res = client.send(BINANCE_REQUEST.place_order, data=data)
    # res = client.send(BINANCE_REQUEST.get_exchange_info)
    # res = client.send(BINANCE_REQUEST.get_historical_trades, data=data)
    # res = client.send(BINANCE_REQUEST.get_all_orders, data=data)
    # res = client.send(BINANCE_REQUEST.get_klines, data=data)

    # data = {
    #     'symbol': 'BTCUSDT',
    #     'orderId': 1222,
    # }
    # res = client.send(BINANCE_REQUEST.get_order, data=data)
    # res = client.send(BINANCE_REQUEST.delete_order, data=data)
    # res = client.send(BINANCE_REQUEST.get_average_price, data=data)
    # res = client.send(BINANCE_REQUEST.get_agg_trades, data=data)
    # res = client.send(BINANCE_REQUEST.get_my_allocations, data=data)
    # res = client.send(BINANCE_REQUEST.get_all_order_list)

    print('Status Code:', res.status_code)
    print(res.json())


    # res = client.send(BINANCE_REQUEST.get_average_price, data=data)
    # print('Status Code:', res.status_code)
    # print(res.json())

    
    # res = client.send(BINANCE_REQUEST.get_exchange_info)
    # for symbol_info in res.json()['symbols']:
    #     if symbol_info['symbol'] == 'BTCUSDT':
    #         for filter in symbol_info['filters']:
    #             if filter['filterType'] == 'PERCENT_PRICE_BY_SIDE':
    #                 print(filter)
    #                 break
    #             # print(filter)
    

if __name__ == '__main__':
    main()