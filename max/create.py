import MaxPlus as mc
import time
import os
import sys
from variables import *
import padding_numbers
import utils.get_extension as ext
reload(ext)
import mkfolder
import argparse
import pymxs
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#           Create Asset for MAX
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

mx = pymxs.runtime




def asset(asset_name, asset_type):
	''' Creates an asset in the project.
		creates_asset() takes two arguments :
			asset_name = string type (ex : 'Gilles')
			asset_type = string type but one of these (unless you added more) : 'Chars','Props','Sets'
				
		Write the function as : create_asset(asset_name, asset_type)
		( ex : create_asset('Gilles', 'Chars') will create an asset named Gilles in the 'Chars' folder of your project. )
	'''
	
	# ASSET CREATOR
	# asset_name = 'gilles'
	# asset_type = 'chars'
	# asset_state = 'modeling'

	asset_name = asset_name.lower()

	if asset_type == '':

		sys.exit('Pas de chemin existant !')

	if asset_name == '':

		sys.exit('Give your asset a name !')

	project_path = project_path_base + '\\' + project_name

	asset_path = project_path_base + '\\' + project_name + '\\prod\\assets\\' + asset_type
	asset_fullpath = asset_path + '\\' + asset_name 

	asset_path = asset_path.replace('/', '\\')
	asset_fullpath = asset_fullpath.replace('/', '\\')

	retval = os.getcwd()
	os.chdir(asset_path)


	retval = os.getcwd()
	print "Working directory changed to : %s" % retval


	print(asset_fullpath)

# Fenetre de dialogue prevenant si on a bien sauve la scene

	go_on = mx.queryBox("Your current file won't be saved, are you sure ?", title='Creating new asset : ' + asset_name)

	print(go_on)

	if go_on == True:

		if not os.path.exists(asset_fullpath):

			mkfolder.cr_folder(asset_fullpath, 777)
			mkfolder.cr_folder(asset_fullpath + '\\mod', 777)
			mkfolder.cr_folder(asset_fullpath + '\\mod\\V000', 777)


		else:
			print('asset name already existing !')
			sys.exit('asset name already existing !')

		charvalue = asset_fullpath + '\\mod\\V000\\' + 'mod.max' 
		mc.FileManager.Reset()

		# mc.textCurves(f= 'Arial|wt:75|sz:100|sl:n|st:100', t= asset_name)
		mx.text(text=asset_name)
		mc.FileManager.Save(charvalue)
	
	else :
		print('Asset Creation aborted')
		sys.exit('Asset Creation aborted')
