from variables import *
from guerilla import Document, Modifier, pynode
import guerilla
import utils.get_extension as ext
import os
import sys
import grender.render as render
import grender.scene_init
li = liquerillaInit()
doc = Document()

# -------------------------------------------------------------------------
# IMPORTE L'ASSET DANS GUERILLA ET CREE UNE V000
# 
# 
# bugs a fixer :
# 
# - taille en 720/720 (carre semble bien pour assets) - OK
# - cyclo a bien centrer, cam, ect... - OK
# - RenderPass a NE PAS EXPORTER - OK
# - Geometry a NE PAS EXPORTER - OK
# - Integrer deadline pour rendus tests / ou mettre ces tests ? - OK
# - Virer dossier "wip" ailleurs
# - Passer en mode "tags"
# - Changer render_path (render.build_path) - OK
# - 
# -------------------------------------------------------------------------

suffix_rg = '__rg'

doc.new(warn=False)
doc.LastFrame.set(100)

temp_dir = project_dir + '\\utils\\export\\guerilla_temp'
cyclo_dir = project_dir + '\\utils\\guerilla\\cyclo.gproject'

try:

	file_path = open(temp_dir + '.txt', 'r')
	asset_path = file_path.read()
	file_path.close()

	
	asset_path = asset_path.split(';')
	asset_type = asset_path[-1]
	asset_path = asset_path[0]

	asset_name = asset_path.split('/')
	asset_name = asset_name[-1]

	asset_name, asset_ext = ext.get_ext(asset_name)

	write_path = project_dir + '/prod/assets/' + asset_type + '/' + asset_name + '/lookdev/guerilla/'

	a = dict({'prefixnodes':False,'containschildren':False})

	rPass = pynode('RenderPass')

	# add a reference

	with Modifier() as mod:

		refNode, topNodes = mod.createref(asset_name + '__ref', asset_path, parent=None, options=a)
		refNode.setinheritedattr('Referenceable',False, False)

		refNode, topNodes = mod.createref('cyclo', cyclo_dir, parent=None, options=a)
		refNode.setinheritedattr('Referenceable',False, False)

		# create the plug using createplug
		# createplug throws an exception if the plug already exists, so try/except is recommended
		try:
			mod.createplug (rPass, 'Referenceable', plugType='Plug', dataType='bool', flags=guerilla.Plug.Dynamic)
		except:

			pass

		# So we can set it to False now

		rPass.Referenceable.set(False)



	# make Camera from Cyclo scene => MainCamera

	cam = 'studio_lighting|asset_cam'
	cam_attr = cam + ('.Name')


	with Modifier() as mod:

		mod.connect((pynode('.MainCamera')),(pynode(cam_attr)))


	#cyclo = pynode('cyclo')
	#cyclo.setinheritedattr('Referenceable',False, False)

	rPass = pynode('RenderPass')
	rGraph = pynode('RenderGraph')

	# desactiver motionblur, dof, et renommer RenderGraph
	# modifier size du rendu

	with Modifier() as mod:

		rPass.EnableDepthOfField.set(False)
		rPass.DisableMotionBlur.set(True)
		rGraph.Apply.set('tags')
		mod.renamenode(rGraph, asset_name + suffix_rg)
		doc.ProjectHeight.set(720)
		doc.ProjectWidth.set(1280)
		li.set_gamma(1)

	# save file with indentation

	write_path += 'V000'

	try:
		os.mkdir(write_path)
	except:
		print('folder V000 existing !')

	write_path += '/lookdev.gproject'

	doc.save(filename=write_path,warn=False,addtorecent=False)

	# changer emplacement des rendus en local

	render.build_path()
	render_path, render_path_local, job_path = render.get_paths()
	out_image_vars = 'out' + '_$04f.$x'
	out_image_name = render_path_local + '/' + out_image_vars

	with Modifier() as mod:
		rPass.FileName.set(out_image_name)

	doc.save(filename=write_path,warn=False,addtorecent=False)
	
	os.remove(temp_dir + '.txt')
	sys.exit('Done !')

except IOError:

	print('Opening Guerilla without script.')