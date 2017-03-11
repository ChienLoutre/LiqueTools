# Animation scripts
import maya.cmds as mc
import sys
from variables import *
import utils.get_extension as ext
import padding_numbers

def fix_obj_to_prev_frame(sel=None):

	if not sel:
		# Get Current selection
		sel = mc.ls( sl = True )

	elif not isinstance(sel,list):
		sel = [sel]


	if len(sel) != 1:

		sys.exit('Select one object ONLY please.')

	sel = sel[0]

	time = int(mc.currentTime(q=True))

	mc.currentTime(time-1)

	x_pos = mc.xform(sel, q=True, t=True, ws=True)
	x_rot = mc.xform(sel, q=True, ro=True, ws=True)


	temp_loc = mc.createNode('transform', n='temporary_grp')

	mc.xform(temp_loc, t=x_pos, ro=x_rot, ws=True)

	mc.currentTime(time)

	sel_dad = mc.listRelatives(sel, p=True)
	sel_dad = sel_dad[0]

	caca = mc.parent(temp_loc, sel_dad)

	x_pos = mc.xform(temp_loc, q=True, t=True, ws=True)
	x_rot = mc.xform(temp_loc, q=True, ro=True, ws=True)

	mc.xform(sel, t=x_pos, ro=x_rot, ws=True)

	mc.delete(temp_loc)

	# go to next frame

	mc.currentTime(time+1)

	mc.select(sel)

def fix_obj_to_prev_key(sel=None):

	if not sel:
		# Get Current selection
		sel = mc.ls( sl = True )

	elif not isinstance(sel,list):
		sel = [sel]


	if len(sel) != 1:

		sys.exit('Select one object ONLY please.')

	sel = sel[0]

	time = int(mc.currentTime(q=True))

	last_key = mc.findKeyFrame(time=time, which='previous')

	mc.currentTime(last_key)

	frame_range = time-int(last_key)

	for i in range(frame_range):


		x_pos = mc.xform(sel, q=True, t=True, ws=True)
		x_rot = mc.xform(sel, q=True, ro=True, ws=True)


		temp_loc = mc.createNode('transform', n='temporary_grp')

		mc.xform(temp_loc, t=x_pos, ro=x_rot, ws=True)

		mc.currentTime(time)

		sel_dad = mc.listRelatives(sel, p=True)
		sel_dad = sel_dad[0]

		caca = mc.parent(temp_loc, sel_dad)

		x_pos = mc.xform(temp_loc, q=True, t=True, ws=True)
		x_rot = mc.xform(temp_loc, q=True, ro=True, ws=True)

		mc.xform(sel, t=x_pos, ro=x_rot, ws=True)

		mc.delete(temp_loc)

		# go to next frame

		mc.currentTime(time+1)

		mc.select(sel)

def mirror_controller(sel=None):
	'''
	WIP
	WIP
	WIP
	'''
	if not sel:
		# Get Current selection
		sel = mc.ls( sl = True )

	elif not isinstance(sel,list):
		sel = [sel]

	for each in sel:
		
		namespace=None
		try:
			namespace_split = each.split(':')
			namespace = namespace_split[0]
			each = namespace_split[-1]

		except ValueError:
			pass

		name_split = each.split('_')
		lateral = name_split[0]
		opp_ctrl_name = ''

		if (lateral not in ['l','r']):
			print('Controller "' + each + '" is not a on a side.')

		elif lateral == 'l':
			name_split.pop(0)
			opp_ctrl_name = 'r_' + '_'.join(name_split) 

		elif lateral == 'r':
			name_split.pop(0)
			opp_ctrl_name = 'l_' + '_'.join(name_split)

		print(opp_ctrl_name)

		if namespace != None:

			each = namespace + ':' + each
			opp_ctrl_name = namespace + ':' + opp_ctrl_name

		pos = mc.xform(each, q=True, t=True, r=True)
		rot = mc.xform(each, q=True, ro=True, r=True)

		try:
			mc.xform(opp_ctrl_name, ro=rot, a=True)
		except:
			pass


def make_playblast(hd=False, master=False):

	pb_wh = [1280,720]
	qual = 70
	overwrite = False
	# get folder location

	# verifier la sauvegarde avant de faire la creation d'un shot...

	filename = mc.file(q=True, sn=True)
	charvalue = filename.split('/')

	# Verifier que l'on est dans le projet

	if not project_name in charvalue:
		sys.exit('You are not working in the Project !!')

	if not 'seq' in charvalue:
		sys.exit('This is not a sequence...')

	# get sequence/shot location
	current_shot = None
	current_seq = charvalue[5]
	shot_path = project_dir + '/prod/seq/' + current_seq

	if 'shots' in charvalue:
		current_shot = charvalue[7]
		shot_path += '/shots/' + current_shot

	# playblast location

	pb_path = shot_path + '/playblasts/'
	print(pb_path)
	sh_name = None
	# renaming the playblast file

	path_versions = os.listdir(pb_path)
	print(path_versions)
	if not path_versions:
		print('lol')
	else:
		pb_name = path_versions[-1]

	if 'shots' in charvalue:
		if not path_versions:
			pb_name = 'pb_000.mov'
		else:
			indexing = pb_name.split('_')
			filename, extension = ext.get_ext(indexing[-1])
			indexing = int(filename)
			indexing += 1
			indexing = padding_numbers.padder(indexing, pad)
			pb_name = 'pb_' + str(indexing) + '.' + extension
			sh_name = 'seq' + current_seq + '_' + 'shot' + current_shot + '.' + extension



	# select camera in the scene

	current_panel = mc.getPanel(wf=True)
	panel_types = mc.getPanel(typ='modelPanel')
	if current_panel not in panel_types:
		raise ValueError('Make a Right Click on the Viewport after you have the cam selected !')

	if 'shots' in charvalue:

		pb_cam = mc.ls('render__cam')
		current_cam = mc.lookThru(q=True)
		mc.lookThru(pb_cam)

	else:

		pb_cam = mc.ls(sl=True)
		if len(pb_cam) != 1:
			raise ValueError('Select one camera only !')

		current_shot = pb_cam[0].split('_')
		current_shot = current_shot[-1]
		child = mc.listRelatives(pb_cam[0], c=True)
		grand_child = mc.listRelatives(pb_cam[0] + '|' + child[0], c=True)
		last_child = mc.listRelatives(pb_cam[0] + '|' +  child[0] + '|' + grand_child[0], c=True)
		pb_cam = mc.ls(pb_cam[0] + '|' +  child[0] + '|' + grand_child[0] + '|' + last_child[0])

		print(pb_cam)


		test_cam_name = pb_cam[0].split('|')

		if test_cam_name[-1] != 'render__cam':
			raise NameError('The Camera selected is not a Render Cam !')

 		current_cam = mc.lookThru(q=True)
		mc.lookThru(pb_cam)

		if not path_versions:
			pb_name = 'pb__000.mov'

		indexing = pb_name.split('__')
		filename, extension = ext.get_ext(indexing[-1])
		indexing = int(filename)
		indexing += 1
		indexing = padding_numbers.padder(indexing, pad)
		pb_name = '__' + str(indexing) + '.' + extension	
		pb_name = 'seq' + current_seq + '_' + 'shot' + current_shot + pb_name
		sh_name = 'seq' + current_seq + '_' + 'shot' + current_shot + '.' + extension


	if master == True:

		go_on = mc.confirmDialog(title='MASTERSHOT', message = 'Are you sure you want to make a mastershot ?', button =['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No')
		if go_on == 'Yes':

			pb_name = sh_name
			pb_path = project_dir + '/preprod/animatic/shotlist/'
			hd = True
			overwrite = True
		else:
			raise NameError('Master Shot creation aborted !')

	# virer ornements camera

	if not 'shots' in charvalue:
		pb_cam = [pb_cam[0] + '|render__cam']
		print('NIQUEMOUK')
	mc.setAttr(pb_cam[0]+'Shape'+ '.displayGateMaskColor', 0,0,0)
	mc.setAttr(pb_cam[0]+'Shape'+ '.displayGateMaskOpacity', 1)
	cam_overscan = mc.getAttr(pb_cam[0]+'Shape'+ '.overscan')
	mc.setAttr(pb_cam[0]+'Shape'+ '.overscan', 1.0)

	# virer tout ce qui ne sert a rien...
	curves_visibility = mc.modelEditor(current_panel, q=True, nurbsCurves=True)
	cams_visibility = mc.modelEditor(current_panel, q=True, cameras=True)
	loc_visibility = mc.modelEditor(current_panel, q=True, locators=True)

	if curves_visibility == True:
		try:
			mc.modelEditor(current_panel, e=True, nurbsCurves=False)
		except:
			pass


	if cams_visibility == True:
		try:
			mc.modelEditor(current_panel, e=True, cameras=False)
		except:
			pass

	if loc_visibility == True:
		try:
			mc.modelEditor(current_panel, e=True, locators=False)
		except:
			pass


	current_sel = mc.ls(sl=True)
	mc.select(cl=True)
	# make playblast


	if hd == True:
		pb_wh = [1920,1080]
		qual = 100


	mc.playblast(f=pb_path + pb_name, fmt='qt', c='H.264', p=100, wh=pb_wh, orn=False, qlt=qual, fo=overwrite)
	mc.lookThru(current_cam)
	mc.setAttr(pb_cam[0]+'Shape'+ '.overscan', cam_overscan)


	if curves_visibility == True:
		try:
			mc.modelEditor(current_panel, e=True, nurbsCurves=True)
		except:
			pass
	if cams_visibility == True:
		try:
			mc.modelEditor(current_panel, e=True, cameras=True)
		except:
			pass

	if loc_visibility == True:
		try:
			mc.modelEditor(current_panel, e=True, locators=True)
		except:
			pass
	mc.select(current_sel)


def warpaint(paint=True):

	sel = mc.ls('gilles:body_texture','gilles:hands_texture','gilles:head_texture')

	if not sel:
		sel = mc.ls('body_texture','hands_texture','head_texture')
	for each in sel:
		name_tex = mc.getAttr(each + '.fileTextureName')
		mode_tex = mc.getAttr(each + '.colorSpace')

		if paint == True:
			name_tex = name_tex.split('__')
			name_text = (name_tex[0]).split('_')
			if name_text[-1] == 'paint':
				name_text = '_'.join(name_text)
			else:
				name_text = name_tex[0] + '_paint'
			name_tex = name_text + '__' + name_tex[-1]
		else:
			name_tex = name_tex.split('__')
			name_text = (name_tex[0]).split('_')
			if name_text[-1] == 'paint':
				name_text.pop(-1)
				name_text = '_'.join(name_text)
			name_tex = name_text + '__' + name_tex[-1]

		mc.setAttr(each + '.fileTextureName',name_tex, type='string')
		mc.setAttr(each + '.colorSpace',mode_tex, type='string')

def fix_cams(ratio='16/9'):

	ratio = ratio.split('/')
	
	if len(ratio) > 2:
		raise ValueError('Enter a valid ratio, like 4/3, 16/9...')

	w = float(ratio[0])
	h = float(ratio[-1])

	ratio = w/h
	import pymel.core as pmc
	cams = pmc.ls(cameras=True)
	for cam in cams:
		pmc.camera(cam, e=True, ar=ratio)

	return cams