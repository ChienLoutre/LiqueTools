import maya.cmds as mc
import os
import sys
from variables import *
import utils.create as create
reload(create)
import utils.save as save
reload(save)
import utils.export_to_guerilla as etg
reload(etg)
import utils.check as check
reload(check)
from functools import partial
import utils.get_extension as get_ext
reload(get_ext)
import utils.autorig as autorig
reload(autorig)


# module marilla de Colin Laubry => export de tags, alembic, ect pour Guerilla
import marilla.defMenus as mdefMenus
reload(mdefMenus)
import marilla.marillaUi as mUi
reload(mUi)
import marilla.maUtils as mUtils
reload(mUtils)
import marilla.guegueTags as mTags
reload(mTags)


def UI():

	w = 400
	h = 670

	# check to see if the window exists
	if mc.window('projectUI', exists = True):
		mc.deleteUI('projectUI')

	if mc.dockControl(manager_name, exists = True):
		mc.deleteUI(manager_name)


	# create the window

	window = mc.window('projectUI', title = project_name.capitalize()  + ' Manager', w = w, mnb = False, mxb = False, sizeable = False, rtf=True)

	# create a main layout
	mainLayout = mc.columnLayout(w = w, adj=True)

	# banner image
	# check internalVar
	imagePath = project_dir + '/utils/icons/project_banner.png'
	mc.image(w = w, h = 100, image = imagePath)
	
	mc.separator(h = 10, vis = False)

	mc.columnLayout(w = w, adj = True)


	# ------- SAVE BUTTONS ----------

	mc.columnLayout(w = w, adj= True)

	mc.text(label = '  Commentaries for Master file : ', align = 'left', w = w, h = 26)
	cr_field = mc.textField('master_comment', tx = '')

	mc.separator(h = 10, vis = True)

	mc.rowColumnLayout(nr = 1)

	mc.separator(w = w*0.05, vis = False)

	mc.button(label='Save Version', h = 30, c = save_version, w = w*0.4, bgc = [1,0.75,0.45])

	mc.separator(w = w*0.05, vis = False)

	mc.button(label='Save Master', h = 30, c = save_master, w = w*0.4, bgc = [0,0.55,0.2])

	mc.setParent( '..' )

	mc.button(label='THE MIGHTY FOLDER OPENER', h = 30, c = open_folder, w = w*0.8, bgc = [0.8,0.8,0.8])

	mc.setParent( '..' )
	mc.setParent( '..' )
	mc.setParent( '..' )
	mc.setParent( '..' )

	scroller = mc.scrollLayout('scroll_bar', horizontalScrollBarThickness=16, verticalScrollBarThickness=16, h=h, w = w + 16)
	mc.columnLayout(w = w, adj= True)

	# ------------  THINGS CREATOR ---------------
			# --------> Create Asset
			# --------> Create Layout
			# --------> Create Shot




	mc.frameLayout( label='THINGS CREATOR', cll = True, bgc = [0,0,0], cl=True, cc= size_window)
	mc.columnLayout(w = w, adj= True)




		# ------------ ASSET CREATOR ---------------


	mc.frameLayout( label='Create Asset', cll = True, cl=True, cc= size_window)
	mc.columnLayout(w = w, adj= True)

	mc.text(label = '  Write a name (ex : roger )', align = 'left', w = w, h = 26)

	mc.separator(h = 20, vis = False)

	cr_field = mc.textField('cr_assetTextField', tx = '')

	mc.separator(h = 10, vis = False)
	cr_typeOptionMenu = mc.optionMenu('cr_typeOptionMenu', label = 'Choose Asset type :    ', cc = asset_populateFiles, w = w)
	
	# populate  the assets option menu
	asset_populateTypes('cr')

	# create the create_asset button
	mc.separator(h = 10, vis = False)
	mc.button(label='Create Asset', h = 30, c = cr_asset, w = w)

	mc.setParent( '..' )
	mc.setParent( '..' )


		# ------------ LAYOUT CREATOR ---------------


	mc.frameLayout( label='Create Sequence', cll = True, cl=True, cc= size_window)
	mc.columnLayout(w = w, adj= True)

	mc.text(label = '  Type a number (ex :  100   <== sequence 1, is 100, sequence 1.1 is 110...)', align = 'left', w = w, h = 40)

	mc.separator(h = 20, vis = False)

	cr_field = mc.textField('cr_layoutTextField', tx = '')

	# create the create_asset button
	mc.separator(h = 10, vis = False)
	mc.button(label='Create Layout', h = 30, c = cr_layout, w = w)

	mc.setParent( '..' )
	mc.setParent( '..' )



		# ------------ SHOT CREATOR ---------------


	mc.frameLayout( label='Create Shot', cll = True, cl=True, cc= size_window)
	mc.columnLayout(w = w, adj= True)

	mc.text(label = '  Type a number (ex :  100   <== shot 1, is 100, shot 1.1 is 110...)', align = 'left', w = w, h = 26)

	mc.separator(h = 20, vis = False)

	cr_field = mc.textField('cr_shotTextField', tx = '')

	# create the create_asset button
	mc.separator(h = 10, vis = False)
	mc.button(label='Create Shot', h = 30, c = cr_shot, w = w)

	mc.setParent( '..' )
	mc.setParent( '..' )


	mc.setParent( '..' )
	mc.setParent( '..' )
	mc.setParent( '..' )


	# ------------  THINGS OPENER ---------------
			# --------> Open Asset
			# --------> Open Layout
			# --------> Open Shot


	mc.frameLayout( label='THINGS OPENER', cll = True, bgc = [0.13,0.13,0.13], cl=True, cc= size_window)
	mc.columnLayout(w = w, adj= True)




	# ------------ ASSET OPEN ---------------


	mc.frameLayout( label='Open Asset', cll = True, cl=True, cc= size_window)

	# create assets type option menu
	mc.separator(h = 10, vis = False)
	op_typeOptionMenu = mc.optionMenu('op_typeOptionMenu', label = 'Asset Type :    ', cc = asset_populateFiles, w = w)

	# populate  the assets option menu
	asset_populateTypes('op')

	# create asset files option menu
	mc.separator(h = 10, vis = False)
	fileOptionMenu = mc.optionMenu('fileOptionMenu', label = 'File : ', w = w, cc = asset_populateState)

	# populate files
	asset_populateFiles()


	# create asset state option menu
	mc.separator(h = 10, vis = False)
	fileOptionMenu = mc.optionMenu('stateOptionMenu', label = 'State : ', w = w, cc = asset_populateVersions)

	# populate state
	asset_populateState()


	# create asset versions option menu
	mc.separator(h = 10, vis = False)
	fileOptionMenu = mc.optionMenu('versionOptionMenu', label = 'Version : ', w = w, cc= asset_populateImage)

	# populate versions
	asset_populateVersions()

	mc.rowColumnLayout(nr=1)

	imagePath = project_dir + '/utils/icons/no_thumbnail.png'
	mc.image('thumbnail', w = 100, h = 100, image = imagePath, bgc=[0,0,0])

	# create the open_asset button
	mc.separator(h = 10, w=10, vis = False)
	mc.button(label='Open Asset', h = 30, w=280, c = open_asset, bgc = [1,0.73,0])

	mc.setParent( '..' )

	mc.text(label = '    ', align = 'left', w = w, h = 8)

	mc.setParent( '..' )



	# ------------ LAYOUT OPEN ---------------


	mc.frameLayout( label='Open Layout', cll = True, cl=True, cc= layout_refresh)

	# create layout number option menu
	mc.separator(h = 10, vis = False)
	lo_numOptionMenu = mc.optionMenu('lo_numOptionMenu', label = 'Sequence Number :    ', cc=layout_populateVersions, w = w)

	# populate  the layout option menu
	
	layout_populateNumber()

	# create layout versions option menu
	mc.separator(h = 10, vis = False)
	lo_versionOptionMenu = mc.optionMenu('lo_versionOptionMenu', label = 'Version : ', w = w)

	# populate versions
	layout_populateVersions()

	# create the open_layout button
	mc.separator(h = 10, vis = False)
	mc.button(label='Open Layout', h = 30, c = open_layout, w = w, bgc = [1,0.73,0])


	mc.setParent( '..' )


	# ------------ SHOT OPEN ---------------

	mc.setParent( '..' )
	mc.setParent( '..' )


	# ------- REFERENCE IMPORTER ----------

	mc.frameLayout( label='REFERENCES', cll = True, cl=True, bgc=[0.13,0.35,0.5], cc= size_window)
	mc.text(label = '    ', align = 'left', w = w, h = 10)
	mc.text(label = '  Import a Reference : ', align = 'left', w = w, h = 10)
	mc.text(label = '  syntax :  "<chars/props/sets> <asset_name> <mod/rig> <master/version>"', align = 'left', w = w, h = 10)
	mc.text(label = '  do not write the <> !', align = 'left', w = w, h = 10, bgc=[1,0,0])

	mc.rowColumnLayout(nr = 1)
	mc.text(label = 'Namespace : ', align = 'left', w = 70, h = 10)
	mc.separator(w = w*0.05, vis = False)

	namespace_field = mc.textField('namespace_ref', tx = '', w = 200)

	mc.setParent( '..' )


	cr_field = mc.textField('ref_import', tx = '')

	mc.rowColumnLayout(nr = 1)
	mc.separator(w = w*0.05, vis = False)

	mc.button(label='Reference it !', h = 30, c = ref_import, w = w*0.4, bgc = [0.50,0.90,0.70])
	mc.separator(w = w*0.05, vis = False)

	mc.button(label='Duplicate Ref !', h = 30, c = ref_duplicate, w = w*0.4, bgc = [0,0.30,0.75])
	mc.separator(w = w*0.05, vis = False)


	# ------- RENDER / GUERILLA THINGS ----------

	mc.setParent( '..' )
	mc.setParent( '..' )


	mc.frameLayout( label='GUERILLA OPTIONS', cll = True, bgc = [0.36,0.18,0.18], cl=True, cc= size_window)
	mc.columnLayout(w = w, adj= True)

	mc.separator(h = 10, vis = True)

	mc.separator(h = 50, vis = False)


	mc.rowColumnLayout(nc=1)
	

	mc.text(label = 'Bientot, sous vos yeux ebahis, lexport pour les SEQUENCES !!!', align = 'center', w = w, h = 20)

	mc.rowColumnLayout(nr = 1)
	mc.separator(w = w*0.05, vis = False)


	mc.button(label='Tag Objects', c = tag_objects, h = 30, w = w*0.4, bgc = [0.97,0.45,0.65])
	mc.separator(w = w*0.05, vis = False)
	mc.button(label='AutoTag Selection', h = 30, c = autotag_selection, w = w*0.4, bgc = [0.90,0.35,0.55], ann='Selectionner uniquement la geometrie, et pas les groupes.' )

	mc.setParent( '..' )
	mc.separator(h = 10, vis = False)
	mc.rowColumnLayout(nr=1)

	mc.separator(w = w*0.05, vis = False)
	mc.button(label='Asset Group Builder', c=asset_group_builder,h = 30, w = w*0.4, bgc = [0.85,0.25,0.50], ann='Cree un groupe avec le nom de lasset, qui englobe toute la geometrie et les groupes, POUR ASSETS SEULEMENT')
	mc.separator(w = w*0.05,  vis = False)
	mc.button(label='Export Alembic', h = 30, c = g_asset_export, w = w*0.4, bgc = [0.80,0.15,0.45])



	mc.separator(h = 10, vis = True)
	mc.setParent( '..' )
	mc.separator(h = 10, vis = True)

	mc.text(label = "If the options above are set, you are ready to go.", align = 'center', w = w, h = 20, bgc=[0.7,0,0])
	mc.text(label = "If you are NOT SURE, ask your TD. He knows the answer.", align = 'center', w = w, h = 20, bgc=[0.7,0,0])
	mc.button(label='Build Guerilla Scene', h = 30, c = build_guerilla_scene, w = w*0.5, bgc=[1,0,0])

	mc.separator(w = w*0.05, vis = False)

	mc.setParent( '..' )
	mc.setParent( '..' )

	mc.setParent( '..' )


	# ------- DEV OPTIONS ----------+ 



	mc.frameLayout( label='TD AND RIG', cll = True, bgc = [0.2,0.5,0.2], cl=True, cc= size_window, fn='boldLabelFont')

	# ------- TEXTUAL OPENER ----------

	mc.frameLayout( label='TEXTUAL OPENER', cll = True, cl=True, bgc=[0.20,0.20,0.20], cc= size_window, w=w*0.8)
	mc.text(label = '    ', align = 'left', w = w, h = 10)
	mc.text(label = '  Open a file in text, enter fullpath (extension included)', align = 'left', w = w, h = 10)
	mc.text(label = '  do not write the <> !', align = 'left', w = w, h = 10, bgc=[1,0,0])

	cr_field = mc.textField('textual_open', tx = '')

	mc.separator(w = w*0.05, vis = False)

	mc.button(label='Open a file !', h = 30, c = textual_open, w = w*0.4, bgc = [0.50,0.90,0.70])
	mc.separator(w = w*0.05, vis = False)

	mc.setParent( '..' )

	# ------- RIG OPTIONS ----------

	mc.columnLayout(w = w, adj= True)
	mc.text(label = '    ', align = 'left', w = w, h = 20)

	mc.rowColumnLayout(nr = 1)

	mc.rowColumnLayout(nc = 1)

	mc.separator(w = w*0.4, vis = False)
	mc.button(label='Zero Out', h = 30, c = wip, w = w*0.5)
	mc.separator(w = w*0.05, vis = False)
	mc.button(label='Half Bone', h = 30, c = half_bone, w = w*0.5)

	mc.setParent( '..' )

	mc.rowColumnLayout(nc = 1)

	mc.separator(w = w*0.05, vis = False)
	cr_field = mc.textField('nb_joints', tx = '')
	mc.separator(w = w*0.05,  vis = False)
	mc.button(label='Build Deform Chain', c=build_deform_chain, h = 30, w = w*0.5)


	mc.setParent( '..' )
	mc.setParent( '..' )

	mc.setParent( '..' )


	# ------- CHECKING OPTIONS ----------



	mc.columnLayout(w = w, adj= True)
	mc.text(label = '    ', align = 'left', w = w, h = 20)

	mc.rowColumnLayout(nr = 1)

	mc.rowColumnLayout(nc = 1)

	mc.separator(w = w*0.4, vis = False)
	mc.button(label='Check Missing Rigs', h = 30, c = check_rigs, w = w*0.5)
	mc.separator(w = w*0.05, vis = False)
	mc.button(label='Check Ngons and Triangles', h = 30, c = check_ngons, w = w*0.5)

	mc.setParent( '..' )

	mc.rowColumnLayout(nc = 1)

	mc.separator(w = w*0.05, vis = False)
	mc.button(label='Check History', h = 30, c = check_history, w = w*0.5)
	mc.separator(w = w*0.05,  vis = False)
	mc.button(label='Check Ta Mere', h = 30, w = w*0.5)


	mc.setParent( '..' )
	mc.setParent( '..' )

	mc.text(label = '    ', align = 'left', w = w, h = 5)

	mc.text(label = 'QUE POUR MAURIN. ON TOUCHE PAS A CE BOUTON !!!!1', align = 'center', w = w, h = 20, bgc=[0.7,0,0])

	mc.button(label='Master Rig !!!', h = 30, c = master_rig, w = w*0.5, bgc=[1,0,0])



	mc.setParent( '..' )
	mc.setParent( '..' )



	# ------- FILM MAKING OPTIONS ----------

	mc.frameLayout( label='FILM MAKING', cll = True, bgc = [0.6,0.6,0.1], cl=True, cc= size_window, fn='boldLabelFont')

	mc.text(label = 'Options pour les Realisateurs : Cameras, creation de sequences, ect...', align = 'center', w = w, h = 20)
	mc.rowColumnLayout(nr = 1)
	mc.separator(w = w*0.05, vis = False)


	mc.button(label='Import Camera', c = import_cam, h = 30, w = w*0.4, bgc = [0.8,0.4,0.0])
	mc.separator(w = w*0.05, vis = False)
	mc.rowColumnLayout(nr = 1, w = w*0.4)
	mc.text(label = 'Shot Number : ', h = 20, align='left')
	cam_shot_number = mc.textField('cam_sh_num', tx = '')
	mc.setParent( '..' )

	mc.setParent( '..' )

	mc.separator(w = w*0.05, vis = True)

	mc.rowColumnLayout(nr=1)

	mc.separator(w = w*0.05, vis = False)
	mc.button(label='Wip', c=wip,h = 30, w = w*0.4, bgc = [0.8,0.4,0.0], ann='Cree un groupe avec le nom de lasset, qui englobe toute la geometrie et les groupes, POUR ASSETS SEULEMENT')
	mc.separator(w = w*0.05,  vis = False)
	mc.button(label='Create Shot', h = 30, c = create_shot, w = w*0.4, bgc = [0.9,0.7,0.3])

	# ------- SAVE BUTTONS ----------
	mc.setParent( '..' )
	mc.setParent( '..' )
	mc.setParent( '..' )
	mc.setParent( '..' )

	# ------- SAVE BUTTONS ----------

	mc.columnLayout(w = w, adj= True)

	# show the window

	allowedAreas = ['right', 'left']
	mc.dockControl(manager_name, area='right', content=window, allowedArea=allowedAreas, dpc=size_window, io=False, h=h, r=True)
	

	size_window()
	mc.warning('The ' + manager_name + ' has been opened.')
	#mc.showWindow(window)
# ------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------ FUNCTIONS DEFINITIONS -------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------


	# ------> ASSET SEARCH

def asset_populateTypes(cr_op):

	projectPath = project_dir + '/prod/assets/'
	projects = os.listdir(projectPath)

	for project in projects:
		mc.menuItem(label = project, parent = cr_op + '_typeOptionMenu')


# populate NAME of assets

def asset_populateFiles(*args):

	menuItems = mc.optionMenu('fileOptionMenu', q = True, itemListLong = True)

	if menuItems != None:

		for item in menuItems:
			mc.deleteUI(item)


	selectedType = mc.optionMenu('op_typeOptionMenu', q = True, v = True)
	projectPath = project_dir + '/prod/assets/' + selectedType + '/'

	files = os.listdir(projectPath)

	characters = []

	for file in files:
		mc.menuItem(label = file, parent = 'fileOptionMenu')


# populate STATE of assets (mod, rig...)


def asset_populateState(*args):

	menuItems = mc.optionMenu('stateOptionMenu', q = True, itemListLong = True)

	if menuItems != None:

		for item in menuItems:
			mc.deleteUI(item)


	selectedType = mc.optionMenu('op_typeOptionMenu', q = True, v = True)
	selectedAsset = mc.optionMenu('fileOptionMenu', q = True, v = True)

	if selectedAsset != None:

		projectPath = project_dir + '/prod/assets/' + selectedType + '/' + selectedAsset

		files = os.listdir(projectPath)
	
	else:
		
		files = []

	for file in files:
		if (file == 'export') or (file == 'lookdev') or (file == 'zbrush'):
			pass
		else:
			mc.menuItem(label = file, parent = 'stateOptionMenu')


# populate VERSION of asset

def asset_populateVersions(*args):

	menuItems = mc.optionMenu('versionOptionMenu', q = True, itemListLong = True)

	if menuItems != None:
		for item in menuItems:
			mc.deleteUI(item)


	selectedType = mc.optionMenu('op_typeOptionMenu', q = True, v = True)
	selectedAsset = mc.optionMenu('fileOptionMenu', q = True, v = True)
	selectedState = mc.optionMenu('stateOptionMenu', q = True, v = True)



	if selectedAsset != None: 

		projectPath = project_dir + '/prod/assets/' + selectedType + '/' + selectedAsset + '/' + selectedState

		files = os.listdir(projectPath)

	else:

		files = []

	for file in files:
		mc.menuItem(label = file, parent = 'versionOptionMenu')


def asset_populateImage(valeur):

	selectedType = mc.optionMenu('op_typeOptionMenu', q = True, v = True)
	selectedAsset = mc.optionMenu('fileOptionMenu', q = True, v = True)
	selectedState = mc.optionMenu('stateOptionMenu', q = True, v = True)
	selectedVersion = valeur

	if selectedAsset != None:

		projectPath = project_dir + '/prod/assets/' + selectedType + '/' + selectedAsset + '/' + selectedState + '/' + selectedVersion

		files = os.listdir(projectPath)

		if 'thumbnail.png' not in files:

			imagePath = project_dir + '/utils/icons/no_thumbnail.png'

		else:

			imagePath = projectPath + '/thumbnail.png'
	else:

		imagePath = project_dir + '/utils/icons/no_thumbnail.png'

	mc.image('thumbnail', edit
		=True, image = imagePath)




	# ------> LAYOUT SEARCH

def layout_populateNumber(*args):

	menuItems = mc.optionMenu('lo_numOptionMenu', q = True, itemListLong = True)
	selectedNumber = mc.optionMenu('lo_numOptionMenu', q = True, v = True)


	if menuItems != None:
		for item in menuItems:
			mc.deleteUI(item)


	projectPath = project_dir + '/prod/seq/'
	projects = os.listdir(projectPath)

	for project in projects:
		mc.menuItem(label = project, parent = 'lo_numOptionMenu')




def layout_populateVersions(*args):


	menuItems = mc.optionMenu('lo_versionOptionMenu', q = True, itemListLong = True)

	if menuItems != None:
		for item in menuItems:
			mc.deleteUI(item)

	selectedLayout = mc.optionMenu('lo_numOptionMenu', q = True, v = True)
	
	if selectedLayout != None:

		projectPath = project_dir + '/prod/seq/' + selectedLayout + '/layout/'
		files = os.listdir(projectPath)

		if 'master' in files:
			files.remove('master')


	else:

		files = []

	for file in files:
		mc.menuItem(label = file, parent = 'lo_versionOptionMenu')



# ----------------------------



def open_asset(*args):

	selectedType = mc.optionMenu('op_typeOptionMenu', q = True, v = True)
	selectedAsset = mc.optionMenu('fileOptionMenu', q = True, v = True)
	selectedState = mc.optionMenu('stateOptionMenu', q = True, v = True)
	selectedVersion = mc.optionMenu('versionOptionMenu', q = True, v = True)

	extension = '.ma'

	if selectedVersion == 'master':

		extension = '.mb'

	projectPath = project_dir + '/prod/assets/' + selectedType + '/' + selectedAsset + '/' + selectedState + '/' + selectedVersion + '/'
	selectedAssetVersion = projectPath + selectedState + extension

	go_on = mc.confirmDialog(title='Opening asset : ' + selectedAsset + ' in ' + selectedState , message = "Your current file won't be saved, are you sure ?", button =['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No')

	if go_on != 'Yes':

		
		sys.exit('Opening of asset ' + selectedVersion + ' aborted.')

	print(selectedAssetVersion + ' is opening...')

	mc.file(selectedAssetVersion, open=True, f = True)


def open_layout(*args):

	selectedNumber = mc.optionMenu('lo_numOptionMenu', q = True, v = True)
	selectedVersion = mc.optionMenu('lo_versionOptionMenu', q = True, v = True)

	projectPath = project_dir + '/prod/seq/' + selectedNumber + '/layout/' + selectedVersion
	selectedLayoutVersion = projectPath + '/layout.ma'

	go_on = mc.confirmDialog(title='Opening layout : ' + selectedNumber + ' version ' + selectedVersion , message = "Your current file won't be saved, are you sure ?", button =['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No')

	if go_on != 'Yes':

		
		sys.exit('Opening of asset ' + selectedVersion + ' aborted.')

	print(selectedLayoutVersion + ' is opening...')

	mc.file(selectedLayoutVersion, open=True, f = True)

	print(selectedLayoutVersion + ' opened successfully !')


def open_shot(*args):

	print('Work In Progress')



def cr_asset(*args):

	asset_name = mc.textField('cr_assetTextField', q=True, tx=True)
	asset_name = asset_name.lower()
	asset_type = mc.optionMenu('cr_typeOptionMenu', q = True, v = True)

	create.asset(asset_name, asset_type)


def cr_layout(*args):

	layout_name = mc.textField('cr_layoutTextField', q=True, tx=True)
	layout_name = layout_name.lower()
	layout_name = layout_name.split(',')
	lo_num = layout_name[0]
	lo_name = layout_name[-1]

	create.seq(lo_num)



def cr_shot(*args):

	shot_name = mc.textField('cr_shotTextField', q=True, tx=True)
	shot_name = shot_name.lower()

	create.shot(shot_name)



def layout_refresh(*args):

	layout_populateNumber()
	layout_populateVersions()
	size_window()

def size_window():

	not_docked = mc.dockControl('Liquemanager', q=True, floating=True)

	if not_docked == True:

		mc.window('projectUI', edit=True, rtf=True, h=True)

def g_asset_export(*args):

	filename = mc.file(q=True, sn=True)
	charvalue = filename.split('/')

	# modifier en cas de SHOTS
	# Ajouter un attribut dynamique que l'on ira chercher pour le debut et fin de sequence

	if charvalue[-5] == 'seq':

		result = mc.promptDialog(
						title='Sequence Export',
						message='This seems to be a Sequence, export anim ?',
						button=['OK', 'Cancel'],
						defaultButton='OK',
						cancelButton='Cancel',
						dismissString='Cancel')

		if result == 'OK':
			
			frames = mc.promptDialog(query=True, text=True)
			frames = frames.split(',')

			if len(frames) != 2:
				sys.exit('Wrong number of Frames. Write start frame and end frame separated by a comma.')

			fst = int(frames[0])
			end = int(frames[-1])
			etg.g_abc_seq_export(mode='startend',qst=fst,qend=end)

			# launch the ABC cleaner
			print('---------------------------------------------------')
			print('---------------------------------------------------')

			print('Launching The Alembic Cleaner... Please wait.')

			import utils.mayapy as mp
			reload(mp)
			mp.launch_mayapy()

			mc.warning('ABC exported and CLEAN.')
		else:
			etg.g_abc_seq_export(mode='currentframe',qst=0,qend=0)

			# launch the ABC cleaner
			print('---------------------------------------------------')
			print('---------------------------------------------------')

			print('Launching The Alembic Cleaner... Please wait.')

			import utils.mayapy as mp
			reload(mp)
			mp.launch_mayapy()

			mc.warning('ABC exported and CLEAN.')
	else:
		etg.g_abc_export(mode='currentframe',qst=0,qend=0)

def autotag_selection(*args):
	
	sel = mc.ls(sl=True)
	#bad_name = mc.ls('group*', transforms=True)
	#if bad_name:

	#	sys.exit('Some groups have a bad name (' + str(len(bad_name)) + ' groups). AutoTag Aborted.')

	go_on = mc.confirmDialog(title='AUTOTAG', message = 'Check if everything is named properly ! Continue ?', button =['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No')

	if go_on == 'No':

		sys.exit('AutoTag Aborted.')

	mdefMenus.auto_tags_selection(sel)


def tag_objects(*args):

	mdefMenus.add_custom_tags()


def asset_group_builder(*args):

	mc.SelectAll()
	sel = mc.ls(sl=True)
	bad_name = mc.ls('group*', transforms=True)
	if bad_name:

		sys.exit('Some groups have a bad name (' + str(len(bad_name)) + ' groups). AutoTag Aborted.')

	etg.asset_group_builder(sel)

def build_guerilla_scene(*args):
	filename = mc.file(q=True, sn=True)
	charvalue = filename.split('/')
	
	if 'assets' in charvalue:

		etg.build_guerilla_scene_b()
	
	elif 'seq' in charvalue:
	
		etg.build_guerilla_scene_sequence()
	
	else:
		mc.warning('Your scene is not an asset nor a sequence...')

def save_version(*args):

	save.version()

def save_master(*args):

	comments = mc.textField('master_comment', q=True, tx=True)
	save.master(comments)


def master_rig(*args):

	autorig.publish_rig()

def check_rigs(*args):

	create.missing_rigs()

def check_history(*args):

	check.history()


def check_ngons(*args):

	r_ngons = check.ngons()
	r_tris = check.ngons(tris=True)
	mc.warning('There are ' + str(r_tris) + ' triangles and ' + str(r_ngons) + ' ngons on this asset.' )

def ref_import(*args):

	reload(create)
	ref_txt = mc.textField('ref_import', q=True, tx=True)
	ref_nspace = mc.textField('namespace_ref', q=True, tx=True)

	if ref_nspace == '':
		ref_nspace = ':'

	create.ref(ref_txt, ref_nspace)

def ref_duplicate(*args):

	mc.warning('This function is not available yet. Sorry !!')

def import_cam(*args):

	cam_sh_num = mc.textField('cam_sh_num', q=True, tx=True)
	create.shot_camera(cam_sh_num)

def create_shot(*args):

	sel = mc.ls(sl=True)

	if not len(sel) == 1:

		sys.exit('Select one camera only')

	if not 'shot' in sel[0]:

		sys.exit('Select one camera please')

	create.shot(sel[0])

def wip(*args):

	mc.warning('This function is not available yet. Sorry !!')

def textual_open(*args):

	asset_txt = mc.textField('textual_open', q=True, tx=True)
	asset_vars = asset_txt.split(' ')


	projectPath = project_dir + '/prod'

	for each in asset_vars:

		projectPath += '/' + each

	if 'mod' in projectPath:

		projectPath += '/mod.ma'

	if 'rig' in projectPath:

		projectPath += '/rig.ma'


	if 'layout' in projectPath:

		projectPath += '/layout.ma'


	go_on = mc.confirmDialog(title='Opening asset', message = "Your current file won't be saved, are you sure ?", button =['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No')

	if go_on != 'Yes':

		
		sys.exit('Opening aborted.')

	mc.file(projectPath, open=True, f = True)


def build_deform_chain(*args):

	import rigTools.deform as deform
	reload(deform)

	nb_joints = mc.textField('nb_joints', q=True, tx=True)
	nb_joints = int(nb_joints)

	sel = mc.ls(sl=True)

	naming = sel[0].split('_')
	module_name = naming[0] + '_' + naming[1] + '_' + naming[2]

	if len(sel) != 1:

		if len(sel) == 3:

			st_hook = sel[1]
			nd_hook = sel[-1]

			deform.create_stretchySpline(
				module_name,
				sel[0],
				start_hook= st_hook,
				end_hook=nd_hook,
				nb_joints = nb_joints)

		else:
			sys.exit('selection is not good enough')
	else:

		deform.create_stretchySpline(
			name = module_name,
			main_bone_ctrl = sel[0],
			nb_joints = nb_joints)


def half_bone(*args):
	import utils.halfbone as hb
	hb.halfBoneCreator()

def open_folder(*args):

	filename = mc.file(q=True, sn=True)
	charvalue = filename.split('/')

	if 'assets' in charvalue:
		print('asset')
		charvalue.pop(-1)
		charvalue.pop(-1)
		charvalue.pop(-1)
		folder_to_open = '\\'.join(charvalue)

	else:

		charvalue.pop(-1)
		charvalue.pop(-1)
		charvalue.pop(-1)
		folder_to_open = '\\'.join(charvalue)

	import subprocess
	print(folder_to_open)

	subprocess.call('explorer ' + folder_to_open, shell=True)