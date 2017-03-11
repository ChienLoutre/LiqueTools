import maya.cmds as mc
import os
import sys
import maya.OpenMaya as om
import mkfolder
from variables import *
import padding_numbers
import argparse
import utils.get_extension as extension
# Shot Creator

def shot(cam):

	# verifier la sauvegarde avant de faire la creation d'un shot...

	filename = mc.file(q=True, sn=True)
	charvalue = filename.split('/')

	# Verifier que l'on est dans le projet

	if not project_name in charvalue:
		sys.exit('You are not working in the Project !!')

	if not 'seq' in charvalue:
		sys.exit('This is not a sequence...')

	current_seq = charvalue[5]
	shot_path = project_dir + '/prod/seq/' + current_seq + '/shots/'

	print(shot_path + '<= shot_path')

	# get cam_name

	shot_name = cam.split('_')
	shot_name = str(shot_name[-1])

	if os.path.exists(shot_path + shot_name):

		sys.exit('Shot name already existing.')

	os.mkdir(shot_path + shot_name)
	os.mkdir(shot_path + shot_name + '/cloth')
	os.mkdir(shot_path + shot_name + '/export')

	# create FX folder

	os.mkdir(shot_path + shot_name + '/fx')
	os.mkdir(shot_path + shot_name + '/fx/houdini')
	os.mkdir(shot_path + shot_name + '/fx/fur')

	# create Anim folder

	os.mkdir(shot_path + shot_name + '/anim')
	os.mkdir(shot_path + shot_name + '/anim/V000')
	os.mkdir(shot_path + shot_name + '/playblasts')

	# create lookdev folder

	os.mkdir(shot_path + shot_name + '/lookdev')
	os.mkdir(shot_path + shot_name + '/lookdev/guerilla')
	os.mkdir(shot_path + shot_name + '/lookdev/textures')

	# virer les autres cameras

	all_cams = mc.ls('cams')
	all_cams = mc.listRelatives(all_cams, c=True)
	all_cams.remove(cam)

	for each in all_cams:

		mc.delete(each)


	mc.parent(cam, w=True)
	mc.delete('cams')
	mc.rename(cam, 'cam')

	# create display layers for props, sets, building
	sel = mc.ls('props','sets','building')

	# voir si c'est bien utile...
	mc.createDisplayLayer(sel, name='assembly', nr=True)



	mc.file(rename = shot_path + shot_name + '/anim/V000/anim.ma')
	mc.file(save = True, type = 'mayaAscii')




# Sequence Creator

def seq(lo_num = ''):


	if lo_num == '':

		result = mc.promptDialog(
						title='Create a Sequence',
						message='Sequence Number:',
						button=['OK', 'Cancel'],
						defaultButton='OK',
						cancelButton='Cancel',
						dismissString='Cancel')

		if result == 'OK':
				lo_num = mc.promptDialog(query=True, text=True)
		else:

			sys.exit('Layout Creation Aborted !')

	lo_num = int(lo_num)

	if not isinstance( lo_num, ( int, long ) ):
		sys.exit

	retval = os.getcwd()

	print "Working directory is : %s" % retval

	os.chdir(project_path_base)
	retval = os.getcwd()

	print "Working directory changed to : %s" % retval

	project_path = project_path_base + '/' + project_name


	if not os.path.exists(project_path):

		print 'No Project Found !'


	layout_path = project_path + '/prod/seq/'

	layout_name = padding_numbers.padder(lo_num, 5)

	if os.path.exists(layout_path + layout_name):

		print(layout_name + ' already exists !')
		sys.exit('Sequence name already existing.')


	print(layout_name)

	os.mkdir(layout_path + layout_name)

	# create folders

	os.mkdir(layout_path + layout_name + '/layout')
	os.mkdir(layout_path + layout_name + '/layout/V000')

	os.mkdir(layout_path + layout_name + '/playblasts')
	os.mkdir(layout_path + layout_name + '/export')

	# create cloth folder

	os.mkdir(layout_path + layout_name + '/cloth')

	# create lookdev folder

	os.mkdir(layout_path + layout_name + '/lookdev')
	os.mkdir(layout_path + layout_name + '/lookdev/guerilla')
	os.mkdir(layout_path + layout_name + '/lookdev/textures')

	# create shots folder

	os.mkdir(layout_path + layout_name + '/shots')


	print('Sequence ' + str(lo_num) + ' successfully created !')



	mc.file(new=True, f=True)
	mc.textCurves(f= 'Arial|wt:75|sz:100|sl:n|st:100', t= layout_name)
	mc.file(rename = layout_path + layout_name + '/layout/V000/' + 'layout')


	# create groups for assets

	chars_grp = mc.group(em=True, n='chars')
	props_grp = mc.group(em=True, n='props')
	sets_grp = mc.group(em=True, n='sets')
	cam_grp = mc.group(em=True, n='cams')
	building_grp = mc.group(em=True, n='building')

	grps = [chars_grp, props_grp, sets_grp, building_grp,cam_grp]

	for grp in grps:

		mc.setAttr(grp + '.inheritsTransform', 0)
		mc.setAttr(grp + '.tx',lock=True)
		mc.setAttr(grp + '.ty',lock=True)
		mc.setAttr(grp + '.tz',lock=True)
		mc.setAttr(grp + '.rx',lock=True)
		mc.setAttr(grp + '.ry',lock=True)
		mc.setAttr(grp + '.rz',lock=True)
		mc.setAttr(grp + '.sx',lock=True)
		mc.setAttr(grp + '.sy',lock=True)
		mc.setAttr(grp + '.sz',lock=True)


	mc.file(save = True, type = 'mayaAscii')


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

	project_path = project_path_base + '/' + project_name

	asset_path = project_path_base + '/' + project_name + '/prod/assets/' + asset_type
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
			mkfolder.cr_folder(asset_fullpath + '\\mod', 777)
			mkfolder.cr_folder(asset_fullpath + '\\mod\\V000', 777)

			mkfolder.cr_folder(asset_fullpath + '\\rig', 777)
			mkfolder.cr_folder(asset_fullpath + '\\rig\\V000', 777)

			mkfolder.cr_folder(asset_fullpath + '\\zbrush', 777)

			mkfolder.cr_folder(asset_fullpath + '\\export', 777)

			mkfolder.cr_folder(asset_fullpath + '\\lookdev', 777)
			mkfolder.cr_folder(asset_fullpath + '\\lookdev\\guerilla', 777)
			mkfolder.cr_folder(asset_fullpath + '\\lookdev\\mari', 777)
			mkfolder.cr_folder(asset_fullpath + '\\lookdev\\textures', 777)

		else:
			sys.exit('asset name already existing !')


		mc.file(new=True, f=True)
		mc.textCurves(f= 'Arial|wt:75|sz:100|sl:n|st:100', t= asset_name)
		mc.file(rename = asset_fullpath + '\\rig\\V000\\' + 'rig.ma')
		mc.file(save = True, type = 'mayaAscii')

		mc.file(new=True, f=True)
		mc.textCurves(f= 'Arial|wt:75|sz:100|sl:n|st:100', t= asset_name)
		mc.file(rename = asset_fullpath + '\\mod\\V000\\' + 'mod.ma')
		mc.file(save = True, type = 'mayaAscii')
	
	else :
		
		sys.exit('Asset Creation aborted')
		
	om.MGlobal.displayInfo("New Asset " + asset_name + " successfully created !")


def missing_rigs():


	project_path = project_path_base + '/' + project_name
	assets_path = project_path + '/prod/assets/'
	asset_type = os.listdir(assets_path)
	asset_name = []
	asset_list = []
	for each in asset_type:

		asset_path = assets_path + each + '/'
		print(asset_path)
		asset_name.append(asset_path)

	print(asset_name)

	for each in asset_name:

		assets = os.listdir(each)

		for each in assets:

			asset_list.append(each)


	print (asset_list)

	for typ in asset_type:

		print(typ)
		path = assets_path + typ
		for each in os.listdir(path):
		
			state_path = path +'/'+ each
			states = os.listdir(state_path)
			print ('states == > ' + str(state_path))
			if not 'rig' in states:
				print (each + ' has no rig folder')

				go_on = mc.confirmDialog(title='Missing Rig !', message = 'The asset ' + each + ' has no rig folder, create it ?', button =['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No')
				
				if go_on == 'Yes':

					mkfolder.cr_folder(state_path + '\\rig', 777)
					mkfolder.cr_folder(state_path + '\\rig\\V000', 777)

					mc.file(new=True, f=True)
					mc.textCurves(f= 'Arial|wt:75|sz:100|sl:n|st:100', t= each)
					mc.file(rename = state_path + '\\rig\\V000\\' + 'rig')
					mc.file(save = True, type = 'mayaAscii')



def missing_folders():


	project_path = project_path_base + '/' + project_name
	assets_path = project_path + '/prod/assets/'
	asset_type = os.listdir(assets_path)
	asset_name = []
	asset_list = []
	for each in asset_type:

		asset_path = assets_path + each + '/'
		print(asset_path)
		asset_name.append(asset_path)

	print(asset_name)

	for each in asset_name:

		assets = os.listdir(each)

		for each in assets:

			asset_list.append(each)


	print (asset_list)

	for typ in asset_type:

		print(typ)
		path = assets_path + typ
		folders = ['mod','rig','export','lookdev','zbrush']

		for each in os.listdir(path):
		
			state_path = path +'/'+ each
			states = os.listdir(state_path)
			print ('states == > ' + str(state_path))



			missing_folders_count = 0

			for folder in folders:

				if not folder in states:

					missing_folders_count += 1
					print (each + ' has no ' + folder + ' folder')



		#go_on = mc.confirmDialog(title='Missing Folders !', message = 'There are ' + str(missing_folders_count) + ' folders missing in ' + str(len(os.listdir(path))) + ' assets, create them ?', button =['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No')


		#if go_on == 'Yes':

					mkfolder.cr_folder(state_path + '\\' + folder, 777)

					if folder == 'rig':
						mkfolder.cr_folder(state_path + '\\' + folder + '\\V000', 777)

						mc.file(new=True, f=True)
						mc.textCurves(f= 'Arial|wt:75|sz:100|sl:n|st:100', t= each)
						mc.file(rename = state_path + '\\rig\\V000\\' + 'rig')
						mc.file(save = True, type = 'mayaAscii')

					if folder == 'lookdev':

						mkfolder.cr_folder(state_path + '\\' + folder + '\\guerilla', 777)
						mkfolder.cr_folder(state_path + '\\' + folder + '\\mari', 777)
						mkfolder.cr_folder(state_path + '\\' + folder + '\\textures', 777)






def ref(asset = '', nspace=':'):

	project_path = project_path_base + '/' + project_name + '/prod/assets'

	if asset == '':
		sys.exit('Nothing written !')

	asset_type = asset.split(' ')
	print(asset_type)
	for each in asset_type:

		each = each.lower()

	print('lower ?? ' +  str(asset_type))

	asset = asset_type[1]
	asset_state = asset_type[2]

	if not asset_type[0] in ('chars','props','sets'):

		sys.exit('asset type is not good. it is "chars","props" or "sets"')

	if len(asset_type) < 4:

		# lister dossiers pour chercher "master"
		asset_path = os.listdir(project_path + '/' + asset_type[0] + '/' + asset + '/' + asset_state)
		# master trouve ? demander ouverture
		if 'master' in asset_path:

			go_on = mc.confirmDialog(title='Master found for ' + asset, message = 'a Master file has been found for ' + asset + ', reference it ?', button =['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No')
				
			if go_on == 'No':

				sys.exit('Reference aborted')

			asset_type.append('master')
		# master non trouve? demander si reference de version.
		# dans l'ideal faire une fenetre avec liste deroulante


		else:

			result = mc.promptDialog(
				title='No Master file',
				message='No Master file found. Reference a version instead ?',
				button=['OK', 'Cancel'],
				defaultButton='OK',
				cancelButton='Cancel',
				dismissString='Cancel')

			if result == 'OK':
				txt = mc.promptDialog(query=True, text=True)
				asset_type.append(txt)
			else:
				sys.exit('Reference aborted')


	print(asset_type)
	asset_version = asset_type[3]
	asset_type = asset_type[0]

	asset_path = project_path + '/' + asset_type + '/' + asset + '/' + asset_state + '/' + asset_version
	print(asset_path)
	get_assets = os.listdir(asset_path)
	print('listdir => ' + str(get_assets))
	for each in get_assets:
		print(each)
		if each == 'thumbnail.png':
			get_assets.remove(each)
		if each == 'infos.txt':
			get_assets.remove(each)
		if each == 'Thumbs.db':
			get_assets.remove(each)
	print('new get_assets => ' + str(get_assets))
	asset_ext = get_assets[0]
	asset_name, asset_ext = extension.get_ext(asset_ext)

	print('test asset name et ext ===>   ' + asset_name + '     ' + asset_ext)

	asset_path = asset_path + '/' + asset_name + '.' + asset_ext

	mc.file(asset_path, r=True, mergeNamespacesOnClash=True, options='v=0', namespace=nspace)
	#mc.file(asset_path, edit=True, mergeNamespacesOnClash=True, namespace=asset + '__')


def thumbnail():

	filename = mc.file(q=True, sn=True)
	charvalue = filename.split('/')

	if not project_name in charvalue:

		sys.exit('You are not working in the Project !!')

	charvalue.pop(-1)


	filename = '/'.join(charvalue)
	filename = filename + '/thumbnail'
	print(filename)

	mc.playblast(format='image',
				clearCache=True,
				viewer=True,
				showOrnaments=False,
				fp=0,
				percent=100,
				compression='png',
				quality=70,
				frame=1,
				widthHeight=[100,100],
				filename=filename)

	filename = filename + '.0.png'
	charvalue = filename.split('/')
	new_name = charvalue[-1]
	new_name = new_name.split('.')
	new_name.pop(1)
	new_name = '.'.join(new_name)

	charvalue.pop(-1)

	check_if_exists = os.listdir('/'.join(charvalue))

	charvalue.append(new_name)
	charvalue = '/'.join(charvalue)

	if 'thumbnail.png' in check_if_exists:
		os.remove(charvalue)

	os.rename(filename, charvalue)

def shot_camera(shot_num):


	cam_path = project_dir + '/utils/camera/camera.mb'

	shot_num = padding_numbers.padder(int(shot_num),3)

	new_cam = mc.file(cam_path, i=True)
	new_cam = mc.rename('shot_num', 'shot_' + shot_num)

	def lockHideAttr(obj,attrArray,lock,hide):
		for a in attrArray:
			mc.setAttr(obj + '.' + a, k=hide,l=lock)

	text_curves = mc.textCurves(n='sh_' + shot_num, ch=0, f='Arial|wt:75|sz:8|sl:n|st:100', t='SH_' + shot_num)
	text_curves = mc.rename(text_curves, 'sh_' + shot_num + '__txt')
	mc.xform(text_curves, ws=True, ro=[0,180,0], t= [-0.2,1,0])

	mc.parent(text_curves, new_cam)
	lockHideAttr(text_curves,['tx','ty','tz','rx','ry','rz','sx','sy','sz'],True,False)

	try:
		mc.parent(new_cam, 'cams')
	except:
		sys.exit('No folder <cams> in the scene !!')

