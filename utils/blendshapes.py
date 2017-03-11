import maya.cmds as mc
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore
import sys

import shapes as shp
reload(shp)

class Window(QtGui.QWidget):
	def __init__(self):
		QtGui.QWidget.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)

		self.window().setWindowTitle("BlendShape Extract")

		self.btn_update = QtGui.QPushButton("Update Selected")
		self.line_obj_name = QtGui.QLabel(str('NO OBJECT SELECTED'))
		self.line_shape_name = QtGui.QLineEdit(str())
		self.btn_create = QtGui.QPushButton("Create BlendShape")
		
		self.connect(self.btn_update, QtCore.SIGNAL('clicked()'), self.update_selected)
		self.connect(self.btn_create, QtCore.SIGNAL('clicked()'), self.create_blendshape)
		
		hlayout = QtGui.QHBoxLayout()
		hlayout.addWidget(self.btn_update)
		hlayout.addWidget(self.line_obj_name)
		
		mainWidget = QtGui.QWidget()
		mainWidget.setLayout(hlayout)
		
		vlayout = QtGui.QVBoxLayout()
		vlayout.addWidget(mainWidget)
		vlayout.addWidget(self.line_shape_name)
		vlayout.addWidget(self.btn_create)

		mainLayout = QtGui.QVBoxLayout()
		mainLayout.addWidget(mainWidget)
		self.setLayout(vlayout)
		
	def update_selected(self):
		self.line_obj_name.setText(get_selected())
		
	def create_blendshape(self):
		base_mesh = self.line_obj_name.text()
		blendshape_name = self.line_shape_name.text()
		shp.create_blendshape(base_mesh,blendshape_name)


#my_window = Window()
#my_window.show()

def get_selected():
	return mc.ls(selection=True)[-1]

def create_blendshape(base_mesh,blendshape_name):

	blendshape_name = blendshape_name + '__shp'

	mc.duplicate(base_mesh, n=blendshape_name)

	try:
		mc.parent(blendshape_name, 'blendshapes')
		mc.warning('blendshape "' + blendshape_name + '" successfully created !')
	except:
		mc.warning('no blendshape grp in the scene')

	return blendshape_name

def mirror_blendshape(sel=None, axis=[-1,1,1]):
	'''
	1. select the basemesh (the one with a symmetry)
	2. select also the blendshape you want to mirror
	
	if you want to change the mirror axis, write the expression as:
	mirror_blendshape(axis=[1,-1,1]) 
	First one is X, then Y and Z.
	'''


	returnList = []
	if not sel:
		# Get Current selection
		sel = mc.ls( sl = True )
	elif not isinstance(sel,list):
		sel = [sel]

	if not len(sel) == 2:
		sys.exit('select a mesh and a target for the new mesh')

	basemesh = sel[0]
	blendshp = sel[1]

	name_mirror = ''

	naming = blendshp.split('_')
	if naming[0] == 'l':
		naming[0] = 'r'
		name_mirror = '_'.join(naming)
	elif naming[0] == 'r':
		naming[0] = 'l'
		name_mirror = '_'.join(naming)
	else:
		name_mirror = 'mirrored_' + str(blendshp)

	temp_mesh = mc.duplicate(basemesh, n='__temp__mesh__')
	temp_shape = mc.duplicate(basemesh, n='temp__blendshape')
	# create blendshape on duplicated mesh

	bs_node = mc.blendShape(blendshp, temp_mesh, n='temp__BS')

	mc.xform(temp_mesh, s=axis)

	mc.select(temp_shape, temp_mesh)
	wrap_sel = mc.ls(sl=True)

	mc.CreateWrap(wrap_sel)

	mc.setAttr('temp__BS' + '.' + blendshp, 1)

	mc.duplicate(temp_shape, n=name_mirror)

	mc.delete(temp_mesh)
	mc.delete(temp_shape)
