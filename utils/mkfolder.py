import os

def cr_folder(folder, access):

	os.mkdir(folder)
	os.chmod(folder, access)

	return