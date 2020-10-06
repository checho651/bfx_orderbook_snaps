# Standard library imports.
import csv
from datetime import datetime
import time
import os

# Third-party module or package imports.
import requests
import schedule


def save_orderbook(symbol: str = 'fUSD'):
    """
    Save orderbook for currency selected as csv.
    File will be saved in snapshot directory.
    Each snapshot will be stored in independent files.

    :param symbol: symbol with type prefix ('fUSD').
    :return: None
    """
    try:
        # Request orderbook information.
        print("")
        print('GETTING ORDER BOOK INFORMATION')
        url = 'https://api-pub.bitfinex.com/v2/book/fUSD/P0?_full=1'
        request = requests.get(url)
        full_book = request.json()  # Gets a list from full book.

        # Get path for the file with time information.
        local_time = datetime.strftime(datetime.utcnow(), format='%y-%m-%dT%H.%M')
        dir_path = os.path.join(symbol, 'snapshots', symbol + ' ' + local_time[:8])

        # Checks if day folder already exists.
        try:
            os.makedirs(dir_path)
            print(f'Folder {dir_path} created')
        except:
            pass
        file_name = f'{symbol} {local_time}_booksnapshot.csv'
        file_path = os.path.join(dir_path, file_name)
        print(f'file_path: {file_path}')

        # Saves book information as csv.
        # If file doesn't exists, it will be created automatically.
        with open(file_path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(full_book)

    except Exception as e:
        print("ORDERBOOK COULDN'T BE STORED")
        print(e)


def save_ticker(symbol: str = 'fUSD'):
    """
    Saves ticker information for funding currency specified.
    One file will store whole day information.
    Timestamp in milliseconds is added in ticker list.

    :param symbol: symbol with type prefix ('fUSD').
    :return: None
    """
    try:
        # Request ticker information.
        print('GETTING TICKER')
        url = f'https://api-pub.bitfinex.com/v2/tickers?symbols={symbol}'
        request = requests.get(url)
        ticker = request.json()  # Gets a list from full book.
        ticker[0].append(int(time.time() * 1000))

        # Get path for the file with time information.
        local_time = datetime.strftime(datetime.utcnow(), format='%y-%m-%d')
        file_name = f'{symbol} {local_time}_ticker.csv'
        file_path = os.path.join(symbol, 'tickers', file_name)
        print(f'file_path: {file_path}')

        # Saves ticker information in csv.
        # If path already exits, it will append a new row to at the end of the csv.
        with open(file_path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(ticker[0])

    except Exception as e:
        print("ORDERBOOK COULDN'T BE STORED")
        print(e)


def get_data(coins: list):
    """
    Merges both requests functions in order to create only one instance of schedule.Job
    :return:
    """
    for coin in coins:
        save_orderbook(coin)
        save_ticker(coin)


print("")
print("")

# List of pairs to fetch data
pairs = ['fUSD', 'fEUR', 'fGBP', 'fJPY', 'fUST']

# Create folders to store files in working directory.
folders_needed = ['snapshots', 'tickers']
for pair in pairs:
    for folder in folders_needed:
        try:
            directory = os.path.join(pair, folder)
            os.makedirs(directory)
            print(f'Folder {directory} created')
            print("")
        except Exception as e:
            print(f'Check if {directory} already exists')
            print(e)
            print("")


interval = 5
hours_on_day = [f'{i:02d}' for i in range(0, 24, 1)]  # List with hours in the day
minutes_on_hour = [f'{j:02d}' for j in range(0, 60, interval)]  # List with minutes scheduled in the hour
# List combining hours and minutes for schedule tasks
scheduled_times = [f'{hour}:{minute}:00' for hour in hours_on_day for minute in minutes_on_hour]


# Creates instances of schedule.Job class for every day tasks.
for instant in scheduled_times:
    job = schedule.every().day.at(instant).do(get_data,pairs)
    print(job)
print("")


# Infinite loop for running scheduled tasks.
while True:
    schedule.run_pending()
    time.sleep(1)
