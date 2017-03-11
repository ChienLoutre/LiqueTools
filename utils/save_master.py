# Save Master file


import maya.cmds as mc
import os
from variables import *
import padding_numbers
import save_version

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

	    new_name = save_version.version()


	if os.path.exists(charvalue):
	    
	    go_on = mc.confirmDialog(title='Saving Master', message = 'A MASTER file already exists for : ' + beauty_name.capitalize() + ', do you want to overwrite it ?', button =['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No')

	    if go_on == 'No':

	        sys.exit('Master creation aborted')

	mc.file(rename = charvalue)
	mc.file(save = True, type = 'mayaBinary')
	mc.file(new_name, open=True)


