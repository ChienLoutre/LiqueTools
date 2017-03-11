from variables import *
from guerilla import Document, Modifier, pynode
import guerilla
import utils.get_extension as ext
import os
import sys
import grender.render as render
doc = Document()

# -------------------------------------------------------------------------
# IMPORTE L'ASSET DANS GUERILLA ET CREE UNE V000
# 
# 
# bugs a fixer :
# 
# - taille en 1920/1080 (carre semble bien pour assets) - OK
# - Integrer deadline pour rendus tests / ou mettre ces tests ?
# - Virer dossier "wip" ailleurs
# - master non reference ???
# -------------------------------------------------------------------------
print('-_-_-_-_--_-_-_--_-_-_--_-_-_-_--_-_-_-_-_-_-')
print('CE SCRIPT EST LE BUILD_SHOT_SCENE.PY')
print('-_-_-_-_--_-_-_--_-_-_--_-_-_-_--_-_-_-_-_-_-')

doc.new(warn=False)

temp_dir = project_dir + '\\utils\\export\\guerilla_temp'

try:

	file_path = open(temp_dir + '.txt', 'r')
	seq_path = file_path.read()
	file_path.close()


	seq_path = seq_path.split(';')
	ref_list = [seq_path[2]]
	last_frame = seq_path[1]
	seq_path = seq_path[0]

	shot_list = seq_path.split('/')

	seq_name = shot_list[-4]
	shot_name = shot_list[-2]
	

	write_path = project_dir + '/prod/seq/' + seq_name + '/shots/' + shot_name + '/lookdev/guerilla/'

	a = dict({'prefixnodes':False,'containschildren':False})

	doc.LastFrame.set(int(last_frame))
	rPass = pynode('RenderPass')

	# add a reference

	with Modifier() as mod:

		refNode, topNodes = mod.createref('chars__ref', seq_path + '/chars.abc', parent=None, options=a)
		refNode, topNodes = mod.createref('props__ref', seq_path + '/props.abc', parent=None, options=a)
		refNode, topNodes = mod.createref('sets__ref', seq_path + '/sets.abc', parent=None, options=a)
		refNode, topNodes = mod.createref('cams__ref', seq_path + '/cams.abc', parent=None, options=a)
		refNode, topNodes = mod.createref('building__ref', seq_path + '/building.abc', parent=None, options=a)

		refNode.setinheritedattr('Referenceable',False, False)

		# create the plug using createplug
		# createplug throws an exception if the plug already exists, so try/except is recommended
		try:
			mod.createplug (rPass, 'Referenceable', plugType='Plug', dataType='bool', flags=guerilla.Plug.Dynamic)
		except:

			pass

		# So we can set it to False now

		rPass.Referenceable.set(True)

# add all assets references


	if not ',' in ref_list[0]:
		ref_list = ref_list
	else:
		ref_list = ref_list[0]
		ref_list = ref_list.split(',')

	print(ref_list)
	with Modifier() as mod:

		search_path = project_dir + '/prod/assets/'
		asset_path = None
		for each in ref_list:

			if each in os.listdir(search_path + 'chars/'):

				asset_path = search_path + 'chars/' + each + '/lookdev/guerilla/master/lookdev.gproject'

			elif each in os.listdir(search_path + 'props/'):

				asset_path = search_path + 'props/' + each + '/lookdev/guerilla/master/lookdev.gproject'

			elif each in os.listdir(search_path + 'sets/'):

				asset_path = search_path + 'sets/' + each + '/lookdev/guerilla/master/lookdev.gproject'

			if asset_path != None:
				test_master = asset_path.split('/')
				test_master.pop(-1)
				test_master = '/'.join(test_master)
			else:
				test_master	= None

			if test_master != None:
				try:
					test_master = os.listdir(test_master)
					if 'lookdev.gproject' in test_master:
						refNode, topNodes = mod.createref(each + '__ref', asset_path, parent=None, options=a)
					else:
						print('No Master')
				except WindowsError:
					pass




	rPass = pynode('RenderPass')
	rGraph = pynode('RenderGraph')

	# desactiver motionblur, dof, et renommer RenderGraph
	# modifier size du rendu

	with Modifier() as mod:

		rGraph.Apply.set('tags')
		mod.renamenode(rGraph, seq_name + '_' + shot_name + '__rg')
		doc.ProjectHeight.set(1080)
		doc.ProjectWidth.set(1920)
		li.set_gamma(1)
	# save file with indentation
	
	write_path += 'V000'
	
	try:
		os.mkdir(write_path)
	except:
		print('BUG !!!')
	write_path += '/lookdev.gproject'

	doc.save(filename=write_path,warn=False,addtorecent=False)

	render.build_path()


	os.remove(temp_dir + '.txt')

	
	sys.exit('OK DOGGIE !')

except IOError:
	print('Problem happened.')
