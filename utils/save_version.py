import maya.cmds as mc
import os
import sys
from variables import *
import padding_numbers

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


	print(charvalue)
	print(file_path)
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

