import MaxPlus as mc
import time
import os
import sys
from variables import *
import padding_numbers
import utils.get_extension as ext
reload(ext)



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#           Save Version File for MAX
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


def version():

	fm = mc.FileManager

	filename = fm.GetFileNameAndPath()

	charvalue = filename.split('\\')

	# Verifier que l'on est dans le projet

	if not project_name in charvalue:

		sys.exit('You are not working in the Project !!')


	# Sortir l'emplacement du dossier de version seulement

	file_path = charvalue[:-2]
	filepath = '\\'.join(file_path)
	path_versions = os.listdir(filepath)

	file_path = '\\'.join(charvalue)


	filevalue = path_versions[-1]

	indexing = filevalue.split('V')
	indexing = int(indexing[-1])

	indexing += 1


	indexing = padding_numbers.padder(indexing, pad)


	filevalue = 'V' + str(indexing)

	file_type, extension = ext.get_ext(charvalue[-1])


	charvalue.pop(-1)
	charvalue.pop(-1)
	charvalue.append(filevalue)
	charvalue = '\\'.join(charvalue)

	os.mkdir(charvalue)

	charvalue = charvalue + '\\' + file_type + '.' + extension

	print(charvalue)
	fm.Save(charvalue)

	print('version number ' + str(indexing) + ' created !')
	return charvalue


def folder_only():

	fm = mc.FileManager

	filename = fm.GetFileNameAndPath()

	charvalue = filename.split('\\')

	print(filename)
	print(charvalue)

	# Verifier que l'on est dans le projet

	if not project_name in charvalue:

		sys.exit('You are not working in the Project !!')


	# Sortir l'emplacement du dossier de version seulement

	file_path = charvalue[:-2]
	filepath = '\\'.join(file_path)
	path_versions = os.listdir(filepath)

	file_path = '\\'.join(charvalue)


	filevalue = path_versions[-1]

	indexing = filevalue.split('V')
	indexing = int(indexing[-1])

	indexing += 1


	indexing = padding_numbers.padder(indexing, pad)


	filevalue = 'V' + str(indexing)

	file_type, extension = ext.get_ext(charvalue[-1])


	charvalue.pop(-1)
	charvalue.pop(-1)
	charvalue.append(filevalue)
	charvalue = '\\'.join(charvalue)

	os.mkdir(charvalue)

	print(charvalue)
	return charvalue