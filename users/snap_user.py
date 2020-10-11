# Standard library imports.
import os

# Third-party module or package imports.

# Code repository sub-package imports.
from data_management.drive_connection import google_drive_authentication
from data_management.drive_connection import get_drive_folder_id
from .user_configs import Parameters


class SnapUser(Parameters):
    """Main user which contains configuration parameters and connections"""

    def __init__(self):
        # Inherit parameters from Parameters.
        Parameters.__init__(self)

        # GoogleDrive object to authenticate connections.
        self.drive = google_drive_authentication(self.google_drive_credentials_path)
        # Check folders id in drive.
        self.drive_book_folder_id = get_drive_folder_id(self.drive, self.drive_book_folder)
        self.drive_ticker_folder_id = get_drive_folder_id(self.drive, self.drive_ticker_folder)

        # Create local directories needed.
        self.create_necessary_folders()
        print("")

    def create_necessary_folders(self):
        # Folders needed in each pair desired.
        folders_needed = ['snapshots', 'tickers']
        for pair in self.pairs:
            for folder in folders_needed:
                try:
                    directory = os.path.join(self.data_dir, 'temp_data', pair, folder)
                    os.makedirs(directory)
                    print(f'Folder {directory} created')
                except Exception as e:
                    print(f'create_necessary_folders.1: {e}')

        # Folders needed to store local data previous google drive upload.
        try:
            local_books_dir = os.path.join(self.data_dir, 'zipped_books')
            os.makedirs(local_books_dir)
            print(f'Folder {local_books_dir} created')
        except Exception as e:
            print(f'create_necessary_folders.2: {e}')
        try:
            local_tickers_dir = os.path.join(self.data_dir, 'day_tickers')
            os.makedirs(local_tickers_dir)
            print(f'Folder {local_tickers_dir} created')
        except Exception as e:
            print(f'create_necessary_folders.3: {e}')

    def update_drive(self):
        self.drive = google_drive_authentication(self.google_drive_credentials_path)
