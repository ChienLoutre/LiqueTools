import maya.cmds as mc
import os
import sys
from variables import *
import padding_numbers
import utils.get_extension as ext
import utils.check as check
import shutil

# module marilla de Colin Laubry => export de tags, alembic, ect pour Guerilla
import marilla.defMenus as mdefMenus
import marilla.marillaUi as mUi
import marilla.maUtils as mUtils
import marilla.guegueTags as mTags

#pymel pour export selection
import pymel.core as pmc

guerilla_path = os.getenv('GUERILLA')
#guerilla_path = 'G:\\Guerilla_Render_2.0.0a21'

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#		   Guerilla export with/without animation
#
#
#
#
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
try:
	import pymel.core as pmc
except ImportError:
	pass

def abc_custom_export(framemode='currentframe', qstart=0, qend=0, preroll=False,
				path='', preframe=0, nodes=[]):
	"""wrapper the abcexport export abc file with abcexport maya command with
	 some preset like uvwrite, world space, color groups, face groups

	:type framemode: string
	:param framemode: currentframe, timeslider, startend
	:type qstart: int
	:param qstart: precise start frame manualy for startend framemode option
	:type qend: int
	:param qend: precise end frame manualy for startend framemode option
	:type preroll: bool
	:param preroll: active a preroll compute frames
	:type preframe: int
	:param preframe: precise the preroll start frame
	:type nodes: list
	:param nodes: list of maya transform nodes
	:type path: string
	:param path: the alembic path file
	"""
	if framemode == 'currentframe':
			start = int(pmc.currentTime(query=True))
			end = int(pmc.currentTime(query=True))
	elif framemode == 'timeslider':
		start = int(pmc.playbackOptions(q=True, ast=True))
		end = int(pmc.playbackOptions(q=True, aet=True))
	elif framemode == 'startend':
		start = qstart
		end = qend
	else:
		raise ValueError(("Wrong framemode, must be currentframe or timeslider"
						" or startend"))
	if path == '':
		raise ValueError("Must precise a string path")
	prerollstring = ''
	if preroll:
		prerollstring = ('-frameRange {prerollstart} {startp} -step 1 -preRoll'
		).format(prerollstart=preframe, startp=start-1)
	if len(nodes) == 0:
		raise ValueError("obj arg cant be an empty list of transform")
	objects = ''
	for obj in nodes:
		objects += ' -root |' + obj.name()
	abcstring = ('{prerollstring} -frameRange {start} {end} -attr GuerillaTags -Attr Center -attr Front -attr Up -attr PupilSize'
	' -uvWrite -writeColorSets -writeFaceSets -writeVisibility -worldSpace -dataFormat ogawa'
	' {objects} -file {path}').format(
					prerollstring=prerollstring, start=start, end=end, 
					objects=objects, path=path)
	pmc.AbcExport(jobArg=abcstring, verbose=True)


def g_abc_export(mode='currentframe',qst=0,qend=0):

	filename = mc.file(q=True, sn=True)
	charvalue = filename.split('/')

	# Verifier que l'on est dans le projet

	if not project_name in charvalue:
		sys.exit('You are not working in the Project !!')

	# Verifier asset/sequence
	# Definir options pour asset sequence

	if 'seq' in charvalue:

		# sequences options/variables
		check_name = ['chars','props','sets','cams','building']

	else:

		# asset options/variables
		check_name = charvalue[-4]

	# Sortir l'emplacement du fichier seulement

	file_path = charvalue[:-1]

	filevalue = charvalue[-1]

	print('filevalue => ' + filevalue)

	filevalue, extension = ext.get_ext(filevalue)

	filevalue = charvalue[-4]

	file_path.pop(-1)
	file_path.pop(-1)
	print(charvalue)

	file_path = '/'.join(file_path)
	print('file_path => '+ file_path)
	print(filevalue)

	extension = '.abc'
	charvalue = file_path + '/' + 'export/' + filevalue + extension
	print(charvalue)

	mc.SelectAll()
	sel = mc.ls(sl=True)
	check.transforms(sel)
	sel = pmc.ls(sl=True)
	mc.select(cl=True)
	print(sel)

	# check export asset / sequence
	if not len(sel) == 1:
		print('sel > 1')
		# asset export checks
		if not 'seq' in charvalue:
			print('asset type')
			sys.exit('One group only must be selected, with the asset name. Use the Asset Group Builder command to do that.')


		#sequence export checks
		else:
			print('seq type')
			if not sel == check_name:
				sys.exit('You need to select the 5 groups that are in the asset => chars, props, sets, cams and building. Nothing else should be present.')

	# asset export checks
	elif not sel[0] == check_name:
		sys.exit('One group only must be selected, with the asset name. Use the Asset Group Builder command to do that.')



	if os.path.exists(charvalue):

		go_on = mc.confirmDialog(title='Exporting Alembic !!', message = 'An ABC already exists for : ' + filevalue + ', do you want to overwrite it ?', button =['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No')

		if go_on == 'No':

			sys.exit('Alembic Export Aborted')


	abc_custom_export(framemode=mode,qstart=qst,qend=qend,preroll=False,path=charvalue,preframe=0,nodes=sel)

	print('Alembic : ' + filevalue + ' successfully created !')


def g_abc_seq_old_export(mode='currentframe',qst=0,qend=0):

	filename = mc.file(q=True, sn=True)
	charvalue = filename.split('/')

	# Verifier que l'on est dans le projet

	if not project_name in charvalue:
		sys.exit('You are not working in the Project !!')

	# Verifier asset/sequence
	# Definir options pour asset sequence

	# sequences options/variables
	cam_exp = 'cams'
	if 'shots' in charvalue:
		cam_exp = 'cam1'

	check_name = ['chars','props','sets',cam_exp,'building']

	# Sortir l'emplacement du fichier seulement

	file_path = charvalue[:-1]

	filevalue = charvalue[-1]

	filevalue, extension = ext.get_ext(filevalue)

	filevalue = charvalue[-4]

	file_path.pop(-1)
	file_path.pop(-1)

	file_path = '/'.join(file_path)

	extension = '.abc'
	charvalue = file_path + '/' + 'export/'

	mc.select(cl=True)
	for each in check_name:
		group = mc.select(each, add=True)

	chktr = mc.ls(sl=True)
	check.transforms(chktr)

	sel = pmc.ls(sl=True)
	mc.select(cl=True)

	# create a txt file with infos for the time.
	temp_dir = charvalue + 'frames'

	with open(temp_dir  + '.txt', "w") as f:
		f.write(str(qst) + ';' + str(qend))
		f.close()

	# dump "rig" folders out of the export.

	# create the folders that will be exported.



	for each in sel:

		assets = mc.listRelatives(str(each), c=True)
		print(assets)

		for asset in assets:

			try:
				folders = mc.listRelatives(str(asset), c=True)
				
			except ValueError:
				print(asset + ' seems to exist more than once. Full export will be performed.')

			print(folders)

			if folders == ['mod', 'rig']:

				print('asset chelou')

			else:
				print('Full export is performed.')
		print('________________________________')
		print('________________________________')


	if os.path.exists(charvalue):

		go_on = mc.confirmDialog(title='Exporting Alembic !!', message = 'An ABC already exists for : ' + filevalue + ', do you want to overwrite it ?', button =['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No')

		if go_on == 'No':

			sys.exit('Alembic Export Aborted')


	for each in sel:
		abc_name = charvalue + each + '.abc'
		node_to_export = []
		node_to_export.append(each)
		abc_custom_export(framemode=mode,qstart=qst,qend=qend,preroll=False,path=abc_name,preframe=0,nodes=node_to_export)

	temp_dir = project_dir + '\\utils\\export\\clean_abc'

	with open(temp_dir  + '.txt', "w") as f:
		f.write(str(charvalue))
		f.close()

	print('Alembic : ' + filevalue + ' successfully created !')


def g_abc_seq_export(mode='currentframe',qst=0,qend=0, check_name = ['chars','props','sets','cams','building']):

	filename = mc.file(q=True, sn=True)
	charvalue = filename.split('/')

	# Verifier que l'on est dans le projet

	if not project_name in charvalue:
		sys.exit('You are not working in the Project !!')

	# Verifier asset/sequence
	# Definir options pour asset sequence

	# sequences options/variables
	
	# Sortir l'emplacement du fichier seulement

	file_path = charvalue[:-1]

	filevalue = charvalue[-1]

	filevalue, extension = ext.get_ext(filevalue)

	filevalue = charvalue[-4]

	file_path.pop(-1)
	file_path.pop(-1)

	file_path = '/'.join(file_path)

	extension = '.abc'
	charvalue = file_path + '/' + 'export/'

	mc.select(cl=True)
	for each in check_name:
		group = mc.select(each, add=True)

	chktr = mc.ls(sl=True)
	check.transforms(chktr)

	sel = pmc.ls(sl=True)
	mc.select(cl=True)

	# create a txt file with infos for the time.
	temp_dir = charvalue + 'frames'

	with open(temp_dir  + '.txt', "w") as f:
		f.write(str(qst) + ';' + str(qend))
		f.close()

	# dump "rig" folders out of the export.

	# create the folders that will be exported.



	for each in sel:

		assets = mc.listRelatives(str(each), c=True)
		print(assets)

		for asset in assets:
			folders = None
			try:
				folders = mc.listRelatives(str(asset), c=True)
				
			except ValueError:
				print(asset + ' seems to exist more than once. Full export will be performed.')


			if folders == ['mod', 'rig']:

				print('asset chelou')

			else:
				print('Full export is performed.')
		print('________________________________')
		print('________________________________')


	if os.path.exists(charvalue):

		go_on = mc.confirmDialog(title='Exporting Alembic !!', message = 'An ABC already exists for : ' + filevalue + ', do you want to overwrite it ?', button =['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No')

		if go_on == 'No':

			sys.exit('Alembic Export Aborted')


	for each in sel:
		abc_name = charvalue + each + '.abc'
		node_to_export = []
		node_to_export.append(each)
		abc_custom_export(framemode=mode,qstart=qst,qend=qend,preroll=False,path=abc_name,preframe=0,nodes=node_to_export)

	temp_dir = project_dir + '\\utils\\export\\clean_abc'

	with open(temp_dir  + '.txt', "w") as f:
		f.write(str(charvalue))
		f.close()

	if ('chars' in check_name) or ('props' in check_name):

		# launch the ABC cleaner
		print('---------------------------------------------------')
		print('---------------------------------------------------')

		print('Launching The Alembic Cleaner... Please wait.')

		import utils.mayapy as mp
		reload(mp)
		mp.launch_mayapy()	

	print('Alembic : ' + filevalue + ' successfully created !')


def asset_group_builder(sel):

	filename = mc.file(q=True, sn=True)

	charvalue = filename.split('/')


	if not project_name in charvalue:
		sys.exit('You are not working in the Project !!')

	asset_name = charvalue[-4]
	
	top_grp = mc.group(em=True, n=asset_name)
	mc.parent(sel,top_grp)

# -------------------------------------------------------------
#  BUILDING GUERILLA SCENE
#
# modifier pour export de sequences :
# 	- pas de cyclo : OK
#	- importer les bons RenderGraph pour chaque asset reference dans la scene : OK
#	- cameras ?
#
#
#
#
# -------------------------------------------------------------


def build_guerilla_scene():

	filename = mc.file(q=True, sn=True)
	charvalue = filename.split('/')

	# Verifier que l'on est dans le projet

	if not project_name in charvalue:
		sys.exit('You are not working in the Project !!')

	# verifier que l'alembic est cree

	charvalue.pop(-1)
	charvalue.pop(-1)
	charvalue.pop(-1)

	asset_name = charvalue[-1]

	charvalue.append('export')

	print(charvalue)


	filepath = '/'.join(charvalue)

	exports = os.listdir(filepath)

	if not asset_name + '.abc' in exports:

		sys.exit('No Alembic file created !!')

	print('The alembic for the asset ' + asset_name + ' exists !')

	filepath += '/' + asset_name + '.abc'
	asset_type = charvalue[-3]

	# arguments a garder

	temp_dir = project_dir + '\\utils\\export\\guerilla_temp'

	with open(temp_dir  + '.txt', "w") as f:
		f.write(filepath + ';' +asset_type)
		f.close()

	# Verifier si V000 existe deja

	charvalue.pop(-1)
	filepath = '/'.join(charvalue)
	filepath += '/lookdev/guerilla'

	if len(os.listdir(filepath)) != 0:

		go_on = mc.confirmDialog(title='Creating Guerilla Project', message = 'A gproject file already exists for : ' + asset_name + ', do you want to overwrite it ?', button =['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No')

		if go_on == 'No':

			sys.exit('Guerilla Project creation aborted')

	# lancer guerilla avec script integre

	import subprocess
	subprocess.call([guerilla_path + '/guerilla.exe' , "Y:\\Liquefacteur\\utils\\scripts\\grender\\build_asset_scene.py"])

	# dire que la commande est reussie

	mc.warning('Lookdev file for the asset ' + asset_name + ' sucessfully built !')



# -------------------------------------------------------------
#  BUILDING GUERILLA SCENE
#
# modifier pour export de sequences :
# 	- pas de cyclo : OK
#	- importer les bons RenderGraph pour chaque asset reference dans la scene : OK
#	- cameras ?
#	- regler probleme de reference si il y a des cameras genre back et bottom. Probleme trouve, il recup les cams avant le reste
#	  il faut donc que je trouve un moyen de ne pas prendre en compte les cameras dans la ref
#
#
# -------------------------------------------------------------


def build_guerilla_scene_b():

	filename = mc.file(q=True, sn=True)
	charvalue = filename.split('/')

	# Verifier que l'on est dans le projet

	if not project_name in charvalue:
		sys.exit('You are not working in the Project !!')

	# verifier que l'alembic est cree

	charvalue.pop(-1)
	charvalue.pop(-1)
	charvalue.pop(-1)

	asset_name = charvalue[-1]
	type_seq = False
	if charvalue[-2] == 'seq':

		type_seq = True


	charvalue.append('export')

	print(charvalue)


	filepath = '/'.join(charvalue)

	exports = os.listdir(filepath)

	if not asset_name + '.abc' in exports:

		sys.exit('No Alembic file created !!')

	print('The alembic for the asset ' + asset_name + ' exists !')

	filepath += '/' + asset_name + '.abc'

	# Asset ou sequence

	if not 'seq' in charvalue:

		asset_type = charvalue[-3]
		temp_dir = project_dir + '\\utils\\export\\guerilla_temp'

		print(temp_dir)
		with open(temp_dir  + '.txt', "w") as f:
			f.write(filepath + ';' +asset_type)
			f.close()

	else:

		# recuperer les references
		sel = mc.ls(references=True)
		ref_list = ''

		# temporaire = faire plus clean
		cam_nodes = ['left','leftShape','back','backShape','bottom','bottomShape'] 

		for each in sel:

			ref_nodes = mc.referenceQuery(each, n=True)

			for item in cam_nodes:

				if item in ref_nodes:

					ref_nodes.remove(item)


			ref = ref_nodes[0]

			if ref_list == '':

				ref_list = ref
			else:
				ref_list += ',' + ref

		last_frame = 150
		temp_dir = project_dir + '\\utils\\export\\guerilla_temp'

		print(temp_dir)
		with open(temp_dir  + '.txt', "w") as f:
			f.write(filepath + ';' + str(last_frame) + ';' + ref_list)
			f.close()	# arguments a garder

	# Verifier si V000 existe deja

	charvalue.pop(-1)
	filepath = '/'.join(charvalue)
	filepath += '/lookdev/guerilla'


	print(guerilla_path)

	if len(os.listdir(filepath)) != 0:

		go_on = mc.confirmDialog(title='Creating Guerilla Project', message = 'A gproject file already exists for : ' + asset_name + ', do you want to overwrite it ?', button =['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No')

		if go_on == 'No':

			sys.exit('Guerilla Project creation aborted')

	# lancer guerilla avec script integre

	if type_seq == False:

		import subprocess
		subprocess.call([guerilla_path + '\\guerilla.exe' , "Y:\\Liquefacteur\\utils\\scripts\\import_guerilla\\build_asset_scene.py"])
		mc.warning('Lookdev file for the asset ' + asset_name + ' sucessfully built !')



def build_guerilla_scene_sequence():
	
	print('-_-_-_-_--_-_-_--_-_-_--_-_-_-_--_-_-_-_-_-_-')
	print('Sequence building for Guerilla launched')
	print('-_-_-_-_--_-_-_--_-_-_--_-_-_-_--_-_-_-_-_-_-')

	filename = mc.file(q=True, sn=True)
	charvalue = filename.split('/')

	# Verifier que l'on est dans le projet

	if not project_name in charvalue:
		sys.exit('You are not working in the Project !!')

	# verifier que l'alembic est cree

	charvalue.pop(-1)
	charvalue.pop(-1)
	charvalue.pop(-1)

	if not (charvalue[-2] == 'seq'):
		if not 'shots' in charvalue:
			raise ValueError('You are not working in a sequence')

	seq_name = charvalue[-1]

	charvalue.append('export')

	filepath = '/'.join(charvalue)

	exports = os.listdir(filepath)

	# check alembics (chars, props, set, building)
	# alembic => comment ????
	
	print('Acquiring References...')

	abc_list = ['chars','props','sets','cams','building']

	for each in abc_list:

		if not each + '.abc' in exports:
			print('No alembic for ' + each.upper() +'!')


	# recuperer les references
	ref_sel = mc.ls(references=True)
	print('--------------------------------------')
	print(ref_sel)
	print('--------------------------------------')

	ref_list = ''

	# temporaire = faire plus clean
	cam_nodes = ['left','leftShape','back','backShape','bottom','bottomShape'] 	
	
	for each in ref_sel:
		try:
			ref_nodes = mc.referenceQuery(each, n=True)
			if not ref_nodes:
				pass
			else:	
				for item in cam_nodes:

					if item in ref_nodes:

						ref_nodes.remove(item)

				ref = ref_nodes[0]

				if ref_list == '':

					ref_list = ref
				else:
					ref_list += ',' + ref

		except RuntimeError:
			pass
			
	print('References acquired.')

	last_frame = 150
	temp_dir = project_dir + '\\utils\\export\\guerilla_temp'

	with open(temp_dir  + '.txt', "w") as f:
		f.write(filepath + ';' + str(last_frame) + ';' + ref_list)
		f.close()	# arguments a garder

	# Verifier si V000 existe deja

	charvalue.pop(-1)
	filepath = '/'.join(charvalue)
	filepath += '/lookdev/guerilla'

	if len(os.listdir(filepath)) != 0:

		go_on = mc.confirmDialog(title='Creating Guerilla Project', message = 'A gproject file already exists, do you want to overwrite it ?', button =['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No')

		if go_on == 'No':

			sys.exit('Guerilla Project creation aborted')

	# lancer guerilla avec script integre
	
	print('Launching Guerilla...')

	script_import = "Y:\\Liquefacteur\\utils\\scripts\\import_guerilla\\build_sequence_scene__test.py"

	if 'shots' in filepath:
		script_import = "Y:\\Liquefacteur\\utils\\scripts\\import_guerilla\\build_shot_scene.py"
	import subprocess
	subprocess.call([guerilla_path + '\\guerilla.exe' , script_import])
	mc.warning('Lookdev file for this sequence sucessfully built !')
