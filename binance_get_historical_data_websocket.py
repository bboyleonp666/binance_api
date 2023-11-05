import pandas as pd
from binance.websockets import BinanceSocketManager
from binance.enums import KLINE_INTERVAL_1HOUR

# Define historical data parameters
symbol = 'btcusdt'
start_time = '1 Jan 2021 00:00:00'
end_time = '31 Jan 2021 23:59:59'
interval = KLINE_INTERVAL_1HOUR

# Define function to process WebSocket klines data
def process_message(msg):
    global klines
    klines.append(msg['k'])
    if msg['k']['t'] >= end_timestamp:
        # Stop WebSocket connection after all data has been received
        bsm.stop_socket(conn_key)

# Convert start and end times to timestamps
start_timestamp = pd.Timestamp(start_time).timestamp() * 1000
end_timestamp = pd.Timestamp(end_time).timestamp() * 1000

# Connect to Binance WebSocket API
bsm = BinanceSocketManager()
conn_key = bsm.start_kline_socket(symbol, interval, process_message)

# Initialize klines list
klines = []

# Wait for WebSocket connection to receive all data
bsm.start()

# Convert data to pandas DataFrame
df = pd.DataFrame(klines, columns=['t', 'o', 'h', 'l', 'c', 'v', 'ct', 'qav', 'not', 'tbav', 'tqav', 'ignore'])

# Convert timestamp to datetime format
df['t'] = pd.to_datetime(df['t'], unit='ms')

# Set timestamp as index
df.set_index('t', inplace=True)

# Convert columns to numeric format
df = df.apply(pd.to_numeric)

# Print DataFrame
print(df)