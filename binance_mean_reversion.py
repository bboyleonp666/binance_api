import time
from binance.client import Client

# Set up Binance API credentials
api_key = 'your_api_key'
api_secret = 'your_api_secret'
client = Client(api_key, api_secret)

# Define mean reversion strategy parameters
window_size = 20
buy_threshold = 0.05
sell_threshold = 0.05
symbol = 'BTCUSDT'

# Define function to retrieve current price from Binance API
def get_current_price(symbol):
    ticker = client.get_symbol_ticker(symbol=symbol)
    return float(ticker['price'])

# Define function to calculate moving average
def calculate_moving_average(prices, window_size):
    if len(prices) < window_size:
        return None
    return sum(prices[-window_size:]) / window_size

# Define function to place buy/sell orders
def execute_trade(side, quantity, symbol):
    try:
        order = client.create_order(
            symbol=symbol,
            side=side,
            type=Client.ORDER_TYPE_MARKET,
            quantity=quantity
        )
        print(f"Successfully executed {side} order for {quantity} {symbol}")
    except Exception as e:
        print(f"Error executing {side} order: {e}")

# Monitor price and execute trades
prices = []
while True:
    # Get current price and add to price history
    price = get_current_price(symbol)
    prices.append(price)

    # Calculate moving average
    ma = calculate_moving_average(prices, window_size)

    # Place buy/sell order if necessary
    if ma is not None:
        if price < ma * (1 - buy_threshold):
            execute_trade(Client.SIDE_BUY, 0.001, symbol)
        elif price > ma * (1 + sell_threshold):
            execute_trade(Client.SIDE_SELL, 0.001, symbol)

    # Wait for next iteration
    time.sleep(60)