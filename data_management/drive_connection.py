# Standard library imports.
import os

# Third-party module or package imports.
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def google_drive_authentication(credentials):
    """Receive credentials in .txt format and creates GoogleDrive object.

    :param credentials: credentials file path including name and extension.
    :return: GoogleDrive object to interact with API.
    """
    google_auth = GoogleAuth()

    # Try to load saved client credentials.
    google_auth.LoadCredentialsFile(credentials_file=credentials)

    if google_auth.access_token_expired:
        # Refresh credentials if they expired.
        google_auth.Refresh()
    else:
        # Initialize the saved credentials.
        google_auth.Authorize()

    # Save the current credentials to a file.
    google_auth.SaveCredentialsFile(credentials_file=credentials)

    drive = GoogleDrive(google_auth)
    return drive


def create_drive_folder(drive: GoogleDrive, folder_name: str):
    folder = drive.CreateFile({
        'title': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    })
    folder.Upload()
    print(f'Folder created: {folder}', end='\n')


def get_drive_folder_id(drive: GoogleDrive, folder: str):
    """Checks if folder exits, if not it creates it"""

    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    drive_folders_available = [file['title'] for file in file_list]

    if folder not in drive_folders_available:
        create_drive_folder(drive=drive, folder_name=folder)
        file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()

    folder_id = [file['id'] for file in file_list if file['title'] == folder][0]
    print(f'Drive id for {folder}: {folder_id}')
    print("")
    return folder_id


def upload_files(drive: GoogleDrive, folder_id: str, files_dir: str):
    """Upload files in local files_dir to drive folder folder_id. Erase data at the end"""
    try:
        files_to_upload = os.listdir(files_dir)
        file_paths = [os.path.join(files_dir, file) for file in files_to_upload]
        for file in file_paths:
            drive_file = drive.CreateFile({'parents': [{'id': folder_id}]})
            drive_file.SetContentFile(file)
            drive_file['title'] = os.path.basename(file)
            drive_file.Upload()
            print(f'File uploaded: {drive_file}')
            os.remove(file)
            print(f'File removed: {file}')
    except Exception as e:
        print(f'upload_files: {e}')
