import os
import sys
import mkfolder
from variables import *
import padding_numbers
import maya.cmds as mc

# Shot Creator

def create_shot(sh_num = ''):


	if sh_num = '':

		result = mc.promptDialog(
						title='Create a shot',
						message='Shot Number:',
						button=['OK', 'Cancel'],
						defaultButton='OK',
						cancelButton='Cancel',
						dismissString='Cancel')

		if result == 'OK':
				sh_num = mc.promptDialog(query=True, text=True)
		else:

			sys.exit('Shot Creation Aborted !')

	sh_num = int(sh_num)

	if not isinstance( sh_num, ( int, long ) ):
		sys.exit

	retval = os.getcwd()

	print "Working directory is : %s" % retval

	os.chdir(project_path_base)
	retval = os.getcwd()

	print "Working directory changed to : %s" % retval

	project_path = project_path_base + '/' + project_name


	if not os.path.exists(project_path):

	    print 'No Project Found !'
	    sys.exit('FUCK YOUUUUUUU')


	shot_path = project_path + '/02_prod/shots/'

	shot_name = 'sh_' + padding_numbers.padder(sh_num, 5)

	if os.path.exists(shot_path + shot_name):

		print(shot_name + ' already exists !')
		sys.exit('Shot name already existing.')


	print(shot_name)

	os.mkdir(shot_path + shot_name)

	# create FX folder

	os.mkdir(shot_path + shot_name + '/fx')

	os.mkdir(shot_path + shot_name + '/fx/houdini')
	os.mkdir(shot_path + shot_name + '/fx/fur')
	os.mkdir(shot_path + shot_name + '/fx/cloth')

	# create Anim folder

	os.mkdir(shot_path + shot_name + '/anim')

	os.mkdir(shot_path + shot_name + '/anim/playblasts')
	os.mkdir(shot_path + shot_name + '/anim/versions')
	# create guerilla folder

	os.mkdir(shot_path + shot_name + '/guerilla')

	print('Shot number ' + str(sh_num) + ' successfully created !')