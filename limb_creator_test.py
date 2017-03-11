# IK FK LIMB CREATOR

# NE FONCTIONNE SI LA CHAINE EST ALIGNEE SUR UN AXE !!

import maya.cmds as mc
import sys
import rivet

# Naming suffix

def naming_suffix(obj, suffix):

    naming = obj.split('__')
    naming.pop()
    naming.append(suffix)
    zero_name = '__'.join(naming)

    return zero_name

# Miroir
 
def mirror_joints(base_joint):
    
    result = mc.promptDialog(
	    	title='Mirror Joints',
    		text='',
    		message='Choose Axis (XY, YZ, XZ) :',
    		button=['OK', 'Cancel'],
    		defaultButton='OK',
    		cancelButton='Cancel',
    		dismissString='Cancel')
    
    if result == 'Cancel':
        
        print('No mirror Applied')
        return

    breakdown_name = base_joint[0].split('_')
    side = breakdown_name[0]
    
    if side == 'l':
        
        side_opp = 'r'
        
    elif side == 'r':
        
        side_opp = 'l'
        
    else:
    	sys.exit('No left of right. Wrong argument.')
    	
    m_axis = mc.promptDialog(text=True,q=True)
    
    if m_axis == 'XY':
        
        mir_joint = mc.mirrorJoint(base_joint, mb=True, mirrorXY=True, searchReplace=(side + '_', side_opp + '_'))
        t_distance = mc.getAttr(base_joint + '.translateZ')
        mc.setAttr(mir_joint[0] + '.translateZ', -(t_distance))
        
    if m_axis == 'YZ':
        
        mir_joint = mc.mirrorJoint(base_joint, mb=True, mirrorYZ=True, searchReplace=(side + '_', side_opp + '_'))
        t_distance = mc.getAttr(base_joint + '.translateX')
        mc.setAttr(mir_joint[0] + '.translateX', -(t_distance))

    if m_axis == 'XZ':
        
        mir_joint = mc.mirrorJoint(base_joint, mb=True, mirrorXZ=True, searchReplace=(side + '_', side_opp + '_'))
        t_distance = mc.getAttr(base_joint + '.translateY')
        mc.setAttr(mir_joint[0] + '.translateY', -(t_distance))


    print('MIROIR ====>   ')
    print(mir_joint)
    
    mir_joint.pop(0)
    
    return mir_joint
    
    
#----- Zero out ------


def zero_out(sSel):
    ''''''    
    # Get Parent
    s_parent = mc.listRelatives( sSel, p= True )
    if s_parent:
        s_parent= s_parent[0]

    # Get current Obj Transform
    lPos_Sel = mc.xform( sSel, q=True, t=True, ws=True )
    lRot_Sel = mc.xform( sSel, q=True, ro=True, ws=True )

    # Naming convention
    
    zero_name = naming_suffix(sSel, 'zero')

    # Create a zero_out
    
    obj_type = mc.objectType(sSel)
    
    if obj_type == 'joint':
        
        s_zero = mc.joint(name= zero_name )
        mc.parent(s_zero, w=True )
    else:
        s_zero = mc.group(em=True, name= zero_name )
        
    # Set in place
    mc.xform( s_zero, a=True, t=lPos_Sel, ro=lRot_Sel, s=[1,1,1] )
    # Parent current to orig Group
    mc.parent( sSel, s_zero, relative= False)

    # reParent group to original parent
    if s_parent:
        mc.parent( s_zero, s_parent, relative= False )
        
    return(s_zero)


def create_ik(jnt_sel):


    breakdown_name = jnt_sel[0].split('_')
    print(breakdown_name)
    del breakdown_name[-4:]
    print(breakdown_name)
    name_base = '_'.join(breakdown_name) + '_'

    joint_zero = naming_suffix(jnt_sel[0], 'zero')
    
    
    mc.ikHandle( sj= jnt_sel[0], ee= jnt_sel[2], sol='ikRPsolver', n=name_base + 'ik__util')
    ik_handle = name_base + 'ik__util'
    ik_zero = zero_out(ik_handle)

 
    
    ik_name = naming_suffix(ik_zero, 'anim')
    mc.rename(ik_zero, ik_name)
    
    ik_shape = mc.circle(nr = (1,0,0), r=2, d=1, s=4, n= name_base + 'ik__ctrl')
    s_shape = mc.listRelatives(ik_shape, s=True)
    mc.parent(s_shape[0], ik_name, s=True, r=True)
    mc.delete(ik_shape)
    
    ik_zero = zero_out(ik_name)
    
    #locker le ik_handle
    
    mc.setAttr(ik_handle + '.tx', lock=True)
    mc.setAttr(ik_handle + '.ty', lock=True)
    mc.setAttr(ik_handle + '.tz', lock=True)
    
    # Creation du Pole Vector
    
    pv_shape = mc.curve(
            d = 1,
            p=[(-3.09086e-008,0,0.707107),
            (-0.707107, 0, -6.18172e-008),
            (9.27258e-008, 0, -0.707107),
            (0.707107, 0, 0),
            (0, 0.707107, 0),
            (9.27258e-008, 0, -0.707107),
            (0.707107, 0, -6.18172e-008),
            (0, 0.707107, 0),
            (-3.09086e-008, 0, 0.707107),
            (0.707107, 0, 0),
            (0, -0.707107, 0),
            (9.27258e-008, 0, -0.707107),
            (-0.707107, 0, -6.18172e-008),
            (0, -0.707107, 0),
            (-3.09086e-008, 0, 0.707107),
            (-0.707107, 0, 0),
            (0, 0.707107, 0)])    
    
    
    pole_vector = mc.group(em=True, name=name_base + 'ik_pv__anim')
    s_shape = mc.listRelatives(pv_shape, s=True)
    mc.parent(s_shape, pole_vector, s=True, r=True)
    mc.delete(pv_shape)
    mc.parent(pole_vector, joint_zero)
    mc.xform(pole_vector, ro=(0,0,0), t=(0,0,0))
    zero_out(pole_vector)
    
    mc.poleVectorConstraint(pole_vector, ik_handle)
    
    # Ajouts de Controllers FK
    
    for each in jnt_sel[:-1]:
        
        ctrl_shape = mc.circle(nr = (1,0,0), n=each+'__ctrl')
        s_shape = mc.listRelatives(ctrl_shape, s=True)
        mc.parent(s_shape[0], each, s=True, r=True)
        mc.delete(ctrl_shape)
        
    # Ajout du Controller Global
    
    global_shape = mc.circle(nr = (1,0,0), r=0.5, d=1, n= name_base + 'global__TEMP')
    s_shape = mc.listRelatives(global_shape, s=True)
    mc.rename(s_shape[0], name_base + 'global__ctrl')
    s_shape = mc.listRelatives(global_shape, s=True)
    global_shape = s_shape[0]
    mc.parent(global_shape, 'TEMP__grp')
    mc.setAttr(global_shape + '.visibility', 0)
    
    # Ajout de parametres sur le controller global (en ajouter plein ici)
    
    mc.addAttr(global_shape, ln='fkik', nn='FK/IK', at='float', min=0.0, max=1.0, dv=0.0, k=True, hidden=False)
    mc.connectAttr(global_shape+'.fkik',ik_handle+'.ikBlend')
    
    # Placer le Controller sur chaque endroit ou on le souhaite
    
    all_ctrls = jnt_sel
    all_ctrls.append(ik_name)
    all_ctrls.append(pole_vector)
    
    for each in all_ctrls:
        
        mc.parent(global_shape, each, s=True, r=True, add=True)

    limb_grp = mc.group(em=True, n=name_base + '_grp')
    mc.parent(limb_grp, joint_zero)
    mc.xform(limb_grp, t=(0,0,0), ro=(0,0,0), a=True)
    mc.parent(limb_grp, w=True)
    mc.parent(ik_zero, limb_grp)
    mc.parent(joint_zero, limb_grp)

    
#----- FONCTION PRINCIPALE  ---

def create_limb(limb_pos, limb_name, aim_axis, up_axis):
    
    if up_axis == aim_axis:
        
        sys.exit('Aim and Up axis are the same ones !!') 
    
    axis = [aim_axis,up_axis]
    
    for idx, vector in enumerate(axis):
        
        if vector == 'x':
            
            vector = (1,0,0)
            
        elif vector == 'y':
            
            vector = (0,1,0)
            
        elif vector == 'z':
            
            vector = (0,0,1)
        
        else:
            sys.exit('Axe non valide !')
        
        axis[idx] = vector

    print(axis)
    
    aim_axis = axis[0]
    up_axis = axis[1]
    
    print(up_axis)

    print('aim_axis == '+ str(aim_axis))
    print('up_axis == '+ str(up_axis))
    loc_sel = mc.ls(sl = True)
    if not len(loc_sel) == 3:
        
    	sys.exit('You must select 3 locators for creating a limb.')
    
    
    if not mc.objExists('TEMP__grp'):
        temp_grp = mc.group(em=True, n='TEMP__grp')
    
    #mc.select('locator1','locator2','locator3', r=True)
    
    
    
    if limb_pos == 'l':
        limb_opp = 'r'
    elif limb_pos == 'r':
        limb_opp = 'l'
    else:
    	sys.exit('No left of right. Wrong argument.')
    
    name_base = limb_pos + '_' + limb_name + '_'
    
    
    
    
    jnt_sel =[]
    
    for each in loc_sel:
        
        print(each)
        jnt = mc.createNode('joint')
        mc.parent(jnt, each)
        mc.xform(jnt, t=(0,0,0) )
        mc.parent(jnt, w=True)
        jnt_sel.append(jnt)
    
    print(jnt_sel)
    mc.rename(jnt_sel[0], name_base + 'fk_0__anim')
    mc.rename(jnt_sel[1], name_base + 'fk_1__anim')
    mc.rename(jnt_sel[2], name_base + 'fk_x__anim')
    
    jnt_sel =[]
    jnt_sel.append(name_base + 'fk_0__anim')
    jnt_sel.append(name_base + 'fk_1__anim')
    jnt_sel.append(name_base + 'fk_x__anim')
    
    
# GET TRIPLANAR NORMAL

    coords = []
    
    for each in loc_sel:
        
        pos = mc.xform(each, q=True, t=True)
        coords.append(pos)
        
    
    
    poly = mc.polyCreateFacet(p = coords)
    
    normals = mc.polyInfo(poly[0], faceNormals=True)
    mc.polyNormal(nm=0)
    print(normals)
    
    rivet.ch4_rivet(name_base+'__normal')
    
    limb_normal = name_base + '__normal'
    
    print(limb_normal)
    
    
    # ZeroOut sur le premier Joint
    
    n_Rot = mc.xform(limb_normal, q=True, ro=True)
    
    for each in jnt_sel:
        
        mc.xform(each, ro=n_Rot)

    sys.exit('dfgdfg')


    if up_axis == (0,1,0):
        
        mc.xform(jnt_sel[1], ro=(0,0,0), roo = 'yxz')
    
    elif up_axis == (0,0,1):
    
        mc.xform(jnt_sel[1], ro=(0,0,0), roo = 'zxy')
        
    elif up_axis == (1,0,0):
    
        mc.xform(jnt_sel[1], ro=(0,0,0), roo = 'zyx') 
           
    temp_x = mc.getAttr(jnt_sel[2] + '.rotateX')
    temp_y = mc.getAttr(jnt_sel[2] + '.rotateY')
    temp_z = mc.getAttr(jnt_sel[2] + '.rotateZ')
    mc.setAttr(jnt_sel[2] + '.jointOrientX', 0)
    mc.setAttr(jnt_sel[2] + '.jointOrientY', 0)
    mc.setAttr(jnt_sel[2] + '.jointOrientZ', 0)
    
    mc.xform(jnt_sel[2], r=True, ro=(0,0,0))
    mc.parent(jnt_sel[2], w=True)
    
    # Parenter les joints entre eux
    
    mc.parent(jnt_sel[2], jnt_sel[1])
    mc.parent(jnt_sel[1], jnt_sel[0])

    flip_bone = mc.getAttr(jnt_sel[1] + '.jointOrientX')

    if abs(flip_bone) == 180:
        
        mc.setAttr(jnt_sel[1] + '.jointOrientX', 0)
        
        
    # Miroir
    jnt_sel_mir = mirror_joints(joint_zero)
    
    # CHANGER DE FONCTION ICI
    
    # Creer IK
    create_ik(jnt_sel)
    create_ik(jnt_sel_mir)
    
    mc.confirmDialog(t= 'Warning !!!',m='Ne pas oublier de regler les axes de rotation TOUT DE SUITE')    


create_limb('l','arm','x','y')