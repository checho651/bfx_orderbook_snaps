# Standard library imports.
from datetime import datetime
import time
import os
import csv

# Third-party module or package imports.
import requests


def save_orderbook(symbol: str, precision: str, root_dir: str):
    """
    Save orderbook for currency selected as csv.
    File will be saved in snapshots directory of symbol selected in root_dir.
    Each snapshot will be stored in independent files.

    :param root_dir: where local data will be store during current day.
    :param symbol: symbol with type prefix ('fUSD').
    :param precision: level of price aggregation ('P0' to 'P4'. 'R0' for raw) 
    :return: None
    """
    try:
        # Request orderbook information.
        url = f'https://api-pub.bitfinex.com/v2/book/{symbol}/{precision}?_full=1'
        request = requests.get(url)
        full_book = request.json()  # Gets a list from full book.

        # Get path for the file with time information.
        local_time = datetime.strftime(datetime.utcnow(), format='%y-%m-%dT%H.%M')
        dir_path = os.path.join(
            root_dir,
            'temp_data',
            symbol,
            'snapshots',
            symbol + '_' + local_time[:8] + '_booksnapshots'
        )

        # Checks if day folder already exists.
        try:
            os.makedirs(dir_path)  # Creates every folder needed in dir_path.
            print(f'Folder {dir_path} created')
        except FileExistsError:
            pass

        # Get file path.
        file_name = f'{symbol}_{local_time}_booksnapshot.csv'
        file_path = os.path.join(dir_path, file_name)
        print(f'Book stored: {file_path}')

        # Saves book information as csv.
        # If file doesn't exists, it will be created automatically.
        with open(file_path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(full_book)

    except Exception as e:
        print(f'save_orderbook: {e}')


def save_ticker(symbol: str, root_dir: str):
    """
    Saves ticker information for funding currency specified.
    One file will store whole day information.
    File will be saved in tickers directory of symbol selected in root_dir.
    Timestamp in milliseconds is added in ticker list.

    :param root_dir: where local data will be store during current day.
    :param symbol: symbol with type prefix ('fUSD').
    :return: None
    """
    try:
        # Request ticker information.
        url = f'https://api-pub.bitfinex.com/v2/tickers?symbols={symbol}'
        request = requests.get(url)
        ticker = request.json()  # Gets a list from full book.
        ticker[0].append(int(time.time() * 1000))

        # Get path for the file with time information.
        local_time = datetime.strftime(datetime.utcnow(), format='%y-%m-%d')
        file_name = f'{symbol}_{local_time}_tickers.csv'
        file_path = os.path.join(
            root_dir,
            'temp_data',
            symbol,
            'tickers',
            file_name
        )
        print(f'Ticker appended: {file_path}')

        # Saves ticker information in csv.
        # If path already exits, it will append a new row to at the end of the csv.
        with open(file_path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(ticker[0])

    except Exception as e:
        print(f'save_ticker: {e}')

