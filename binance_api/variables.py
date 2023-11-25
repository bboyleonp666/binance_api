#!/usr/bin/env python3

# REAL URL
SPOT_URL = 'https://api.binance.com'
FUTURE_URL = 'https://fapi.binance.com'

# TESTNET URL
TESTNET_SPOT_URL = 'https://testnet.binance.vision'
TESTNET_FUTURE_URL = 'https://testnet.binancefuture.com'

# Request parameters
API_SPOT_PREFIX = '/api/v3'
API_FUTURE_PREFIX = '/fapi/v1'

API_GET_PRICE = '/ticker/price'
API_GET_OPEN_ORDERS = '/openOrders'
API_GET_ACCOUNT = '/account'
API_GET_EXCHANGE_INFO = '/exchangeInfo'
API_GET_HISTORICAL_TRADES = '/historicalTrades'
API_GET_ALL_ORDERS = '/allOrders'
API_GET_ALL_ORDER_LIST = '/allOrderList'
API_GET_KLINES = '/klines'
API_GET_ORDER = '/order'
API_GET_AVERAGE_PRICE = '/avgPrice'
API_GET_AGG_TRADES = '/aggTrades'
API_GET_MY_ALLOCATIONS = '/myAllocations'

API_PLACE_ORDER = '/order'
API_DELETE_ORDER = '/order'

# Historical data URL
HISTORY_DATA_URL = 'https://data.binance.vision/data'