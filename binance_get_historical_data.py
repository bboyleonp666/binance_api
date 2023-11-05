import pandas as pd
from binance.client import Client

# Set up Binance API credentials
api_key = 'your_api_key'
api_secret = 'your_api_secret'
client = Client(api_key, api_secret)

# Define historical data parameters
symbol = 'BTCUSDT'
start_time = '1 Jan 2021 00:00:00'
end_time = '31 Jan 2021 23:59:59'
interval = Client.KLINE_INTERVAL_1HOUR

# Retrieve historical data from Binance API
klines = client.get_historical_klines(symbol, interval, start_time, end_time)

# Convert data to pandas DataFrame
df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])

# Convert timestamp to datetime format
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

# Set timestamp as index
df.set_index('timestamp', inplace=True)

# Convert columns to numeric format
df = df.apply(pd.to_numeric)

# Print DataFrame
print(df)