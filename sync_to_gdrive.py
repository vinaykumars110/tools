from projects_sync.projects_sync_common_functions import zip_folder
from Google_drive_1.Google_drive import common_functions as gdrive_funcs
import os

def sync_to_gdrive(directory):
	# zip the directory
	zip_folder.zip_dir(directory)

	# upload to GDrive
	gdrive_funcs.upload_file_gdrive(directory+'.zip')

	# Delete file
	os.remove(directory+'.zip')


if __name__ == "__main__":
	sync_to_gdrive(input())