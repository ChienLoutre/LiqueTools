from maya import cmds
import math

from library import Vector, create_orig_on_selected, create_bones_from_length
from constants import *


'''

import rigTools
reload(rigTools)

nbjoints = 6

rigTools.deform.create_stretchySpline(
	'l_arm',
	'l_arm_fk_0_anim',
	start_hook='l_arm_fk_0_half_anim',
	end_hook='l_arm_fk_1_half_anim',
	nb_joints = nbjoints) 

rigTools.deform.create_stretchySpline(
	'l_forearm',
	'l_arm_fk_1_anim',
	start_hook='l_arm_fk_1_half_anim',
	end_hook='l_arm_fk_x_half_anim',
	nb_joints = nbjoints)
	
'''

def create_stretchySpline( name, main_bone_ctrl, nb_joints = 3, start_hook=None, end_hook=None, axis = 'x', upaxis = 'y'):
	'''
		create stretchy Spine rig 
		
		args:
			name (srt) name of module created
			main_bone_ctrl (str) name of bone ctrl where the module is attached
			nb_joints (int): number of sections joints spread on spline curve
		
		options:
			start_hook (str) name of start half bone where start tangent will be hooked
			end_hook (str) name of end half bone where end tangent will be hooked
			axis (str) enum : x,-x ,y,-y,z,-z main_bone_ctrl length axis
			upaxis (str) enum : x,-x ,y,-y,z,-z main_bone_ctrl flexion axis
	'''
	if axis:
		axis = axis.lower()
	
	if upaxis:
		upaxis = upaxis.lower()
		
	# attributes
	stretchSquashAttribute = 'stretchSquahAmplitude'
	controlAttribute = 'stretchSquash_profile'
	bendyAttribute = 'bendy'
	
	# mapping of axis to vectors and indexes in spline ikhandle
	# axis_mapping['x'][0] ---> index in splineIkHandle main axis
	# axis_mapping['x'][1] ---> [1.0,0,0] vector corresponding to 'x'
	
	axis_mapping = {'x':[0,[1.0,0,0]],
					'-x':[1,[-1.0,0,0]],
					'y':[2,[0,1.0,0]],
					'-y':[3,[0,-1.0,0]],
					'z':[4,[0,0,1.0]],
					'-z':[5,[0,0,-1.0]]
					}

	up_axis_mapping = {'x':[6,[1.0,0,0]],
					'-x':[7,[-1.0,0,0]],
					'y':[0,[0,1.0,0]],
					'-y':[1,[0,-1.0,0]],
					'z':[3,[0,0,1.0]],
					'-z':[4,[0,0,-1.0]]
					}

	# prepare rig hierarchy
	rig_grp = name + RIG_GRP
	if not cmds.objExists(rig_grp):
		rig_grp = cmds.createNode('transform',n=rig_grp)
	
	noXform_grp = name + NOXFORM_GRP
	if not cmds.objExists(noXform_grp):
		noXform_grp = cmds.createNode('transform',n=noXform_grp)
		cmds.setAttr(noXform_grp+'.visibility',False)

	noXform_parent = cmds.listRelatives(noXform_grp,p=True)

	if not noXform_parent or ( noXform_parent and noXform_parent[0] is not rig_grp):
		cmds.parent(noXform_grp,rig_grp)

	# set no xform to world space when ever rig_grp moves	
	cmds.setAttr(noXform_grp+'.inheritsTransform',False)
		
	# get start pos and end pos
	main_bone_ctrl_pos = cmds.xform(main_bone_ctrl,q=True,ws=True,t=True)
	
	if end_hook:
		end_hook_pos = cmds.xform(end_hook,q=True,ws=True,t=True)
		# compute direction and length from start_point to end_point
		vec_start = Vector(main_bone_ctrl_pos[0],main_bone_ctrl_pos[1],main_bone_ctrl_pos[2])
		vec_end = Vector(end_hook_pos[0],end_hook_pos[1],end_hook_pos[2])
		vec_start_to_end = vec_end - vec_start
		length = vec_start_to_end.norm()
	
	# create deform joints chain
	cmds.select (clear=True)
	jointList = create_bones_from_length(nb_joints,1.0,axis= axis_mapping[axis][1],name=name, suffix=JNT_SUFFIX)
	startJoint = jointList[0]
	endJoint = jointList[-1]
	cmds.parent(startJoint,  noXform_grp)
	
	# create ik spline handle
	ikH, eff, crv = cmds.ikHandle(  startJoint=startJoint, 
								endEffector=endJoint,
								createCurve=True, 
								sol='ikSplineSolver',
								numSpans=1,
								parentCurve=True,
								rootOnCurve=True,
								rootTwistMode=True,
								simplifyCurve=True
								)
	
	crv = cmds.rename(crv, name+CRV_SUFFIX)
	ikH = cmds.rename(ikH, name+IKH_SUFFIX)
	cmds.parent(ikH, noXform_grp)
	
	crvShape = cmds.listRelatives(crv, s=True)[0]
	
	# create Manips
	cmds.select(cl=True)
	
	listManip = []
	
	for cvId,manip in enumerate(SPLINE_MANIPS):
		point_pos = cmds.xform( crvShape + ".controlPoints[%s]" % cvId, q=True, ws=True, t=True )
		jnt = cmds.joint(p=point_pos, a=True, n= name + manip + CTRL_SUFFIX)
		cmds.setAttr(jnt+'.overrideEnabled',True)
		cmds.setAttr(jnt+'.overrideColor',IKCOLOR_ID)
		listManip.append(jnt)
	
	start_manip = listManip[0]
	end_manip = listManip[-1]
	
	# set display as tangent(line) 
	cmds.setAttr(start_manip + '.radius',0)
	cmds.setAttr(end_manip + '.radius',0)
	
	print(start_manip)
	print(end_manip)
	# inverse parenting of end_manip and end_tangent
	cmds.parent(end_manip,w=True)
	cmds.parent(listManip[-2],end_manip)
	
	start_manip_zero,startTangent_zero,endTangent_zero,end_manip_zero = create_orig_on_selected(cSelection=listManip)
	cmds.parent([start_manip_zero,end_manip_zero], rig_grp)
	
	# create locator at zeros position for global scale
	locBase = cmds.createNode('locator',n=start_manip_zero.replace(ZERO_SUFFIX,LOC_SUFFIX),p=start_manip_zero)
	cmds.setAttr(locBase+'.v',False)
	
	locEnd = cmds.createNode('locator',n=end_manip_zero.replace(ZERO_SUFFIX,LOC_SUFFIX),p=end_manip_zero)
	cmds.setAttr(locEnd+'.v',False)
	
	dbw_globalScale = cmds.createNode('distanceBetween',n=name+ 'GlobalScale' +DBW_SUFFIX)
	
	cmds.connectAttr(locBase +'.worldPosition[0]', dbw_globalScale+'.point1')
	cmds.connectAttr(locEnd+'.worldPosition[0]', dbw_globalScale+'.point2')
	
	# do curve Skinning to manips
	skinCluter = cmds.skinCluster(listManip,crvShape)[0]
	for iter,jnt in enumerate(listManip):
		cmds.skinPercent(skinCluter,crvShape + '.controlPoints[%s]' % iter ,transformValue=[(jnt, 1.0)])
	
	# add rebuilds curve for sliding effect
	# because of buggy rebuild fitRebuild mode create first linear with 4 points  
	rebuild0 = cmds.rebuildCurve(crvShape, ch=True,fitRebuild=False, rpo=True,rebuildType=0,end=True,kr=0, kcp=False, kep=True, kt=False,s=4, d=1, tol=0.01)
	# add an other rebuild node with fitRebuild on with 3 spans minimum and in quadratic parametrisation
	rebuild1 = cmds.rebuildCurve(crvShape, ch=True,fitRebuild=True, rpo=True,rebuildType=0,end=True,kr=0, kcp=False, kep=True, kt=False,s=4, d=2, tol=0.01)
	
	# set twist behavior of ikSpline
	cmds.setAttr(ikH+'.visibility', False)
	cmds.setAttr(ikH+'.dTwistControlEnable', True)
	cmds.setAttr(ikH+'.dWorldUpType',4)
	
	cmds.setAttr(ikH+'.dForwardAxis',axis_mapping[axis][0])
	
	cmds.setAttr(ikH+'.dWorldUpAxis',up_axis_mapping[upaxis][0])
	
	cmds.setAttr(ikH+'.dWorldUpVector',
					axis_mapping[upaxis][1][0],
					axis_mapping[upaxis][1][1],
					axis_mapping[upaxis][1][2],
					type='double3')
	
	cmds.setAttr(ikH+'.dWorldUpVectorEnd',
					axis_mapping[upaxis][1][0],
					axis_mapping[upaxis][1][1],
					axis_mapping[upaxis][1][2],
					type='double3')
	
	cmds.connectAttr(start_manip + '.worldMatrix[0]' ,ikH+'.dWorldUpMatrix')
	cmds.connectAttr(end_manip + '.worldMatrix[0]' ,ikH+'.dWorldUpMatrixEnd')
	
	# populate pointOnCurve
	prev_loc = None
	locs = []
	for iter,jnt in enumerate(jointList):
		# create locator at current joint position
		loc, = cmds.spaceLocator(n=jnt.replace(JNT_SUFFIX,LOC_SUFFIX))
		locs.append(loc)
		cmds.setAttr(loc+'.v',False)
		# create pointOnCurveInfo node
		poc = cmds.createNode('pointOnCurveInfo',n=jnt.replace(JNT_SUFFIX,POC_SUFFIX))
		# compute parametric value of current joint
		param = 1.0*iter/(len(jointList)-1)
		# set param value and percentage settings to pointOnCurveInfo
		cmds.setAttr(poc+'.parameter',param)
		cmds.setAttr(poc + '.turnOnPercentage',True)
		# connect curve to pointOnCurveInfo
		cmds.connectAttr(crvShape + '.worldSpace[0]', poc+'.inputCurve')
		# connect output of pointOnCurveInfo to locator 
		cmds.connectAttr(poc+'.result.position',loc+'.t')
		# now create distanceBetween
		
		if iter >0:
			dbw = cmds.createNode('distanceBetween',n=jnt.replace(JNT_SUFFIX,DBW_SUFFIX))
			cmds.connectAttr(prev_loc +'.worldPosition[0]', dbw+'.point1')
			cmds.connectAttr(loc+'.worldPosition[0]', dbw+'.point2')
			# create multiply divide node for length axis choice
			md = cmds.createNode('multiplyDivide',n=jnt.replace(JNT_SUFFIX,MD_SUFFIX))
			cmds.setAttr(md+'.input2',
						 axis_mapping[axis][1][0],
						 axis_mapping[axis][1][1],
						 axis_mapping[axis][1][2],
						 )
						 
			cmds.connectAttr(dbw+'.distance', md +'.input1.input1X')
			cmds.connectAttr(dbw+'.distance', md +'.input1.input1Y')
			cmds.connectAttr(dbw+'.distance', md +'.input1.input1Z')
			# connect multiplyDivide result ex: [ 1.0*distance, 0*distance, 0*distance ]
			cmds.connectAttr(md + '.output',jnt+'.t')
		
		prev_loc = loc
		
	cmds.parent(locs, noXform_grp)
	
	# create squash Expression
	curveInfoNode = cmds.createNode('curveInfo',n=crv.replace(CRV_SUFFIX,CRVLEN_SUFFIX) )
	cmds.connectAttr(crvShape + '.worldSpace[0]',curveInfoNode+'.inputCurve' )
	# now that we have the objects, we can create the animation curve which will control the attribute
	
	
	objAttr = (rig_grp + '.' + controlAttribute)
	if not cmds.objExists(objAttr):
		cmds.addAttr(rig_grp, ln= controlAttribute, at= 'double', k=True )
	
	strSqAmpAttr = (rig_grp + '.' + stretchSquashAttribute)
	if not cmds.objExists(strSqAmpAttr):
		cmds.addAttr(rig_grp, ln= stretchSquashAttribute, at= 'double', k=True, min=0, dv=1.0 )
	
	cmds.setKeyframe(rig_grp,at=controlAttribute, t=1,v=0)
	cmds.setKeyframe(rig_grp,at=controlAttribute, t=nb_joints+1,v=0)
	
	cmds.keyTangent(rig_grp, wt=1, at=controlAttribute)
	cmds.keyTangent(rig_grp, weightLock=False, at=controlAttribute)
	
	
	cmds.keyTangent(objAttr,e=True, a=True, t=(1,1), outAngle= 50)
	cmds.keyTangent(objAttr,e=True, a=True, t=(nb_joints+1,nb_joints+1), outAngle= -50)
	
	# create the frameCache node
	frameCache = cmds.createNode( 'frameCache',n=crv.replace(CRV_SUFFIX,FC_SUFFIX) )
	cmds.connectAttr( objAttr, frameCache + '.stream')
	cmds.setAttr(frameCache + '.vt' , 0)
	cmds.setAttr(frameCache + '.frozen' , True)
	#cmds.setAttr(frameCache + '.nodeState' , 2)
	
	# find squash axis from length axis
	xyz = axis_mapping[axis][1]
	x = abs(abs(xyz[0])-1)
	y = abs(abs(xyz[1])-1)
	z = abs(abs(xyz[2])-1)
	
	txt = ('// INPUTS\n'+
		'vector $axis = <<'+str(x)+','+str(y)+','+str(z)+'>>;\n'+
		'$distance_actuelle = '+ curveInfoNode +'.arcLength;\n'+
		'$stretchSquashAmplitude = '+ rig_grp +'.stretchSquahAmplitude;\n'
		)
		   
	for jntId in xrange(len(jointList)):
	   txt += '$val_'+str(jntId)+' = '+frameCache+'.future['+str(jntId) + ']*$stretchSquashAmplitude;\n'
	
	txt +=('\n'+
		   '// CONSTANTS\n'+
		   '$distance_initiale = ' + dbw_globalScale + '.distance;\n'+
		   '\n'+
		   '// COMPUTE\n'+
		   '$rapport_stretch = $distance_actuelle / $distance_initiale;\n'+
		   '$volumicScale = 1.0/sqrt($rapport_stretch);\n'+
		   '\n'+
		   '// OUTPUTS\n'
		   )
	jointList.remove(jointList[-1])
	for iter,jnt in enumerate(jointList):
		txt += jnt+'.scaleX = pow($volumicScale,$axis.x*$val_'+str(iter)+');\n'
		txt += jnt+'.scaleY = pow($volumicScale,$axis.y*$val_'+str(iter)+');\n'
		txt += jnt+'.scaleZ = pow($volumicScale,$axis.z*$val_'+str(iter)+');\n'
		
	cmds.expression(n=name+'keepVolume'+EXP_SUFFIX,s=txt,ae=1,uc='all')
	
	# parent constraint module
	cmds.parentConstraint(main_bone_ctrl, rig_grp)
	
	
	if start_hook:
		cmds.parentConstraint(start_hook,start_manip_zero)

	if end_hook:
		# set length by scale to get different size according to bone ctrl length
		cmds.setAttr(rig_grp+'.scale',length,length,length,type='double3')
		cmds.parentConstraint(end_hook,end_manip_zero)

		
	# add bendy attribute to hooks if it doesn't exist
	hooks = (start_hook,end_hook)
	tangZeros = (startTangent_zero,endTangent_zero)
	
	for hook,tangZero in zip(hooks,tangZeros):
		bendy_attr = hook + '.' + bendyAttribute
		drivenAxis = axis.rpartition('-')[2]
		tang_attr = tangZero + '.translate'+drivenAxis.upper()
		
		if not cmds.objExists(bendy_attr):
			bendy_attr = cmds.addAttr(hook, ln= bendyAttribute, at= 'double', k=True,min=0.0, max=1.0 )
		
		default_tang_length = cmds.getAttr(tang_attr)
		cmds.setDrivenKeyframe(tang_attr, currentDriver=bendy_attr, driverValue=1,value=default_tang_length, itt='linear' )
		cmds.setDrivenKeyframe(tang_attr, currentDriver=bendy_attr, driverValue=.00001, value=0, itt='linear' )
