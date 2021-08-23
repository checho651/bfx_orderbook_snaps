# bfx_orderbook_snaps
Store orderbook snapshots and ticker.

# Installation
Or via pip3:
```
python3.8 -m pip install -r requirements.txt
sudo python3.8 setup.py install
```

# Configuration
user_configs.py needs to be created in 'users' directory.
import os module and create Parameters class as follows:
```
# Standard library imports.
import os


# Standard configuration:
class Parameters:
    def __init__(self):
        # General parameters
        self.pairs = ['fUSD', 'fEUR', 'fGBP', 'fJPY', 'fUST', 'fBTC']
        self.precision = 'P0'
        self.interval = 5  # Minutes within snapshots/tickers created.
        self.zipping_time = '05:01:00'  # When to zip yesterday book snapshots.
        self.moving_time = '05:06:00' # When to locally move yesterday tickers.
        self.uploading_time = '05:11:00' # When to upload zipped and moved files to Google Drive.
        self.data_dir = 'data'  # Root folder for temporary data storage.
        # Google drive parameters
        self.google_drive_credentials_path = os.path.join('users', 'mycreds.txt')
        self.drive_book_folder = 'funding_book_snaps'  # Created if doesn't exits.
        self.drive_ticker_folder = 'funding_tickers'  # Created if doesn't exits.

``` 
Values are just examples, but variable types should remain the same.

Consider that zipping_time, moving_time and uploading time are local time. 


#Google credentials
google credentials may be stored in path specified in user_configs.py.
Store credentials in .txt format in specified credentials path.
Path should include file name and extension.


# Running
'main.py' needs to be run in order to run program.
