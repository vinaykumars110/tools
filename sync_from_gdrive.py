from projects_sync.projects_sync_common_functions import unzip_dir
from Google_drive_1.Google_drive import common_functions as gdrive_funcs
from Google_drive_1.Google_drive import get_home_dir,download_file_gdrive,list_files_gdrive
import os
import time

def sync_from_gdrive():
	# Recent file in Drive
	recent_file = list_files_gdrive.list_files_gdrive(1)
	#print(recent_file[0]['name'])
	filename_words = recent_file[0]['name'].split('/')
	filename = filename_words[len(filename_words)-1].split('.')[0]
	print(filename)

	# download the file
	download_file_gdrive.download_file_gdrive(recent_file[0]['id'])

	# Move the existing directory to _old
	if os.path.exists(get_home_dir.get_home_dir()+filename):
		os.rename(get_home_dir.get_home_dir()+filename,get_home_dir.get_home_dir()+filename+'_'+str(time.time()))
	# unzip the directory
	unzip_dir.unzip_dir(get_home_dir.get_home_dir()+filename_words[len(filename_words)-1])

if __name__ == "__main__":
	sync_from_gdrive()
