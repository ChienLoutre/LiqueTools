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

	print('ref_list = ' + str(ref_list))

	seq_name = seq_path.split('/')
	seq_name = seq_name[-1]

	seq_name, asset_ext = ext.get_ext(seq_name)

	write_path = project_dir + '/prod/seq/' + seq_name + '/lookdev/guerilla/'

	a = dict({'prefixnodes':False,'containschildren':False})

	doc.LastFrame.set(int(last_frame))
	rPass = pynode('RenderPass')

	# add a reference

	with Modifier() as mod:

		refNode, topNodes = mod.createref(seq_name + '__ref', seq_path, parent=None, options=a)
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


	print('ref_list = ' + str(ref_list))


	with Modifier() as mod:

		search_path = project_dir + '/prod/assets/'

		for each in ref_list:

			if each in os.listdir(search_path + 'chars/'):

				asset_path = search_path + 'chars/' + each + '/lookdev/guerilla/master/lookdev.gproject'

			elif each in os.listdir(search_path + 'props/'):

				asset_path = search_path + 'props/' + each + '/lookdev/guerilla/master/lookdev.gproject'

			elif each in os.listdir(search_path + 'sets/'):

				asset_path = search_path + 'sets/' + each + '/lookdev/guerilla/master/lookdev.gproject'

			try:  
				refNode, topNodes = mod.createref(each + '__ref', asset_path, parent=None, options=a)
			except:
				print('No Guerilla Master file for ' + each + '.')




	rPass = pynode('RenderPass')
	rGraph = pynode('RenderGraph')

	# desactiver motionblur, dof, et renommer RenderGraph
	# modifier size du rendu

	with Modifier() as mod:

		rGraph.Apply.set('tags')
		mod.renamenode(rGraph, seq_name + '_RenderGraph')
		doc.ProjectHeight.set(1080)
		doc.ProjectWidth.set(1920)


	# save file with indentation

	write_path += 'V000'

	try:
		os.mkdir(write_path)
	except:
		print('folder V000 existing !')

	write_path += '/lookdev.gproject'

	doc.save(filename=write_path,warn=False,addtorecent=False)

	render.build_path()


	os.remove(temp_dir + '.txt')

	#sys.exit('Done !')

except IOError:
	print('lolilol')