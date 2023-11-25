#!/usr/bin/env python3
import time
import base64
import requests

import hmac
import hashlib
import cryptography

from binance_api.variables import *


from cryptography.hazmat.bindings._rust import openssl
TYPE_PRIVATE_KEY = openssl.ed25519.Ed25519PrivateKey
TYPE_SECRET_KEY = bytes


class BINANCE_CLIENT(object):
    def __init__(self, 
                 api_key: str, 
                 secret_key: TYPE_SECRET_KEY = None, 
                 private_key: TYPE_PRIVATE_KEY = None, 
                 futures: bool = True, 
                 testnet: bool = True):

        assert secret_key is not None or private_key is not None, 'Either "secret_key" or "private_key" should be provided!'

        if futures:
            url = (TESTNET_FUTURE_URL if testnet else FUTURE_URL) + API_FUTURE_PREFIX
        else:
            url = (TESTNET_SPOT_URL if testnet else SPOT_URL) + API_SPOT_PREFIX
        
        self._url = url
        self._api_key = api_key
        self._secret_key = secret_key
        self._private_key = private_key
        self._headers = {'X-MBX-APIKEY': self._api_key}


    def send(self, func, data={}):
        """
        Send the request to Binance API
        ---
        :param func: Binance API to call
        :param data: request parameters (only needed when placing an order)
        :param kwargs: other parameters
        ---
        :return: response from Binance API
        """
        data['timestamp'] = self._get_timestamp()
        data['signature'] = self._get_signature(data)

        print('Request:')
        print('  Method: ', func.__name__)
        print('  URL:    ', self._url)
        print('  Headers:', self._headers)
        print()

        response = func(url=self._url, headers=self._headers, data=data)
        return response
    
    def _get_signature(self, args):
        """
        sign the request with secret key or private key
        if both are provided, private key has higher priority
        """
        payload = '&'.join([f'{param}={value}' for param, value in args.items()])

        if self._private_key is not None:
            signature = base64.b64encode(self._private_key.sign(payload.encode('ASCII')))

        else:
            signature = hmac.new(self._secret_key, msg=bytes(payload, 'latin-1'), digestmod=hashlib.sha256).hexdigest()

        return signature

    def _get_timestamp(self):
        """UNIX timestamp in milliseconds"""
        return int(time.time() * 1000)
    

class BINANCE_REQUEST(object):
    def __init__():
        pass

    @staticmethod
    def get_price(url, headers, data):
        api_call = API_GET_PRICE
        if 'symbol' in data:
            api_call += f'?symbol={data["symbol"]}'

        response = requests.get(
            url=url + api_call,
            headers=headers,
        )
        return response
    
    @staticmethod
    def get_open_orders(url, headers, data):
        api_call = API_GET_OPEN_ORDERS

        response = requests.get(
            url=url + api_call,
            headers=headers,
            params=data,
        )
        return response
    
    @staticmethod
    def get_account(url, headers, data):
        if '/fapi/v1' in url:
            # GET /fapi/v1/account is retired, use GET /fapi/v2/account instead
            url = url.replace('/fapi/v1', '/fapi/v2')
        
        api_call = API_GET_ACCOUNT

        response = requests.get(
            url=url + api_call,
            headers=headers,
            params=data,
        )
        return response
    
    @staticmethod
    def place_order(url, headers, data):
        api_call = API_PLACE_ORDER

        response = requests.post(
            url=url + api_call,
            headers=headers,
            params=data,
        )
        return response
    
    @staticmethod
    def get_exchange_info(url, headers, data):
        api_call = API_GET_EXCHANGE_INFO

        response = requests.get(
            url=url + api_call,
            headers=headers,
        )
        return response
    
    @staticmethod
    def get_historical_trades(url, headers, data):
        api_call = API_GET_HISTORICAL_TRADES
        data = {'symbol': data['symbol']}
        
        response = requests.get(
            url=url + api_call,
            headers=headers,
            params=data,
        )
        return response
    
    @staticmethod
    def get_all_orders(url, headers, data):
        api_call = API_GET_ALL_ORDERS
        
        response = requests.get(
            url=url + api_call,
            headers=headers,
            params=data,
        )
        return response
    
    @staticmethod
    def get_klines(url, headers, data):
        api_call = API_GET_KLINES
        data = {
            'symbol': data["symbol"], 
            'interval': data["interval"]
        }
        
        response = requests.get(
            url=url + api_call,
            headers=headers,
            params=data,
        )
        return response
    
    @staticmethod
    def get_order(url, headers, data):
        api_call = API_GET_ORDER
        
        response = requests.get(
            url=url + api_call,
            headers=headers,
            params=data,
        )
        return response
    
    @staticmethod
    def delete_order(url, headers, data):
        api_call = API_DELETE_ORDER
        
        response = requests.delete(
            url=url + api_call,
            headers=headers,
            params=data,
        )
        return response
    
    @staticmethod
    def get_average_price(url, headers, data):
        assert '/fapi/' not in url, f'"{API_GET_AVERAGE_PRICE}" is not supported in futures!'

        api_call = API_GET_AVERAGE_PRICE
        data = {'symbol': data['symbol']}
        
        response = requests.get(
            url=url + api_call,
            headers=headers,
            params=data,
        )
        return response
    
    @staticmethod
    def get_agg_trades(url, headers, data):
        api_call = API_GET_AGG_TRADES
        data = {'symbol': data['symbol']}
        
        response = requests.get(
            url=url + api_call,
            headers=headers,
            params=data,
        )
        return response
    
    @staticmethod
    def get_my_allocations(url, headers, data):
        assert '/fapi/' not in url, f'"{API_GET_MY_ALLOCATIONS}" is not supported in futures!'

        api_call = API_GET_MY_ALLOCATIONS
        
        response = requests.get(
            url=url + api_call,
            headers=headers,
            params=data,
        )
        return response
    
    @staticmethod
    def get_all_order_list(url, headers, data):
        api_call = API_GET_ALL_ORDER_LIST
        
        response = requests.get(
            url=url + api_call,
            headers=headers,
            params=data,
        )
        return response


# class TEST_BINANCE_REQUEST(object):
#     client = BINANCE_CLIENT(api_key=API_KEY, private_key=load_private_key(PRIVATE_KEY_PATH), testnet=True)

#     def __init__(self):
#         pass
    
#     def test_get_price():
#         data = {'symbol': 'BTCUSDT'}
#         res = client.send(BINANCE_REQUEST.get_price, data=data)
    
#     def test_get_open_orders():
#         data = {'symbol': 'BTCUSDT'}
#         res = client.send(BINANCE_REQUEST.get_open_orders, data=data)
    
#     def test_get_account():
#         data = {}
#         res = client.send(BINANCE_REQUEST.get_account, data=data)

#     def test_place_order():
#         data = {
#             'symbol':       'BTCUSDT',
#             'side':         'SELL',
#             'type':         'LIMIT',
#             'timeInForce':  'GTC',
#             'quantity':     '1.0000000',
#             'price':        '0.20',
#             # 'recvWindow':   '5000',
#         }
#         res = client.send(BINANCE_REQUEST.place_order, data=data)

#     def test_get_exchange_info():
#         data = {}
#         res = client.send(BINANCE_REQUEST.get_exchange_info, data=data)

#     def test_get_historical_trades():
#         data = {'symbol': 'BTCUSDT'}
#         res = client.send(BINANCE_REQUEST.get_historical_trades, data=data)
        
#     def test_get_all_orders():
#         data = {'symbol': 'BTCUSDT'}
#         res = client.send(BINANCE_REQUEST.get_all_orders, data=data)

#     def test_get_klines():
#         data = {
#             'symbol':       'BTCUSDT',
#             'interval':     '1m',
#         }
#         res = client.send(BINANCE_REQUEST.get_klines, data=data)

#     def test_get_order():
#         data = {
#             'symbol': 'BTCUSDT',
#             'orderId': 1222,
#         }
#         res = client.send(BINANCE_REQUEST.get_order, data=data)
    
#     def test_delete_order():
#         data = {
#             'symbol': 'BTCUSDT',
#             'orderId': 1222,
#         }
#         res = client.send(BINANCE_REQUEST.delete_order, data=data)

#     def test_get_average_price():
#         data = {'symbol': 'BTCUSDT'}
#         res = client.send(BINANCE_REQUEST.get_average_price, data=data)
        
#     def test_get_agg_trades():
#         data = {'symbol': 'BTCUSDT'}
#         res = client.send(BINANCE_REQUEST.get_agg_trades, data=data)

#     def test_get_my_allocations():
#         data = {'symbol': 'BTCUSDT'}
#         res = client.send(BINANCE_REQUEST.get_my_allocations, data=data)
    
#     def test_get_all_order_list():
#         data = {}
#         res = client.send(BINANCE_REQUEST.get_all_order_list, data=data)