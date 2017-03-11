import maya.cmds as mc
import os
import sys
import maya.OpenMaya as om
import mkfolder
from variables import *
import padding_numbers
import argparse


def create_asset(asset_name, asset_type):
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

	project_path = project_path_base + '/' + project_name

	asset_path = project_path_base + '/' + project_name + '/02_prod/assets/' + asset_type
	asset_fullpath = asset_path + '/' + asset_name 

	asset_path = asset_path.replace('/', '\\')
	asset_fullpath = asset_fullpath.replace('/', '\\')

	retval = os.getcwd()
	os.chdir(asset_path)


	retval = os.getcwd()
	print "Working directory changed to : %s" % retval



# Fenetre de dialogue prevenant si on a bien sauve la scene

	go_on = mc.confirmDialog(title='Creating new asset : ' + asset_name , message = "Your current file won't be saved, are you sure ?", button =['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No')

	if go_on == 'Yes':

		if not os.path.exists(asset_fullpath):

			mkfolder.cr_folder(asset_fullpath, 777)
			mkfolder.cr_folder(asset_fullpath + '\\versions', 777)
		else:
			sys.exit('asset name already existing !')

		asset_fullpath = asset_fullpath + '/versions'


		mc.file(new=True, f=True)
		mc.textCurves(f= 'Arial|wt:75|sz:100|sl:n|st:100', t= asset_name)
		mc.file(rename = asset_fullpath + '\\' + asset_name + '_' + padding_numbers.padder(1, pad))
		mc.file(save = True, type = 'mayaAscii')
	
	else :
		
		sys.exit('Asset Creation aborted')
		
	om.MGlobal.displayInfo("New Asset " + asset_name + " successfully created !")