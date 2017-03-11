print('---HELLO DOGGIE----')
print('-------------------')
print('ALEMBIC RIG CLEANER')
print('-------------------')
print('-------------------')

import os
from variables import *
import time
import sys
import utils.get_extension as gx

# get infos from text file

try:
	print('Reading File for Path...')
	obj_path = project_dir + '\\utils\\export\\clean_abc'

	file_path = open(obj_path + '.txt', 'r')
	abc_path = file_path.read()
	file_path.close()

except ValueError:

	print('No file to read a text from.')
	sys.exit('GOODBYE DOGGIE')

print('These are the ABC files found :')
print(' ')

for each in os.listdir(abc_path):
	file, ext = gx.get_ext(each)
	if ext == 'abc':
		print(each)


try:
	abc_path = abc_path.split(';')
except IndexError:
	abc_path = [abc_path]




import maya.standalone
maya.standalone.initialize()
maya.standalone.initialize('Python')

import maya.cmds as mc
import pymel.core as pmc
import utils.save as save


print('Loading Marilla plugins...')

import marilla.defMenus as mdefMenus
import marilla.marillaUi as mUi
import marilla.maUtils as mUtils
import marilla.guegueTags as mTags

# load ABCimport plugin
print('Loading Abc import...')

mc.loadPlugin('AbcImport.mll')

print('Abc Import loaded.')



print(abc_path)

# loop for files !
for seq in abc_path:
	print(seq)

	try:
		print('Reading File for frames...')
		print(' ')
		frames_path = open(seq + '\\frames.txt', 'r')
		all_frames = frames_path.read()
		frames_path.close()

		all_frames = all_frames.split(';')
		st_fr = all_frames[0]
		end_fr = all_frames[-1]

	except ValueError:

		print('No file to read a text from.')
		sys.exit('GOODBYE DOGGIE')



	get_abc = os.listdir(seq)

	abc_names = ['chars.abc','props.abc','sets.abc','cams.abc','building.abc']

	for each in get_abc:
		if each in abc_names:

	# import alembic
			mc.file(new=True, f=True)

			abc_test = seq + each
			mc.file(abc_test, i=True, type='Alembic', pr=True, namespace=':', mergeNamespacesOnClash=True, ra=True)
			print('-------------------')
			print(each + ' opened.')
			
			try:
				mc.select('*|rig')
				rigs = mc.ls(sl=True)
				mc.delete(rigs)

				abc_name = each.split('.')
				abc_name = abc_name[0]
				abc_name = pmc.ls(abc_name)

				# create alembic again
				old_name = seq + each
				new_name = seq + 'temp__' + each
				mUtils.abc_export(framemode='startend',qstart=st_fr,qend=end_fr,preroll=False,path=new_name ,preframe=0,nodes=abc_name)

				mc.file(new=True, f=True)
				os.remove(old_name)
				os.rename(new_name, old_name)
				print(each + 'has been cleaned, no more rig folders remaining !')
				print('-------------------')

			except ValueError:
				print('No rig folder in this Abc.')
				print('-------------------')

		else:
			print(each + ' is not an alembic, or a weird one.')
			print('-------------------')

os.remove(obj_path + '.txt')


print('-------------------------')
print('-------------------------')
print('THANK YOU, GOODBYE DOGGIE')
print('-------------------------')
print('-------------------------')

raise SystemExit


# Search rig groups

# Delete rig groups

# Save alembic (replace)
