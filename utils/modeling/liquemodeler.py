import os, sys
from PySide import QtGui, QtCore

from variables import *
class liqueModeler(QtGui.QWidget):
	def __init__(self):
		super(liqueModeler, self).__init__()
		self.setWindowTitle('LiqueModeler')
		self.resize(300,300)

		self.s_l_textbox = QtGui.QLineEdit(self)
		self.s_l_textbox.setEnabled(False)

		self.s_l_writebox = QtGui.QLineEdit(self)

		self.s_w_textbox = QtGui.QLineEdit(self)

		self.createButton = QtGui.QPushButton('PAPER THAT')

		hbox = QtGui.QHBoxLayout()

		hbox.addWidget(self.s_l_textbox)
		hbox.addWidget(self.s_l_writebox)
		self.setLayout(hbox)

		# main widget

		vbox = QtGui.QVBoxLayout()

		vbox.addWidget(hbox)
		vbox.addWidget(self.s_w_textbox)
		vbox.addWidget(self.createButton)

		self.setLayout(vbox)

app = QtGui.QApplication.instance()
if app is None:
	app = QtGui.QApplication(sys.argv)
lM = liqueModeler()
lM.show()
