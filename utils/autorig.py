import maya.cmds as mc
import maya.mel as mel
import sys
from variables import *
import utils.save as save
import utils.shapes as shapes
reload(shapes)
# recuperer les bones / squelette entier. Replacer.
# Reconstruire squelette ?

# miroir locators R/L

mel.eval('source "cometJointOrient.mel";')
mel.eval('deleteUI "cometJointOrientWin"')


def override_color():

	import pymel.core as pmc

	sel = pmc.ls(sl=True)

	red = [1,0,0]
	green = [0,1,0]
	blue = [0,0,1]

	for each in sel:
		color_code=[0.5,0,1]
		break_name = each.split('_')
		if break_name[0] == 'l':
			color_code=blue
		elif break_name[0] == 'r':
			color_code=green
		elif break_name[0] == 'm':
			color_code=red
		else:
			raise ValueError('This node has no directional order.')
		pmc.setAttr(each.overrideEnabled,1)
		pmc.setAttr(each.overrideRGBColors,True)
		pmc.setAttr(each.overrideColorRGB,color_code)

	return color_code

def rot_in_jntorient():
	'''
	Experimental script.
	Not really functionnal at this point.

	'''
	j_ro = mc.xform(q=True, ro=True)
	j_or = mc.joint(q=True, o=True)

	j_mod = []
	for i in range(3):
		rep =  - j_ro[i] + j_or[i]
		j_mod.append(rep)

	mc.joint(e=True, o=j_mod)
	mc.xform(ro=[0,0,0], r=True)


def zero_out(sSel=None):
	'''
	makes a zero_out on top of the selected transform (joint or group).
	The zero_out is a group. The function will create a jnt on top on jnt, but not for now.
	Select a transfom, then run the script. zero_out(),
	You can also load the script by entering the name of the transform:

	zero_out('jnt_04')
	'''	

	returnList = []
	if not sSel:
		# Get Current selection
		sSel = mc.ls( sl = True )
	elif not isinstance(sSel,list):
		sSel = [sSel]

	sSel = sSel[0]
	print(sSel)
	# Get Parent
	s_parent = mc.listRelatives( sSel, p= True )
	if s_parent:
		s_parent= s_parent[0]

	# Get current Obj Transform
	lPos_Sel = mc.xform( sSel, q=True, t=True, ws=True )
	lRot_Sel = mc.xform( sSel, q=True, ro=True, ws=True )

	# Naming convention
	try:
		naming = sSel.split('__')
		naming.pop(-1)
		naming.append('zero')
		zero_name = '__'.join(naming)
	except:
		zero_name = sSel + '__zero'
	# Create a zero_out

	s_zero = mc.group(em=True, name= zero_name )
	
	# Set in place
	mc.xform( s_zero, a=True, t=lPos_Sel, ro=lRot_Sel, s=[1,1,1] )

	mc.parent( sSel, s_zero, relative= False)

	# reParent group to original parent
	if s_parent:
		mc.parent( s_zero, s_parent, relative= False )

	obj_type = mc.objectType(sSel)

	if obj_type == 'joint':

		mc.xform(sSel, ro=[0,0,0])
		mc.joint(sSel, e=True, o=[0,0,0])

		# dupliquer joint et le placer au meme endroit.

		sZero = mc.duplicate(sSel, po=True, n= zero_name + '___temp')
		mc.parent(sSel, sZero, r=False)
		if s_parent:
			mc.parent(sZero, s_parent)
		else:
			mc.parent(sZero, w=True)
		
		mc.delete(s_zero)
		mc.rename(sZero, zero_name)
		return sZero



def hand_attributes(sel=None):
	'''
	'''
	
	# selectionner controller Hand
		# lateralisation

	returnList = []
	if not sel:
		# Get Current selection
		sel = mc.ls( sl = True )
	elif not isinstance(sel,list):
		sel = [sel]

	if not len(sel) == 1:

		sys.exit('Only one controller must be selected !')

	sel = sel[0]

	selName = sel.split('_')

	if not selName[1] == 'wrist':

		sys.exit('Select a wrist please')

	lateralisation = selName[0]

	# ajouter Attributes

	print(sel)
	shapes.add_enum_attr(sel, 'customAttr')

	mc.addAttr(sel, ln='spread', niceName='Spread', at='float', min=-10, max=10, k=True)
	mc.addAttr(sel, ln='cup', niceName='Cup', at='float', min=0, max=10, k=True)
	# creer driven keys
		# selectionner les bones a bouger
	carps = ['carp_b_0_fk__zero','carp_c_0_fk__zero','carp_d_0_fk__zero','carp_e_0_fk__zero']
	fingers = ['finger_b_0_fk__zero','finger_c_0_fk__zero','finger_d_0_fk__zero','finger_e_0_fk__zero']

	carps = [w.replace('carp', lateralisation + '_carp') for w in carps]
	print(carps)
	fingers = [w.replace('finger', lateralisation + '_finger') for w in fingers]
	print(fingers)

	# spread comportement

	# e_carp drivenkey

	mc.setDrivenKeyframe(carps[-1], at='ry', cd=sel + '.spread', dv=0, v=0)
	mc.setDrivenKeyframe(carps[-1], at='ry', cd=sel + '.spread', dv=10, v=3)
	mc.setDrivenKeyframe(carps[-1], at='ry', cd=sel + '.spread', dv=-10, v=-7)

	# e_finger drivenkey

	mc.setDrivenKeyframe(fingers[-1], at='ry', cd=sel + '.spread', dv=0, v=0)
	mc.setDrivenKeyframe(fingers[-1], at='ry', cd=sel + '.spread', dv=10, v=6)
	mc.setDrivenKeyframe(fingers[-1], at='ry', cd=sel + '.spread', dv=-10, v=-17)

	# d_carp drivenkey

	mc.setDrivenKeyframe(carps[-2], at='ry', cd=sel + '.spread', dv=0, v=0)
	mc.setDrivenKeyframe(carps[-2], at='ry', cd=sel + '.spread', dv=10, v=2)
	mc.setDrivenKeyframe(carps[-2], at='ry', cd=sel + '.spread', dv=-10, v=-3.5)

	# d_finger drivenkey

	mc.setDrivenKeyframe(fingers[-2], at='ry', cd=sel + '.spread', dv=0, v=0)
	mc.setDrivenKeyframe(fingers[-2], at='ry', cd=sel + '.spread', dv=10, v=2.5)
	mc.setDrivenKeyframe(fingers[-2], at='ry', cd=sel + '.spread', dv=-10, v=-6)
	
	# c_carp drivenkey

	mc.setDrivenKeyframe(carps[1], at='ry', cd=sel + '.spread', dv=0, v=0)
	mc.setDrivenKeyframe(carps[1], at='ry', cd=sel + '.spread', dv=10, v=-0.5)
	mc.setDrivenKeyframe(carps[1], at='ry', cd=sel + '.spread', dv=-10, v=1)

	# c_finger drivenkey

	mc.setDrivenKeyframe(fingers[1], at='ry', cd=sel + '.spread', dv=0, v=0)
	mc.setDrivenKeyframe(fingers[1], at='ry', cd=sel + '.spread', dv=10, v=-0.5)
	mc.setDrivenKeyframe(fingers[1], at='ry', cd=sel + '.spread', dv=-10, v=0)

	# b_carp drivenkey

	mc.setDrivenKeyframe(carps[0], at='ry', cd=sel + '.spread', dv=0, v=0)
	mc.setDrivenKeyframe(carps[0], at='ry', cd=sel + '.spread', dv=10, v=-3)
	mc.setDrivenKeyframe(carps[0], at='ry', cd=sel + '.spread', dv=-10, v=6.5)

	mc.setDrivenKeyframe(carps[0], at='rx', cd=sel + '.spread', dv=0, v=0)
	mc.setDrivenKeyframe(carps[0], at='rx', cd=sel + '.spread', dv=-10, v=1)

	mc.setDrivenKeyframe(carps[0], at='rz', cd=sel + '.spread', dv=0, v=0)
	mc.setDrivenKeyframe(carps[0], at='rz', cd=sel + '.spread', dv=-10, v=1)

	# b_finger drivenkey

	mc.setDrivenKeyframe(fingers[0], at='ry', cd=sel + '.spread', dv=0, v=0)
	mc.setDrivenKeyframe(fingers[0], at='ry', cd=sel + '.spread', dv=10, v=-4)
	mc.setDrivenKeyframe(fingers[0], at='ry', cd=sel + '.spread', dv=-10, v=12)

	mc.setDrivenKeyframe(fingers[0], at='rz', cd=sel + '.spread', dv=0, v=0)
	mc.setDrivenKeyframe(fingers[0], at='rz', cd=sel + '.spread', dv=-10, v=-5)

	# connecter driven keys vers attributes

	# cup comportement

	# e_carp drivenkey

	mc.setDrivenKeyframe(carps[-1], at='rx', cd=sel + '.cup', dv=0, v=0)
	mc.setDrivenKeyframe(carps[-1], at='rz', cd=sel + '.cup', dv=0, v=0)

	mc.setDrivenKeyframe(carps[-1], at='rx', cd=sel + '.cup', dv=10, v=-23)
	mc.setDrivenKeyframe(carps[-1], at='rz', cd=sel + '.cup', dv=10, v=-15)

	# d_carp drivenkey

	mc.setDrivenKeyframe(carps[-2], at='rx', cd=sel + '.cup', dv=0, v=0)
	mc.setDrivenKeyframe(carps[-2], at='rz', cd=sel + '.cup', dv=0, v=0)

	mc.setDrivenKeyframe(carps[-2], at='rx', cd=sel + '.cup', dv=10, v=-7)
	mc.setDrivenKeyframe(carps[-2], at='rz', cd=sel + '.cup', dv=10, v=-4)



def create_ik():
	''' 
	Select a joint on the limb you wanna build an IK.
	You can select an arm, or leg. The limb must have 3 joints (0,1,x)
	'''

	# recuperer les fk auquels attacher les IKhandle


	sel = mc.ls(sl=True)

	if not len(sel) == 1:
		sys.exit('One object only must be selected.')

	# splitter le nom pour isoler

	sel = sel[0]
	break_name = sel.split('__')
	suffix = break_name[-1]
	break_name = break_name[0]
	break_name = break_name.split('_')


	side = break_name[0]
	leg_arm = break_name[1]

	print(break_name)

	# verifier que lon est bien sur le bon type dobjet. Plein de verifications...

	# 3eme element doit etre le numero du membre. 0,1 ou x.

	members_digit = ['0', '1', 'x']
	joint_sel = []


	if not break_name[2] in members_digit:

		sys.exit('you have not a limb selected (like an arm or a leg).')

	# recuperer les joints du membre

	if not break_name[2] == members_digit[-1]:

		break_name[2] = members_digit[-1]
		break_name = '_'.join(break_name)
		sel = break_name + '__' + suffix
		print(sel)

	sel_parent = mc.listRelatives(sel, p=True)
	sel_parent = sel_parent[0]

	sel_grandparent = mc.listRelatives(sel_parent, p=True)
	sel_grandparent = sel_grandparent[0]

	joint_sel.append(sel_grandparent)
	joint_sel.append(sel_parent)
	joint_sel.append(sel)

	print(joint_sel)

	# nommer ik dynamiquement


		# condition arm/leg

	if leg_arm == 'leg':

		ik_la = 'foot'

	elif leg_arm == 'arm':

		ik_la = 'hand'


	ik_name = side + '_' + ik_la + '_ik__util' 
	print(ik_name)
	# creer IKHandle.
	# Renommer IKHandle.

	mc.ikHandle(n=ik_name, sj=joint_sel[0], ee=joint_sel[-1], sol='ikRPsolver')
	# Parenter IKHandle.

	# PV. choper le FK_zero.

	sel_parent = mc.listRelatives(joint_sel[0], p=True)
	limb_zero = sel_parent[0]

	# Creer locator, offset et anim pour le PV

	pv_name = side + '_' + leg_arm + '_pv'

	pv_zero = mc.createNode('transform', n=pv_name + '__zero')
	pv_zero_offset = mc.createNode('transform', n=pv_name + '__zero_offset')
	pv_anim = mc.createNode('transform', n=pv_name + '__anim')

	# ajouter shape

	# optimiser !! (il faut pour linstant une shape nommee "CTRL_ball" dans la scene)

	temp_ctrl_pv = mc.duplicate('CTRL_ball', rr=True)
	temp_ctrl_pv = mc.listRelatives(temp_ctrl_pv, c=True)
	temp_ctrl_pv = temp_ctrl_pv[0]


	mc.rename(temp_ctrl_pv, pv_anim + '_shape')
	mc.parent(pv_anim + '_shape', pv_anim, s=True, r=True)
	mc.delete('CTRL_ball1')

	mc.parent(pv_anim, pv_zero_offset)
	mc.parent(pv_zero_offset, pv_zero)

	# placer le PV

	offset_value = 30

	if leg_arm == 'arm':

		offset_value = -offset_value

	if side == 'r':

		offset_value = -offset_value


	mc.xform(pv_zero_offset, t=[0,0,offset_value], ws=False)

	mc.parent(pv_zero, limb_zero)
	mc.xform(pv_zero, t=[0,0,0], ro=[0,0,0], ws=False)

	# Creer lien avec annotation (BONUS)


	# creer PV Constraint

	mc.poleVectorConstraint(pv_anim, ik_name)

	# Creer IK controller (zero, etc)

	ik_ctrl = side + '_' + ik_la + '_ik'

	ik_anim = mc.createNode('transform', n= ik_ctrl + '__anim')
	ik_zero = mc.createNode('transform', n= ik_ctrl + '__zero')

	mc.parent(ik_anim, ik_zero)

	# Placer le controller sur le dernier joint

	mc.parent(ik_zero, joint_sel[-1])
	mc.xform(ik_zero, t=[0,0,0], ws=False)
	mc.parent(ik_zero, w=True)

	mc.parent(ik_name, ik_anim)

	# Ajouter la shape de custom attributes sur les joints / controllers

	common_attr = mc.createNode('nurbsCurve', n=side + '_' + leg_arm + '_common_attributes')
	common_attr_parent = mc.listRelatives(common_attr, p=True)
	common_attr_parent = common_attr_parent[0]

	mc.parent(common_attr, ik_anim, s=True, r=True)
	mc.parent(common_attr, pv_anim, s=True, add=True)

	mc.delete(common_attr_parent)

	for each in joint_sel:

		mc.parent(common_attr, each, add=True, s=True)

	# Creer custom attributes

	fk_ik = 'fk_ik'
	mc.addAttr(common_attr, ln=fk_ik, niceName='FK/IK', at='float', min=0, max=1, k=True)

	mc.connectAttr(common_attr + '.' + fk_ik, ik_name + '.ikBlend')


def place_skeleton():

	# importer squelette
		# replacer neck dans dossier rig ainsi que les "__placer"
	
	mc.file(project_dir + '/utils/rig/skeleton_base.ma', i=True)


def build_skeleton():

	# recuperer les locators de placement

	placers = ['leg_0','leg_1','leg_x','arm_0','arm_1','arm_x','carp_b_0','finger_b_0','finger_b_1','finger_b_2','finger_b_x','carp_c_0','finger_c_0','finger_c_1','finger_c_2','finger_c_x','carp_d_0','finger_d_0','finger_d_1','finger_d_2','finger_d_x','carp_e_0','finger_e_0','finger_e_1','finger_e_2','finger_e_x']
	
	l_placers = []
	r_placers = []



	for each in placers:
		each = 'l_' + each + '__placer'
		l_placers.append(each)

	for each in placers:
		each = 'r_' + each + '__placer'
		r_placers.append(each)

	# recuperer les joints

	l_joints = []
	r_joints = []

	for each in placers:

		each_anim = 'l_' + each + '_fk' + '__anim'
		each_zero = 'l_' + each + '_fk' + '__zero'
		l_joints.append(each_anim)
		l_joints.append(each_zero)

	for each in l_joints:

		try:
			mc.select(each)
			mc.select(cl=True)

		except ValueError:
			l_joints.remove(each)

	for each in placers:

		each_anim = 'r_' + each + '_fk' + '__anim'
		each_zero = 'r_' + each + '_fk' + '__zero'
		r_joints.append(each_anim)
		r_joints.append(each_zero)

	for each in r_joints:

		try:
			mc.select(each)
			mc.select(cl=True)

		except ValueError:
			r_joints.remove(each)

	print(l_joints)
	print(r_joints)

	# placer les zeroOut sur les locators de placement

		# placer jambes

	w_pos = mc.xform(l_placers[0], q=True, t=True, ws=True)
	w_rot = mc.xform(l_placers[0], q=True, ro=True, ws=True)

	mc.xform(l_joints[1], t=w_pos, ro=w_rot, ws=True)

	w_pos = mc.xform(l_placers[1], q=True, t=True, ws=True)
	w_rot = mc.xform(l_placers[1], q=True, ro=True, ws=True)

	mc.xform(l_joints[2], t=w_pos, ro=w_rot, ws=True)


	w_pos = mc.xform(l_placers[2], q=True, t=True, ws=True)
	w_rot = mc.xform(l_placers[2], q=True, ro=True, ws=True)

	mc.xform(l_joints[3], t=w_pos, ro=w_rot, ws=True)


	mc.parent(l_joints[3], l_joints[2])
	mc.parent(l_joints[2], l_joints[0])


	# placer les coudes

	# Reparenter tout

	# orienter les joints avec CJO

	jointsToOrient = []

	jointsToOrient.append(l_joints[0])
	jointsToOrient.append(l_joints[1])
	jointsToOrient.append(l_joints[2])
	jointsToOrient.append(l_joints[3])

	aimAxis = [1.0, 0.0, 0.0]
	upAxis = [0.0, 1.0, 0.0]
	upDir = [0.0, 1.0, 0.0]

	jointsToOrientString = convertPythonArrayToMelArrayString(jointsToOrient)
	aimAxisString = convertPythonArrayToMelArrayString(aimAxis)
	upAxisString = convertPythonArrayToMelArrayString(upAxis)
	upDirString = convertPythonArrayToMelArrayString(upDir)

	autoGuessUpDirectionString = "0"

	melCommandString = "cJO_orient(" + jointsToOrientString + "," + aimAxisString + "," + upAxisString + "," + upDirString + "," + autoGuessUpDirectionString + ");"
	mel.eval(melCommandString)
	mel.eval(melCommandString)




def convertPythonArrayToMelArrayString(array):
	arrayString = str(array)
	arrayString = arrayString.replace('[', '{')
	arrayString = arrayString.replace(']', '}')
	arrayString = arrayString.replace('\'', '"')
	return arrayString



	# creer la spine

	# placer les tangentes sur les locators de placement de tangentes

	# connecter joints (bras)


def publish_rig():

	go_on = mc.confirmDialog(title='BEWARE', message = 'Importing References should be done ONLY when the asset is VALIDATED !! Continue ?', button =['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No')

	if go_on == 'No':

		sys.exit('Import Reference Aborted.')

	namespaces = mc.namespaceInfo(listOnlyNamespaces=True )
	print(namespaces)

	namespaces.pop(0)
	namespaces.pop(-1)
	
	print(namespaces)
	for each in namespaces:

		mc.namespace(removeNamespace=each, mnr=True)

	sel = mc.ls(references=True)
	print(sel)

	for each in sel:

		try:
			each = mc.referenceQuery(each,filename=True )
			mc.file(each, ir=True)
		except:
			print(str(each) + ' seems kinda weird or non existent.')
		# verifier quil ny ait que deux dossiers

		# --------------------------------------

	filename = mc.file(q=True, sn=True)
	charvalue = filename.split('/')

	# Verifier que l'on est dans le projet

	if not project_name in charvalue:
		sys.exit('You are not working in the Project !!')

	charvalue.pop(-1)
	charvalue.pop(-1)
	charvalue.pop(-1)

	asset_name = charvalue[-1]

	# remplacer nom du dossier "asset_name" par "mod"
	try:
		mc.rename(asset_name, 'mod')
	except RuntimeError:
		mc.warning('The folder containing the asset is not the same as the top group in the "mod" file.')
		mc.file(filename, open=True, force=True)
	# creer dossier "asset_name"

	asset_grp = mc.createNode('transform', n=asset_name)

	# parenter mod / rig au dossier asset_name

	mc.parent('mod', asset_grp)
	mc.parent('rig', asset_grp)

	# locker translates et scale

	import utils.selection as selection
	reload(selection)

	try:

		fk_to_lock = selection.by_name('*_fk__anim')

		for each in fk_to_lock:

			if 'spine' in each:

				mc.setAttr(each + '.sx', l=True, k=False, cb=False)
				mc.setAttr(each + '.sy', l=True, k=False, cb=False)
				mc.setAttr(each + '.sz', l=True, k=False, cb=False)

			elif not 'hips' in each:

				mc.setAttr(each + '.tx', l=True, k=False, cb=False)
				mc.setAttr(each + '.ty', l=True, k=False, cb=False)
				mc.setAttr(each + '.tz', l=True, k=False, cb=False)
				mc.setAttr(each + '.sx', l=True, k=False, cb=False)
				mc.setAttr(each + '.sy', l=True, k=False, cb=False)
				mc.setAttr(each + '.sz', l=True, k=False, cb=False)

	except ValueError:

		print('No *_fk__anim on this rig.')

	try:

		mc.setAttr('half_bones__utils.visibility', False)
		mc.setAttr('shapes.visibility', False)
		mc.setAttr('deform_rig__grp.visibility', False)

	except:

		print('Simple Rig apparently.')
	# sauver un master

	save.master(ask_version=False)


def foot_attr():

	sel= mc.ls(sl=True)

	if not len(sel) == 1:
		sys.exit('select only one object please.')

	name = sel[0].split('_')

	if not 'foot' in name:
		sys.exit('This object seems not to be a foot.')


	add_enum_attr(sel, longname='custom')
	add_float_attr(sel, longname='footRoll', min_value=-10.0, max_value=10.0)
	add_float_attr(sel, longname='bankLR', min_value=-10.0, max_value=10.0)
	add_float_attr(sel, longname='bankFB', min_value=-10.0, max_value=10.0)


def auto_bank_foot(amount=55.0):

	sel= mc.ls(sl=True)

	if not len(sel) == 1:
		sys.exit('select only one object please.')

	name = sel[0].split('_')

	if not 'foot' in name:
		sys.exit('This object seems not to be a foot.')


	children = mc.listRelatives(sel[0],ad=True, s=False, typ='transform')

	print(children)

	for each in children:

		if 'shape' in each:

			children.remove(each)

		if 'poleVector' in each:

			children.remove(each)

	print('new children :   ' + str(children))


	# define banking attributes

	bank_in = ''
	bank_out = ''
	bank_front = ''
	bank_up = ''

	for each in children:

		if not 'bank' in each:

			children.remove(each)



	print('new children :   ' + str(children))


	for each in children:

		sep_name = each.split('__')

		if sep_name[-1] == 'zero':

			print('le test de each     ' + each)
			children.remove(each)

	print('new children :   ' + str(children))


	for each in children:

		sep_name = each.split('__')
		sep_name = sep_name[0].split('_')


		if 'out' in sep_name:

			bank_out = each

		if 'in' in sep_name:

			bank_in = each
		
		if 'up' in sep_name:

			bank_up = each

		if 'front' in sep_name:

			bank_front = each


	print(bank_up)
	print(bank_in)
	print(bank_out)
	print(bank_front)


	banking_value = amount
	lateralisation = sel[0].split('_')
	
	if lateralisation[0] == 'r':

		banking_value = -banking_value

	mc.setAttr(sel[0] + '.bankLR', 0.0)
	mc.setAttr(bank_in + '.rotateZ', 0.0)
	mc.setAttr(bank_out + '.rotateZ', 0.0)
	mc.setDrivenKeyframe(bank_in + '.rotateZ', currentDriver=sel[0] + '.bankLR')
	mc.setDrivenKeyframe(bank_out + '.rotateZ', currentDriver=sel[0] + '.bankLR')

	mc.setAttr(sel[0] + '.bankLR', -10.0)
	mc.setAttr(bank_in + '.rotateZ', banking_value)
	mc.setDrivenKeyframe(bank_in + '.rotateZ', currentDriver=sel[0] + '.bankLR')

	mc.setAttr(sel[0] + '.bankLR', 10.0)
	mc.setAttr(bank_out + '.rotateZ', -banking_value)
	mc.setDrivenKeyframe(bank_out + '.rotateZ', currentDriver=sel[0] + '.bankLR')

	mc.setAttr(sel[0] + '.bankLR', 0.0)