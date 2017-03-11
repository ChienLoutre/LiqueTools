import os, sys
from guerilla import Document
from PySide import QtGui
import guerilla
from variables import *
class liqueRender(QtGui.QWidget):
	def __init__(self):
		super(liqueRender, self).__init__()
		self.setWindowTitle('Liquerender')

		# color palettes

		pal = QtGui.QPalette()
		pal.setColor(pal.ColorRole.Background, QtGui.QColor(255,55,120,255))

		self.setAutoFillBackground(True)
		self.setPalette(pal)
		QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))

		# scroll buttons

		self.r_quality = QtGui.QComboBox(self)
		self.f_format = QtGui.QComboBox(self)

		# frames a rendre


		self.r_frames_txt = QtGui.QLabel("Les frames a rendre", self)
		self.r_frames_txt.setFixedHeight(10)

		self.r_frames_2txt = QtGui.QLabel("12:30 <= Rend les frames de 12 a 30", self)
		self.r_frames_2txt.setFixedHeight(10)
		self.r_frames_3txt = QtGui.QLabel("12:15-20:30 <= Rend de 12 a 15 et de 20 a 30", self)
		self.r_frames_3txt.setFixedHeight(10)


		self.r_frames = QtGui.QTextEdit(self)
		self.r_frames.setFixedHeight(30)

		self.batchButton = QtGui.QPushButton("I'm Batchman")
		self.batchButton.setCheckable(True)

		self.farmButton = QtGui.QPushButton('Je vais a la Ferme')
		self.farmButton.setCheckable(True)
		
		self.launchButton = QtGui.QPushButton('LANCE LE RENDU !!!')

		pal.setColor(pal.ColorRole.Button, QtGui.QColor(50,50,50,255))
		pal.setColor(pal.ColorRole.ButtonText, QtGui.QColor(255,255,255,255))

		self.launchButton.setPalette(pal)
		# ...in a vertical layout

		buttonWidget = QtGui.QWidget()

		vbox = QtGui.QVBoxLayout()
		hbox = QtGui.QHBoxLayout()


		hbox.addWidget(self.batchButton)
		hbox.addWidget(self.launchButton)
		buttonWidget.setLayout(hbox)

		vbox.addWidget(self.r_frames_txt)
		vbox.addWidget(self.r_frames_2txt)
		vbox.addWidget(self.r_frames_3txt)

		vbox.addWidget(self.r_frames)
		vbox.addWidget(self.r_quality)
		vbox.addWidget(self.f_format)

		vbox.addWidget(buttonWidget)

		# set our vertical layout
		self.setLayout(vbox)

		self.fillQuality()
		self.fillFormat()
		# connect signals
		self.batchButton.toggled.connect(self.renderMode)
		self.launchButton.clicked.connect(self.launchRender)

	def renderMode(self):
		fb_state = self.batchButton.isChecked()
		if fb_state == True:
			self.batchButton.setText('Je vais a la Ferme')
		else:
			self.batchButton.setText("I'm Batchman")


	def printOk(self):
		print('meuh')

	def fillQuality(self):
		for each in quality:
			self.r_quality.addItem(each)
	
	def fillFormat(self):
		for each in file_format:
			self.f_format.addItem(each)

	def launchRender(self):
		import grender.render as render
		reload(render)

		render_frames = str(self.r_frames.toPlainText())
		if render_frames == '':
			render_frames == None
		render_quality= str(self.r_quality.currentText())
		render_format= str(self.f_format.currentText())
		farm_render= self.batchButton.isChecked()
		if farm_render == True:
			render_mode = 'farm'
		else:
			render_mode = 'batch'
		print(render_frames)
		render.launch(mode=render_mode, file_ext=render_format, qual=render_quality, frames=render_frames, local=False)


app = QtGui.QApplication.instance()
if app is None:
	app = QtGui.QApplication(sys.argv)
lr = liqueRender()
lr.show()