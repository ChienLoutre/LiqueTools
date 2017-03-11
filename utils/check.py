import maya.cmds as mc
import pymel.core as pmc
import sys



def mod(ch_file):

	mc.file(ch_file, open=True)

	sel = mc.select(ado=True)
	sel = mc.ls(sl=True)

	if len(sel) != 2:
		
		sys.exit('You do not have 2 objects in the scene.')

	if sel[0] != 'mod':
		
		sys.exit('group "mod" doesnt exist')

	if sel[1] != 'GuerillaNode':
		
		sys.exit('group "GuerillaNode" doesnt exist')

	for each in sel:
		
		pos = mc.xform(sel[0], q=True, t=True, a=True)
		rot = mc.xform(sel[0], q=True, ro=True, a=True)
		sc = mc.xform(sel[0], q=True, s=True, ws=True)
		
		if pos != [0.0,0.0,0.0]:
			
			sys.exit('group ' + each + ' isnt at ZERO in Position')

		elif rot != [0.0,0.0,0.0]:
			
			sys.exit('group ' + each + ' isnt at ZERO in Rotation')
			
		elif sc != [1.0,1.0,1.0]:
			
			sys.exit('group ' + each + ' isnt at ONE in Scale')
			
	print('Tout semble en ordre dans les deux dossiers')

	children = mc.listRelatives(sel[0], c=True)

	for each in children:

		pos = mc.xform(each, q=True, t=True, a=True)
		rot = mc.xform(each, q=True, ro=True, a=True)
		sc = mc.xform(each, q=True, s=True, ws=True)
		
		if sc != [1.0,1.0,1.0]:
			
			sys.exit(each + ' has some weird SCALE info. Please check')
			
			
	print('Tout semble en ordre dans les fichiers du dossier Mod')

	go_on = mc.confirmDialog(title='History', message = 'Do you want to delete all the History for the scene ?', button =['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No')

	if go_on == 'No':

		print('History will be conserved')

	else:

		for each in children:

			mc.delete(each, ch=True)
			
		print('History successfully deleted !')

def ngons(tris = False):

	typegon = 'ngons'

	if tris == True:

		tris = 1
		typegon = 'triangles'
	
	else:

		tris = 3

	sel = mc.select(ado=True)
	sel = mc.ls(sl=True)

	full_sel = []
	for each in sel:

		mc.listRelatives(each, c=True)
		

	mc.selectMode(component=True)

	#Change to Face Component Mode

	mc.selectType(smp=False, sme=True, smf=False,smu=False, pv=False, pe=False, pf=True, puv=False)

	#Select Object/s and Run Script to highlight Triangles

	mc.polySelectConstraint(mode=3, type=0x0008, size=tris)
	mc.polySelectConstraint(disable=False)

	ngons = mc.polyEvaluate(faceComponent=True)


	mc.polySelectConstraint(disable=True)

	mc.select(cl=True)
	mc.selectMode(object=True)
	mc.select(cl=True)

	if ngons == 0:

		print('No '+ str.capitalize(typegon) +' found !')

	print('There are ' + str(ngons) + ' ' + str.capitalize(typegon) + ' found on this asset.')

	return ngons

def ngons_on_selected(tris = False):


	typegon = 'ngons'

	if tris == True:

		tris = 1
		typegon = 'triangles'
	
	else:

		tris = 3

	sel = mc.ls(sl=True)

	if not sel:

		sys.exit('Nothing selected !')


	mc.selectMode(component=True)

	#Change to Face Component Mode

	mc.selectType(smp=False, sme=True, smf=False,smu=False, pv=False, pe=False, pf=True, puv=False)

	#Select Object/s and Run Script to highlight Triangles

	mc.polySelectConstraint(mode=3, type=0x0008, size=tris)
	mc.polySelectConstraint(disable=False)

	ngons = mc.polyEvaluate(faceComponent=True)


	mc.polySelectConstraint(disable=True)


	if ngons == 0:

		print('No '+ str.capitalize(typegon) +' found !')

	print('There are ' + str(ngons) + ' ' + str.capitalize(typegon) + ' found on this piece of asset.')
	
	if ngons == 1:

		typegon = typegon[:-1]
		
	mc.warning(str(ngons) + ' ' + str(typegon) + ' found.')

	return ngons


def history():

	sel = mc.ls(sl=True)

	if not sel:

		sys.exit('Nothing selected !')

	count = 0
	for each in sel:

		ch_history = mc.listHistory(each)
		ch_history.pop(0)
		if not ch_history:
			mc.warning('no construction history on ' + each + '. Perfect.')
			print('no construction history on ' + each + '. Perfect.')

		else:
			count += 1
			print(each + ' history : ' + str(ch_history))

	if count != 0:

		mc.warning(str(count) + 'have a construction history. Check that please.')

	else:

		mc.warning('No construction history on selected objects !')


def transforms(sel, check_children=False):

	pos = ''
	rot = ''
	sc = ''
	for each in sel:
		
		pos = mc.xform(sel[0], q=True, t=True, a=True)
		rot = mc.xform(sel[0], q=True, ro=True, a=True)
		sc = mc.xform(sel[0], q=True, s=True, ws=True)
		if pos != [0.0,0.0,0.0]:
			pos = False

		elif rot != [0.0,0.0,0.0]:
			rot = False

		elif sc != [1.0,1.0,1.0]:
			sc = False

	if pos == False:
		sys.exit('Main group isnt at 0 in position')
	elif rot == False:
		sys.exit('Main group isnt at 0 in rotation')
	elif sc == False:
		sys.exit('Main group has scaling info')


	if check_children == True:

		children = mc.listRelatives(sel[0], c=True)
		for each in children:

			pos = mc.xform(each, q=True, t=True, a=True)
			rot = mc.xform(each, q=True, ro=True, a=True)
			sc = mc.xform(each, q=True, s=True, ws=True)
			
			if sc != [1.0,1.0,1.0]:
				
				sys.exit(each + ' has some weird SCALE info. Please check')

	transforms = True

	return transforms

