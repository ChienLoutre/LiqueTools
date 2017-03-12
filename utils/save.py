import time
import os
import sys
from variables import *
import padding_numbers
import utils.get_extension as ext


reload(ext)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#		   Save Version File
# Works in Maya and Guerilla Render
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def app_chk():

	open_app = None

	try:
		import maya.cmds as mc
		open_app = 'maya'
		print('Working on MAYA')
	except:
		from guerilla import Document
		doc = Document()
		open_app = 'grender'

	return open_app

def version():
	'''
	Creates a version of the file you are working on.
	You MUST be in your Project to use this function.

	syntax :

	version()
	'''
	open_app = app_chk()

	if open_app == 'maya':
		import maya.cmds as mc
		filename = mc.file(q=True, sn=True)
	elif open_app == 'grender':
		from guerilla import Document
		doc = Document()
		filename = doc.getfilename()
	elif open_app == None:
		raise SystemError('You are not in an Application supported by this script')

	charvalue = str(filename).split('/')

	# Verifier que l'on est dans le projet

	if not project_name in charvalue:

		sys.exit('You are not working in the Project !')


	# fait un thumbnail

	if open_app == 'maya':

		import utils.create as create
		create.thumbnail()

	# Sortir l'emplacement du dossier de version seulement

	file_path = charvalue[:-2]
	filepath = '/'.join(file_path)
	path_versions = os.listdir(filepath)

	# verifier si dossier "wip" dans la version.

	if 'wip' in path_versions:
		path_versions.remove('wip')

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

	if open_app == 'maya':

		mc.file(rename = new_name)
		mc.file(save = True, type = 'mayaAscii')
		mc.warning('version number ' + str(indexing) + ' created !')
	elif open_app == 'grender':

		doc.save(filename = new_name, warn=True, addtorecent=False)

	print('version number ' + str(indexing) + ' created !')

	return new_name


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#		   Save Master File
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def master(comments = '', merge_refs=False, bin_or_ascii='mayaBinary', ask_version=True):
	'''
	Creates a MASTER for your file, that you can reference in your other scenes.
	
	If you need to break references (in case of a Rig Master, for example), do not forget
	to check <merge_refs=True>. Otherwise this is NOT recommended.

	syntax:

	master(comments = '', merge_refs=False, bin_or_ascii='mayaBinary', ask_version=True)
	'''
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

