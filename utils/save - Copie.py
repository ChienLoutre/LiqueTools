

import maya.cmds as mc
import os
import sys
from variables import *
import padding_numbers


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#           Save Version File
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


def version():

	filename = mc.file(q=True, sn=True)

	charvalue = filename.split('/')

	# Verifier que l'on est dans le projet

	if not project_name in charvalue:

		sys.exit('You are not working in the Project !!')


	# Sortir l'emplacement du fichier seulement

	file_path = charvalue[:-1]
	filepath = '/'.join(file_path)
	path_versions = os.listdir(filepath)

	print(path_versions)


	print('charvalue  =  ' + str(charvalue))
	print('file_path  =  ' + str(file_path))
	file_path = '/'.join(charvalue)

	filevalue = path_versions[-1].split('_')

	indexing = filevalue[-1].split('.')

	indexingbis = int(indexing[0])

	indexingbis += 1

	print (indexingbis)

	indexingbis = padding_numbers.padder(indexingbis, pad)

	indexing.pop(0)
	indexing.insert(0, indexingbis)
	indexing = '.'.join(indexing)

	filevalue.pop(-1)
	filevalue.append(indexing)

	filevalue = '_'.join(filevalue)

	charvalue.pop(-1)
	charvalue.append(filevalue)
	charvalue = '/'.join(charvalue)


	print (charvalue)
	print(filevalue)

	mc.file(rename = charvalue)


	date = mc.date()
	mc.fileInfo('creator',pc_name)
	mc.fileInfo('date', date)


	mc.file(save = True, type = 'mayaAscii')

	new_name = charvalue 

	return new_name


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#           Save Master File
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def master():

	filename = mc.file(q=True, sn=True)

	charvalue = filename.split('/')

	# Verifier que l'on est dans le projet

	if not project_name in charvalue:

		sys.exit('You are not working in the Project !!')


	# Sortir l'emplacement du fichier seulement

	file_path = charvalue[:-2]
	file_path = '/'.join(file_path)

	print(charvalue)


	filevalue = charvalue[-1]
	filevalue = filevalue.split('_')
	beauty_name = filevalue[0]
	filevalue = filevalue[0] + '_MASTER.mb'

	charvalue = file_path + '/' + filevalue

	go_on = mc.confirmDialog(title='Save Version First ?', message = 'Do you want to save a version for the asset : ' + beauty_name.capitalize() + ' before saving a Master file ?', button =['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No')

	if go_on == 'Yes':

	    new_name = version()


	if os.path.exists(charvalue):
	    
	    go_on = mc.confirmDialog(title='Saving Master', message = 'A MASTER file already exists for : ' + beauty_name.capitalize() + ', do you want to overwrite it ?', button =['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No')

	    if go_on == 'No':

	        sys.exit('Master creation aborted')

	mc.file(rename = charvalue)
	mc.file(save = True, type = 'mayaBinary')
	mc.file(new_name, open=True)


