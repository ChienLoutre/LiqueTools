import maya.cmds as mc
import pymel.core as pmc
import sys
import selection
reload(selection)
# parent shape to selected

def parent_shape_to_selected():

	sel = mc.ls(sl=True)

	if not len(sel) == 2:
		
		sys.exit('select one shape and an object please')
		
	mc.rename(sel[0], sel[1] + '_shape')
	sel = mc.ls(sl=True)
	mc.parent(sel[0], sel[1], r=True, s=True)


def instance_shape_to_selected():

	sel = mc.ls(sl=True)

	if not len(sel) == 2:
		
		sys.exit('select one shape and an object please')
	

	mc.parent(sel[0], sel[1], add=True, s=True)


def add_float_attr(sel, longname, attr_type='float', min_value=0.0, max_value=0.0, def_value=0.0):

	if not isinstance(sel,list):
		sel = [sel]

	if min_value == 0.0 and max_value == 0.0:

		mc.addAttr(sel[0], ln=longname, at=attr_type)

	else :

		mc.addAttr(sel[0], ln=longname, at=attr_type, min=min_value, max=max_value, dv=def_value)

	mc.setAttr(sel[0] + '.' + longname, k=True)

def add_enum_attr(sel, longname, attr_type='enum', values='--------::'):

	if not isinstance(sel,list):
		sel = [sel]

	mc.addAttr(sel[0], ln=longname, at=attr_type, en=values)
	mc.setAttr(sel[0] + '.' + longname, cb=True)

def copy_inmesh(sel=None, target=None):

	'''
	select two objects, the mesh you want to copy and the target mesh receiving the shape.
	for use in a script, use the following syntax
	
	sel, target = copy_inmesh(mesh_to_copy, target_mesh)

	'''
	returnList = []
	if not sel:
		# Get Current selection
		sel = mc.ls( sl = True )
	elif not isinstance(sel,list):
		sel = [sel]

	if not len(sel) == 2:
		sys.exit('select a mesh and a target for the new mesh')

	target = sel[1]
	sel = sel[0]

	# check if the selected meshes are Shapes.
	chk_shp = mc.listRelatives(sel, s=True)

	print(chk_shp)
	if len(chk_shp) > 1:
		sys.exit('more than one shape on the mesh you wanna copy.')

	sel = chk_shp[0]

	chk_shp = mc.listRelatives(target, s=True)
	
	print(chk_shp)
	if len(chk_shp) > 1:
		mc.warning('more than one shape on the mesh you wanna copy.')

	target = chk_shp[0]

	mc.connectAttr(sel + '.outMesh', target + '.inMesh')

	mc.warning('connection between ' + sel + ' and ' + target + ' done.')

	return sel, target

def blendshape_ui(sel=None):
	'''
	Select a mesh at a state you wanna create a blendshape. You will be asked to 
	'''
	selection.simple_txt_ui(def_window='blendshape_name', def_title = 'Set Blendshape Name', txtfield = 'bs_name', ok_button= 'Create Blendshape', function_launch = create_blendshape)

def create_blendshape(base_mesh,blendshape_name):

	blendshape_name = blendshape_name + '__shp'

	mc.duplicate(base_mesh, n=blendshape_name)

	try:
		mc.parent(blendshape_name, 'blendshapes')
		mc.warning('blendshape "' + blendshape_name + '" successfully created !')
	except:
		mc.warning('no blendshape grp in the scene')

	return blendshape_name

def toggle_parametric_spaces(force=False, show=1):

	#mc.select('*__param')
	sel = mc.ls(type='renderBox')
	# check if the selected objects are parametric spaces

	for each in sel:
		isvisible = mc.getAttr(each + '.visibility')

		if force == True:
			show = show
		else:
			show = 0
			if isvisible == 0:
				show = 1
		mc.setAttr(str(each) +'.visibility', (show))