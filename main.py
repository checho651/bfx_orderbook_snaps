# Standard library imports.
import time
import os
import pprint

# Third-party module or package imports.
import schedule

# Code repository sub-package imports.
from users import snap_user
from bfx_rest import public_endpoints
from data_management import local_ops
from data_management import drive_connection


# Functions needed to perform task
def get_bfx_data(user: snap_user.SnapUser):
    """
    Merges both requests functions in order to create only one instance of schedule.Job
    :return:
    """
    for coin in user.pairs:
        public_endpoints.save_orderbook(
            symbol=coin,
            precision=user.precision,
            root_dir=user.data_dir
        )
        public_endpoints.save_ticker(symbol=coin, root_dir=user.data_dir)
    print("")


def zip_day_snapshots(user: snap_user.SnapUser):
    local_ops.zip_yesterday_data(coins=user.pairs, root_dir=user.data_dir)
    print("")


def move_day_tickers(user: snap_user.SnapUser):
    local_ops.move_yesterday_tickers(coins=user.pairs, root_dir=user.data_dir)
    print("")


def upload_data(user: snap_user.SnapUser):
    """Uploads to google drive yesterday files"""
    # Update google drive credentials.
    user.update_drive()

    # Upload book snapshots
    drive_connection.upload_files(
        drive=user.drive,
        folder_id=user.drive_book_folder_id,
        files_dir=os.path.join(user.data_dir, 'zipped_books')
    )

    # Upload tickers
    drive_connection.upload_files(
        drive=user.drive,
        folder_id=user.drive_ticker_folder_id,
        files_dir=os.path.join(user.data_dir, 'day_tickers')
    )
    print("")


print("")
# Creates instance of main user
main_user = snap_user.SnapUser()
print('User Parameters')
pprint.pprint(main_user.__dict__)  # Prints attributes.
print("")

# Get schedule times using interval configuration of main_user.
hours_on_day = [f'{i:02d}' for i in range(0, 24, 1)]  # List with hours in the day.
minutes_on_hour = [f'{j:02d}' for j in range(0, 60, main_user.interval)]  # List with minutes scheduled in the hour.
# List combining hours and minutes for schedule tasks
scheduled_times = [f'{hour}:{minute}:00' for hour in hours_on_day for minute in minutes_on_hour]

print('Scheduled jobs')
# Creates instances of schedule.Job class for getting bfx data.
for instant in scheduled_times:
    get_data = schedule.every().day.at(instant).do(get_bfx_data, main_user)
    print(get_data)

# Schedule zipping book snapshots.
print("")
zip_books = schedule.every().day.at(main_user.zipping_time).do(zip_day_snapshots, main_user)
print(zip_books)

# Schedule moving day tickers
print("")
move_tickers = schedule.every().day.at(main_user.moving_time).do(move_day_tickers, main_user)
print(move_tickers)

# Schedule uploading task.
print("")
drive_upload = schedule.every().day.at(main_user.uploading_time).do(upload_data, main_user)
print(drive_upload)
print("")

# Infinite loop for running scheduled tasks.
while True:
    schedule.run_pending()
    time.sleep(1)
