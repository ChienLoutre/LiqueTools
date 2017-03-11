import maya.cmds as mc
import os
import sys
from variables import *
import padding_numbers
import utils.get_extension as ext
import shutil

def g_asset_export(cache = 2, refs=1):

	filename = mc.file(q=True, sn=True)

	charvalue = filename.split('/')

	# Verifier que l'on est dans le projet

	if not project_name in charvalue:
		sys.exit('You are not working in the Project !!')


	# Sortir l'emplacement du fichier seulement

	file_path = charvalue[:-1]

	filevalue = charvalue[-1]

	print('filevalue => ' + filevalue)

	filevalue, extension = ext.get_ext(filevalue)

	if cache == 1:

		go_on = mc.confirmDialog(title='Creating Guerilla Project', message = 'Export Cache Only selected. Continue ?', button =['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No')

		if go_on == 'No':

			sys.exit('Guerilla Project creation aborted')



	file_path.pop(-1)
	file_path.pop(-1)
	print(charvalue)

	file_path = '/'.join(file_path)
	print('file_path => '+ file_path)
	print(filevalue)

	if  not cache == 1:
		
		if not file_path + '/guerilla/V000':

			os.mkdir(file_path + '/guerilla/V000')




	charvalue = file_path + '/' + 'guerilla/' + 'tex'
	version_path = file_path + '/' + 'guerilla/V000/' + 'tex'
	print(charvalue)
	if not cache == 1:

		if os.path.exists(charvalue + '.gproject'):

			go_on = mc.confirmDialog(title='Creating Guerilla Project', message = 'A gproject file already exists for : ' + filevalue + '_tex, do you want to overwrite it ?', button =['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No')

			if go_on == 'No':

				sys.exit('Guerilla Project creation aborted')



	mc.GuerillaExport(mode=cache, cgr=refs, fte=2, pf=version_path + '.gproject', cf=charvalue + '.ghostproject')

	print('Guerilla asset project : ' + filevalue + '_tex' + ' successfully created !')

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#           Guerilla export with animation
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def g_layout_export(cache = 2):


	filename = mc.file(q=True, sn=True)

	charvalue = filename.split('/')

	# Verifier que l'on est dans le projet

	if not project_name in charvalue:
		sys.exit('You are not working in the Project !!')


	# Sortir l'emplacement du fichier seulement

	file_path = charvalue[:-1]
	file_path = '/'.join(file_path)

	filevalue = charvalue[-1]
	filevalue = filevalue.split('_')

	refs = mc.ls(rf=True)

	if not filevalue[-1] == 'MASTER.mb':

		sys.exit('MASTER file not selected. Please choose a MASTER file to create the Guerilla data.')

	if not refs:

		sys.exit('No References loaded. You may be in the wrong file...')


	if cache == 1:

		go_on = mc.confirmDialog(title='Creating Guerilla Project', message = 'Export Cache Only selected. Continue ?', button =['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No')

		if go_on == 'No':

			sys.exit('Guerilla Project creation aborted')


	filevalue = filevalue[0]
	print(file_path)
	print(filevalue)

	charvalue = file_path + '/' + filevalue + '_tex'

	if os.path.exists(charvalue + '.gproject'):

		go_on = mc.confirmDialog(title='Creating Guerilla Project', message = 'A gproject file already exists for : ' + filevalue + '_tex, do you want to overwrite it ?', button =['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No')

		if go_on == 'No':

			sys.exit('Guerilla Project creation aborted')

	mc.GuerillaExport(mode=cache, cgr=1, fte=1, pf=charvalue + '.gproject', cf=charvalue + '.ghostproject')

	print('Guerilla layout project : ' + filevalue + '_tex' + ' successfully created !')