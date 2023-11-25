#!/usr/bin/env python3
'''
Reference: 
  https://www.binance.com/en/support/faq/how-to-download-historical-market-data-on-binance-5810ae42176b4770b880ce1f14932262
'''
import hashlib
import requests
from datetime import datetime

from binance_api.variables import HISTORY_DATA_URL

class History(object):
    def __init__(self):
        self.base_url = HISTORY_DATA_URL
    
    def download(self, market, frequency, data_type, symbol, granularity, date):
        """
        Example URL:
        https://data.binance.vision/data/spot/monthly/klines/ADABKRW/1h/ADABKRW-1h-2020-08.zip
        """

        
        kwargs = locals()
        kwargs.pop('self')
        self._verify(**kwargs)

        url = "/".join([
            self.base_url, 
            market, 
            frequency, 
            data_type,
            symbol,
            granularity,
            "-".join([symbol, granularity, date]) + '.zip'
        ])

        
        print(f"The URL to be downloaded is {url}")
        data = requests.get(url, stream=True)
        if data.ok:
            data_check = requests.get(url + ".CHECKSUM")
        else:
            raise Exception(f"Status Code: {data.status_code}: Failed to download from {url}")
        
        return data, data_check
        
    def _verify(self, market, frequency, data_type, granularity, date, **kwargs):
        assert market in ['spot', 'futures/cm', 'futures/um'], 'The market must be spot, futures/cm, or futures/um'
        assert frequency in ['daily', 'monthly'], 'The frequence must be daily or monthly'
        assert data_type in ['klines', 'trades'], 'The data_type must be klines or trades'
        assert granularity in ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', 
                               '6h', '8h', '12h', '1d', '3d', '1w', '1M'], 'The granularity is not supported'
