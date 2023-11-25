#!/usr/bin/env python3
'''
Reference: 
  https://www.binance.com/en/support/faq/how-to-download-historical-market-data-on-binance-5810ae42176b4770b880ce1f14932262
'''

import os
import io
import zipfile
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
            print("Download is successful!")
            data_check = requests.get(url + ".CHECKSUM")
            sha256_checksum = data_check.text.split()[0]
        else:
            raise Exception(f"Status Code: {data.status_code}, failed to download from {url}")
        
        self._verify_sha256(content=data.content, checksum=sha256_checksum)
        return data
    
    def _verify_sha256(self, content, checksum):
        sha256 = hashlib.sha256()
        sha256.update(content)
        assert sha256.hexdigest() == checksum, "Downloaded file is corrupted!"
        print("Downloaded file checksum is verified!")
        
    def _verify(self, market, frequency, data_type, granularity, date, **kwargs):
        assert market in ['spot', 'futures/cm', 'futures/um'], 'The market must be spot, futures/cm, or futures/um'
        assert frequency in ['daily', 'monthly'], 'The frequence must be daily or monthly'
        assert data_type in ['klines', 'trades'], 'The data_type must be klines or trades'
        assert granularity in ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', 
                               '6h', '8h', '12h', '1d', '3d', '1w', '1M'], 'The granularity is not supported'
        
        if frequency == 'daily':
            try:
                datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                raise ValueError("Incorrect data format, should be YYYY-MM-DD")
        assert datetime.strptime(date, '%Y-%m-%d') < datetime.today(), 'The start date must be earlier than today'
    
    @staticmethod
    def save(data, output, extract=True):
        if extract:
            io_data = io.BytesIO(data.content)
            with zipfile.ZipFile(io_data) as f:
                f.extractall(output)

        else:
            with open(output, 'wb') as f:
                f.write(data.content)
