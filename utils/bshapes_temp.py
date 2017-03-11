import maya.cmds as mc
import pymel.core as pmc
import sys

def morph_shape(sel=None):
	'''
	shape_m => la nouvelle shape sur laquelle on veut transferer les blendshapes
	shape_g => la shape de base

	'''
	new_shapes_folder = 'michel__bshapes'

	
	shape_g = mc.duplicate(shape_g)
	shape_g = shape_g[0]
	shape_g = mc.rename(shape_g, 'target_temp__shape')
	
	mc.blendShape(shape_m, sel, shape_g, n='modify_temp__bs')
	mc.blendShape('modify_temp__bs', edit=True, w=[(0, 1),(1, 1)])
	
	mc.delete(shape_g, ch=True)

	mc.parent(shape_g, new_shapes_folder)
	mc.rename(shape_g, 'michel__' + sel)

	return shape_gg, selg, shape_g

# sel = mc.ls(sl=True)
# for each in sel:
# 	morph_shape(each)

def lol():
	'''
	What is the purpose of this ?
	'''
	import maya.cmds as mc

	sel = mc.ls(sl=True)
	shapes = sel[0]
	targets = sel[1]

	shapes = mc.listRelatives(shapes, c=True)
	targets = mc.listRelatives(targets, c=True)

	for shape in shapes:
		get_name = shape.split('__')
		get_name = get_name[1]
		
		print(shape)
		for target in targets:
			
			if target == get_name:
				
				mc.blendShape(shape, target, n='temp_bs')
				mc.delete(target, ch=True)
				
			else:
				pass



def morph_shape_pymel(sel=None, name='michel'):
	'''
	Select first the base shape which has all the targets, then the shape which will receive the new blendshapes.
	Select third the group with all the blendshapes from the old mesh, and fourth the group with all the blendshapes for the new BCS rig.

	Additional infos :
		shape_m => new shape (for receiving blendshapes)
		shape_g => base shape

	Reminder :

	You must have all the blendshapes to transfer in a group.
	You must duplicate those shapes to get them out of the initial facial rig
	You must transfer the BCS setup to the other shape
	You must select all the blendshapes of the new BCS rig and put them in a group
	Now you can transfer the shapes into the new BCS rig.

	'''
	returnList = []
	if not sel:
		# Get Current selection
		sel = pmc.ls( sl = True )
	elif not isinstance(sel,list):
		sel = [sel]

	if len(sel) != 4:
		raise ValueError('Select only two Shapes, the base one then the target. The, select the group containing all the blendshapes to transfer.')

	# Base shape, and target shape (for rig)

	shape_g = sel[0]
	shape_m = sel[1]

	# Groups :
		# old_bshapes_grp : group with all the blendshapes from the base mesh
		# new_bshapes_grp : group with all the blendshapes for the target mesh (they must be all blank, same as the new target mesh.)
	old_bshapes_grp = sel[2]
	new_bshapes_grp = sel[3]

	new_shapes_folder = pmc.group(em=True, n=shape_m + '__bshapes')


	# duplicating the base shape so that the original one is not affected by the changes.

	shapes = pmc.listRelatives(old_bshapes_grp, c=True)

	for shape in shapes:

		shape_gg = pmc.duplicate(shape_g)
		shape_gg = pmc.rename(shape_gg, 'target_temp__shape')

		pmc.blendShape(shape_m, shape, shape_gg, n='modify_temp__bs')
		pmc.blendShape('modify_temp__bs', edit=True, w=[(0, 1),(1, 1)])
		
		pmc.delete(shape_gg, ch=True)

		pmc.parent(shape_gg, new_shapes_folder)

		if '|' in str(shape):
			new_name = str(shape).split('|')
			new_name = new_name[-1]
			new_name = name + '__' + new_name

		print(new_name)
		pmc.rename(shape_gg, new_name)


	shape_shifter_pymel(new_shapes_folder,new_bshapes_grp)


def shape_shifter_pymel(old_bshapes_grp, new_bshapes_grp):
	'''
	Transfer each shape with the new Mesh into the new BCS rig.
	'''
	import pymel.core as pmc

	print('-----------------------------------------')
	print('    Shape Shifter Launching now...       ')
	print('-----------------------------------------')

	shapes = old_bshapes_grp
	targets = new_bshapes_grp

	shapes = pmc.listRelatives(shapes, c=True)
	targets = pmc.listRelatives(targets, c=True)

	for shape in shapes:

		new_name = ''
		if '|' in str(shape):
			new_name = str(shape).split('|')
			new_name = new_name[-1]

		else:
			new_name = str(shape)

		get_name = str(new_name).split('__')
		get_name = get_name[1]
		
		print(get_name)
		for target in targets:

			target_new_name = ''
			if '|' in str(target):
				target_new_name = str(target).split('|')
				target_new_name = target_new_name[-1]	


			if target_new_name == get_name:
				print('Connection Found for ' + str(target) + '!')
				pmc.blendShape(shape, target, n='temp_bs')
				pmc.blendShape('temp_bs', edit=True, w=[(0, 1)])

				pmc.delete(target, ch=True)
				
			else:
				print('No connection found for ' + str(target) + '!')
				pass
