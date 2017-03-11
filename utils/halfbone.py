import pymel.core as pmc

def halfBoneCreator():
		
	# recuperer la selection
		
	selection = pmc.ls(selection=True)
	
	if len(selection) != 2:
		
		sys.exit('Select 2 objects please')
		
		
	bone_base = selection[0]
	bone_orient = selection[1]
	pmc.select(cl = True)

	get_name = str(bone_base)
	get_name = get_name.split('__')
	get_name = get_name[0] + '__half'

	half_bone = pmc.joint( n = get_name + '__anim', rad = 0.5)

	# display local axis (optional)
	
	#pmc.toggle(localAxis = True)
	


	half_bone_zero = pmc.group(half_bone, n=(get_name + '__zero'))
	
	pmc.parent(half_bone_zero, bone_base)
	half_bone_zero.setAttr('translate',[0,0,0])
	half_bone_zero.setAttr('rotate',[0,0,0])
	
	pmc.parentConstraint(bone_base,half_bone_zero, mo = False)
	pmc.scaleConstraint(bone_base,half_bone_zero, mo = False)
	pmc.parent(half_bone_zero, w = True)
	pmc.orientConstraint(bone_orient,half_bone, mo = False)
	
	pmc.setKeyframe(half_bone, at = 'rotate', time = 1)
	
	half_bone.setAttr('blendOrient1', 0.5)
	
	pairblend_node = pmc.listConnections(half_bone)
	in_rotate = pmc.listConnections((pairblend_node)[0])
	
	pairblend_node = pairblend_node[0]
	pairblend_node.rename(get_name + '_pairBlend')
	# passer mode de rotation du pairblend en quaternions
	# TESTER CA
	pairblend_node.setAttr('rotInterpolation', 1)
	# verifier sil faut vraiment supprimer le blend orient
	half_bone.deleteAttr('blendOrient1')
	
	pairblend_node.disconnectAttr('inRotateX1')
	pairblend_node.disconnectAttr('inRotateY1')
	pairblend_node.disconnectAttr('inRotateZ1')
	
	for each in in_rotate:
		test = pmc.nodeType(each)
		if test == 'animCurveTA':
			pmc.delete(str(each))

	if pmc.objExists('deform_rig__grp'):
		
		#CA CAY ELSA KAFAY
		pmc.parent(half_bone_zero, 'deform_rig__grp')
		
	else:
		pmc.createNode('transform', n='deform_rig__grp')
		pmc.parent(half_bone_zero, 'deform_rig__grp')