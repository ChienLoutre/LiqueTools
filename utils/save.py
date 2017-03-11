import time
import maya.cmds as mc
import os
import sys
from variables import *
import padding_numbers
import utils.get_extension as ext
import utils.create as create
reload(ext)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#		   Save Version File
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 



def version():

	filename = mc.file(q=True, sn=True)

	charvalue = filename.split('/')

	# Verifier que l'on est dans le projet

	if not project_name in charvalue:

		sys.exit('You are not working in the Project !!')


	# fait un thumbnail

	create.thumbnail()

	# Sortir l'emplacement du dossier de version seulement

	file_path = charvalue[:-2]
	filepath = '/'.join(file_path)
	path_versions = os.listdir(filepath)

	file_path = '/'.join(charvalue)


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
	charvalue = '/'.join(charvalue)

	os.mkdir(charvalue)

	charvalue = charvalue + '/' + file_type

	new_name = charvalue + '.' + extension


	mc.file(rename = new_name)
	mc.file(save = True, type = 'mayaAscii')


	print('version number ' + str(indexing) + ' created !')
	mc.warning('version number ' + str(indexing) + ' created !')

	return new_name


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#		   Save Master File
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def master(comments = '', merge_refs=False, bin_or_ascii='mayaBinary', ask_version=True):

	print('Master save STARTED')

	filename = mc.file(q=True, sn=True)

	charvalue = filename.split('/')

	# Verifier que l'on est dans le projet

	if not project_name in charvalue:

		sys.exit('You are not working in the Project !!')


	# Sortir l'emplacement du fichier seulement

	file_path = charvalue[:-2]
	file_path = '/'.join(file_path)

	filevalue = charvalue[-2]
	file_type, extension = ext.get_ext(charvalue[-1])


	charvalue.pop(-1)
	charvalue.pop(-1)
	
	charvalue = '/'.join(charvalue)
	charvalue = charvalue + '/master'

	new_name = filename

	if ask_version == True:

		go_on = mc.confirmDialog(title='Save Version First ?', message = 'Do you want to save a version for the asset : ' + file_type.capitalize() + ' before saving a Master file ?', button =['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No')


		print('charvalue ==> ' + charvalue)


		if go_on == 'Yes':

			new_name = version()


	if os.path.exists(charvalue):
		
		go_on = mc.confirmDialog(title='Saving Master', message = 'A MASTER file already exists for : ' + file_type.capitalize() + ', do you want to overwrite it ?', button =['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No')

		if go_on == 'No':

			if ask_version == False:
				mc.file(new_name, open=True, force=True)
				sys.exit('Master creation aborted')
	else:
		os.mkdir(charvalue)


	date = time.strftime('%c')
	hour = time.strftime('%x')

	if not comments == '':

		comments = ' ____ ' + comments

	with open(charvalue + '/' + 'infos.txt', "a") as f:
		f.write('\r\n' + date + ' by ' + pc_name + ' : from ' + filevalue + comments)

	mc.file(rename = charvalue + '/' + file_type)

	# query the references in the scene

	if merge_refs == True:

		namespaces = mc.namespaceInfo(listOnlyNamespaces=True )
		namespaces.pop(0)
		namespaces.pop(-1)

		for each in namespaces:

			mc.namespace(removeNamespace=each, mnr=True)


		sel = mc.ls(references=True)

		for each in sel:

			each = mc.referenceQuery(each,filename=True )


			mc.file(each, ir=True)

	try:
		mc.file(save = True, type = 'mayaBinary')
	except RuntimeError:
		mc.file(save = True, type = 'mayaAscii')
		
	create.thumbnail()


	print(new_name)
	mc.file(new_name, open=True)

	mc.warning('Master created !')

