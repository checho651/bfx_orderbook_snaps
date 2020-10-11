"""
user_configs.py needs to be save in this directory and have this lines:

# Standard library imports.
import os


# Standard configuration:
class Parameters:
    def __init__(self):
        # General parameters
        self.pairs = ['fUSD', 'fEUR', 'fGBP', 'fJPY', 'fUST', 'fBTC']
        self.interval = 5  # Minutes within snapshots/tickers created.
        self.zipping_time = '05:01:00'  # When to zip yesterday book snapshots.
        self.moving_time = '05:06:00'  # When to locally move yesterday tickers.
        self.uploading_time = '05:11:00'  # When to upload zipped and moved files to Google Drive.
        self.data_dir = 'data'  # Root folder for temporary data storage.
        # Google drive parameters
        self.google_drive_credentials_path = os.path.join('users', 'mycreds.txt')
        self.drive_book_folder = 'funding_book_snaps'  # Created if doesn't exits.
        self.drive_ticker_folder = 'funding_tickers'  # Created if doesn't exits.

"""