import PySide.QtGui as QtGui
import PySide.QtCore as QtCore
import sys
import os
from variables import *

import pymel.core as pmc

class characterPicker(QtGui.QWidget):
	
	def __init__(self):
		QtGui.QWidget.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
		
		self.setWindowTitle('Character Picker')

		self.char_name = QtGui.QComboBox(self)

		self.bodyButton = QtGui.QPushButton("Body Controls")
		self.headButton = QtGui.QPushButton("Head Controls")

		self.allButton = QtGui.QPushButton("All Controls")

		hlayout = QtGui.QHBoxLayout()
		mainWidget = QtGui.QWidget()
		hlayout.addWidget(self.bodyButton)
		hlayout.addWidget(self.headButton)
		mainWidget.setLayout(hlayout)
		
		vlayout = QtGui.QVBoxLayout()
		vlayout.addWidget(self.char_name)
		vlayout.addWidget(mainWidget)
		vlayout.addWidget(self.allButton)

		mainLayout = QtGui.QVBoxLayout()
		mainLayout.addWidget(mainWidget)
		self.setLayout(vlayout)

		self.fillChars()


		self.bodyButton.clicked.connect(lambda: self.controlSelect(part='body', add=False))
		self.headButton.clicked.connect(lambda: self.controlSelect(part='head', add=False))
		self.allButton.clicked.connect(self.allControls)


	def fillChars(self):
		self.char_name.clear()
		dirs = os.listdir(project_dir + '/prod/assets/chars')
		for each in dirs:
			self.char_name.addItem(each)

	def controlSelect(self, part, add):

		undefined_ctrls = []
		controls = project_dir + '\\utils\\animation\\'

		if add == False:
			print('Not ADD mode')
		else:
			print('ADD mode activated')

		if part == 'body':
			controls += 'body_controls.txt'
		elif part == 'head':
			controls += 'face_controls.txt'

		controls_txt = open(controls, 'r')
		controls = controls_txt.read()
		controls_txt.close()
		controls = controls.split(';')
		char_namespace = str(self.char_name.currentText())

		if add==False:
			pmc.select(cl=True)
			
		for ctrl in controls:
			try:
				pmc.select(char_namespace + ':' + ctrl, add=True)
			except pmc.general.MayaNodeError:
				undefined_ctrls.append(ctrl)
				pass

		if undefined_ctrls:
			txt_print = ''
			for each in undefined_ctrls:
				txt_print += each + ', '
			txt_print = txt_print[:-2]
			print(char_namespace + ' has no controls named : ' + txt_print)
	def allControls(self):
		self.controlSelect(part='head', add=False)
		self.controlSelect(part='body', add=True)



def char_picker():
	
	try:
		if cP:
			cP.close()
			sys.exit(app.exec_())

	except:
		pass
	cP = characterPicker()
	cP.show()
	app = QtGui.QApplication.instance(cP)
	if app is None:
		app = QtGui.QApplication(sys.argv)

if __name__ == '__char_picker__':
	char_picker()