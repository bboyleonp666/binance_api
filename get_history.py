import argparse
import subprocess

from binance_api import History

def parse_arg():
    parser = argparse.ArgumentParser(description='Download historical data from Binance')
    parser.add_argument('-m', '--market', type=str, default='futures/um', 
                        help='Market to download (default: futures/um), \
                            \nsupports: spot, futures/cm, futures/um')
    parser.add_argument('-f', '--frequency', type=str, default='daily', 
                        help='Frequency to download (default: daily), \
                            \nsupports: daily/monthly')
    parser.add_argument('-d', '--data-type', type=str, default='klines', 
                        help='Date type to download (default: klines)')
    parser.add_argument('-s', '--symbol', type=str, default='BTCUSDT', 
                        help='Symbol to download (default: BTCUSDT) \
                            \nNote: case insensitive, e.g. btcusdt, BTCUSDT, btcUSDT, etc.')
    parser.add_argument('-g', '--granularity', type=str, default='1m', 
                        help='Time granularity to download (default: 1m), \
                            \nsupports: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M')
    parser.add_argument('--start', type=str, default='2020-01-01', 
                        help='Start month to download (default: 2020-01-01), \
                            \nNote: the current date is not included')
    parser.add_argument('--end', type=str, default='2020-01-01', 
                        help='End date to download (default: 2020-01-01)')
    parser.add_argument('--output', type=str, default='data', 
                        help='Output folder (default: data)')

    args = parser.parse_args()
    args.symbol = args.symbol.upper()

    subprocess.run(['mkdir', '-p', args.output])
    return args

async def download(**kwargs):
    downloader = History()
    await downloader.download(**kwargs)

def main():
    args = parse_arg()
    downloader = History()
    date_range = downloader.gen_date_ranges(
        start=args.start, 
        end=args.end, 
        frequency=args.frequency
    )

    # res = downloader.download(market=args.market,
    #                           frequency=args.frequency,
    #                           data_type=args.data_type,
    #                           symbol=args.symbol,
    #                           granularity=args.granularity,
    #                           date=args.start)

    # save_path = f'{args.output}/{args.symbol}-{args.granularity}-{args.start}'
    # downloader.save(res, save_path, extract=True)

if __name__ == '__main__':
    main()