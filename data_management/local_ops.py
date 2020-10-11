# Standard library imports.
import os
import shutil
from datetime import datetime, timedelta


def zip_yesterday_data(coins: list, root_dir):
    """Creates .zip from day snapshots, erase data folder"""
    today_time = datetime.utcnow()
    yesterday_time = today_time - timedelta(days=1)
    yesterday = datetime.strftime(yesterday_time, format='%y-%m-%d')

    for coin in coins:
        yesterday_folder = coin + '_' + yesterday + '_booksnapshots'
        try:
            yesterday_data_dir = os.path.join(
                root_dir,
                'temp_data',
                coin,
                'snapshots',
                yesterday_folder
            )
            output_file = os.path.join(root_dir, 'zipped_books', yesterday_folder)
            zipped_file = shutil.make_archive(
                output_file,
                'zip',
                yesterday_data_dir
            )
            print(f'Day snapshots zipped to: {zipped_file}')
            shutil.rmtree(yesterday_data_dir)  # Erase data.
        except Exception as e:
            print(f'zip_yesterday_data: {e}')


def move_yesterday_tickers(coins: list, root_dir):
    """Moves day tickers .csv to output folder"""
    try:
        today_time = datetime.utcnow()
        yesterday_time = today_time - timedelta(days=1)
        yesterday = datetime.strftime(yesterday_time, format='%y-%m-%d')
        for coin in coins:
            yesterday_data_dir = os.path.join(
                root_dir,
                'temp_data',
                coin,
                'tickers',
                f'{coin}_{yesterday}_tickers.csv'
            )
            day_tickers_dir = os.path.join(
                root_dir,
                'day_tickers',
                f'{coin}_{yesterday}_tickers.csv'
            )
            shutil.move(yesterday_data_dir, day_tickers_dir)
            print(f'Day ticker moved to: {day_tickers_dir}')
    except Exception as e:
        print(f'move_yesterday_tickers: {e}')
