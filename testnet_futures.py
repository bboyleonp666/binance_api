#!/usr/bin/env python3

import os

from binance_api import BINANCE_CLIENT, BINANCE_REQUEST
from binance_api.utils import load_private_key, load_secret_key
from dotenv import load_dotenv

# Set up the default variables
load_dotenv()
FUTURES_API_KEY = os.getenv('FUTURES_API_KEY')
FUTURES_SECRET_KEY = os.getenv('FUTURES_SECRET_KEY')


def main():
    secret_key = load_secret_key(FUTURES_SECRET_KEY)
    client = BINANCE_CLIENT(api_key=FUTURES_API_KEY, secret_key=secret_key, futures=True, testnet=True)

    # Set up the request parameters
    data = {
        'symbol':      'BTCUSDT',
        # 'interval':     '1m',
        # 'side':         'BUY',
        # 'type':         'LIMIT',
        # 'timeInForce':  'GTC',
        # 'quantity':     '1.0000000',
        # 'price':        '8000',
        # 'recvWindow':   '5000',
    }

    # res = client.send(BINANCE_REQUEST.get_price, data=data)
    # res = client.send(BINANCE_REQUEST.get_open_orders, data=data)
    # res = client.send(BINANCE_REQUEST.get_account)    # /fapi/v1/account is no longer supported, use /fapi/v2/account instead
    # res = client.send(BINANCE_REQUEST.get_open_orders, data=data)
    # res = client.send(BINANCE_REQUEST.place_order, data=data)
    # res = client.send(BINANCE_REQUEST.get_exchange_info)
    res = client.send(BINANCE_REQUEST.get_historical_trades, data=data)
    # res = client.send(BINANCE_REQUEST.get_all_orders, data=data)
    # res = client.send(BINANCE_REQUEST.get_klines, data=data)

    # data = {
    #     'symbol': 'BTCUSDT',
    #     'orderId': 1222,
    # }
    # res = client.send(BINANCE_REQUEST.get_order, data=data)
    # res = client.send(BINANCE_REQUEST.delete_order, data=data)
    # res = client.send(BINANCE_REQUEST.get_average_price, data=data) # not supported by futures
    # res = client.send(BINANCE_REQUEST.get_agg_trades, data=data)
    # res = client.send(BINANCE_REQUEST.get_my_allocations, data=data)
    # res = client.send(BINANCE_REQUEST.get_all_order_list) # not supported by futures

    print('Status Code:', res.status_code)
    print(res.json())


if __name__ == '__main__':
    main()