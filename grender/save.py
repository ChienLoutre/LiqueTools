import time
import os
import sys
from variables import *
import padding_numbers
import utils.get_extension as ext
from guerilla import Document
doc = Document()

#--------------------------------------------
# Save Version / Master --- GUERILLA
#--------------------------------------------

def version():

	file_name = doc.getfilename()

	charvalue = str(file_name).split('/')

	# Verifier que l'on est dans le projet

	if not project_name in charvalue:

		print('You are not working in the Project !!')

	else:

		# Sortir l'emplacement du dossier de version seulement

		file_path = charvalue[:-2]

		print(charvalue)
		print(file_path)
		filepath = '/'.join(file_path)
		path_versions = os.listdir(filepath)

		# verifier si dossier "wip" dans la version.

		if 'wip' in path_versions:
			path_versions.remove('wip')

		file_path = '/'.join(charvalue)

		print(file_path)

		filevalue = path_versions[-1]
		print(filevalue)


		indexing = filevalue.split('V')
		indexing = int(indexing[-1])

		indexing += 1

		print(indexing)



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

		doc.save(filename = new_name, warn=True, addtorecent=False)

		print('version number ' + str(indexing) + ' created !')

		return new_name


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#           Save Master File
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def master(comments = ''):

	print('Master save STARTED')

	file_name = doc.getfilename()

	charvalue = str(file_name).split('/')

	# Verifier que l'on est dans le projet

	if not project_name in charvalue:

		print('You are not working in the Project !!')


	# Sortir l'emplacement du fichier seulement

	file_path = charvalue[:-2]
	file_path = '/'.join(file_path)
	
	print(charvalue)
	filevalue = charvalue[-2]
	file_type, extension = ext.get_ext(charvalue[-1])


	charvalue.pop(-1)
	charvalue.pop(-1)
	
	charvalue = '/'.join(charvalue)
	charvalue = charvalue + '/master'

	# Il faudrait le faire pour guerilla ca serait bien (confirm, et save version)

	#go_on = mc.confirmDialog(title='Save Version First ?', message = 'Do you want to save a version for the asset : ' + file_type.capitalize() + ' before saving a Master file ?', button =['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No')

	new_name = file_name

	print('charvalue ==> ' + charvalue)


	#if go_on == 'Yes':

	#    new_name = version()


	# Faudrait aussi voir comment faire ca sous Guerilla


#	if os.path.exists(charvalue):
#		
#		go_on = mc.confirmDialog(title='Saving Master', message = 'A MASTER file already exists for : ' + file_type.capitalize() + ', do you want to overwrite it ?', button =['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No')

#		if go_on == 'No':

#			sys.exit('Master creation aborted')
#	
#	
	if os.path.exists(charvalue):
		print('master file already there...')
	else:
		os.mkdir(charvalue)


	date = time.strftime('%c')
	hour = time.strftime('%x')

	if not comments == '':

		comments = ' ____ ' + comments

	with open(charvalue + '/' + 'infos.txt', "a") as f:
		f.write('\r\n' + date + ' by ' + pc_name + ' : from ' + filevalue + comments)



	write_path = charvalue + '/' + file_type + '.' + extension
	
	doc.save(filename=write_path,warn=False,addtorecent=False)

	print(new_name)

	doc.load(filename=new_name,warn=False)

	print('Master sucessfully created !')
