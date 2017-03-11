import os, sys
from guerilla import Document
from PySide import QtGui
from variables import *
class assetOpener(QtGui.QWidget):
	def __init__(self):
		super(assetOpener, self).__init__()
		self.setWindowTitle('Asset Opener')

		QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
		self.resize(200,200)
		# scroll buttons

		self.typeBox = QtGui.QComboBox(self)
		self.assetBox = QtGui.QComboBox(self)
		self.versionBox = QtGui.QComboBox(self)

		self.openButton = QtGui.QPushButton('Open Asset')

		self.folderButton = QtGui.QPushButton('Open Asset Folder')


		# ...in a vertical layout
		vbox = QtGui.QVBoxLayout()

		vbox.addWidget(self.typeBox)
		vbox.addWidget(self.assetBox)
		vbox.addWidget(self.versionBox)

		vbox.addWidget(self.openButton)
		vbox.addWidget(self.folderButton)
		# set our vertical layout
		self.setLayout(vbox)



		self.fillTypes()
		self.fillAssets()
		self.fillVersions()

		# connect signals
		self.typeBox.currentIndexChanged.connect(self.fillAssets)
		self.assetBox.currentIndexChanged.connect(self.fillVersions)
		self.openButton.clicked.connect(self.openAsset)
		self.folderButton.clicked.connect(self.openFolder)


	def fillTypes(self):
		self.typeBox.clear()
		dirs = os.listdir(project_dir + '/prod/assets')
		for each in dirs:
			self.typeBox.addItem(each)

	def fillAssets(self):
		self.assetBox.clear()
		assetDir = project_dir + '/prod/assets'
		assetType = self.typeBox.currentText()
		dirs = os.listdir(assetDir + '/' + assetType)
		for each in dirs:
			self.assetBox.addItem(each)

	def fillVersions(self):
		self.versionBox.clear()
		assetDir = project_dir + '/prod/assets'
		assetType = self.typeBox.currentText()
		assetName = self.assetBox.currentText()
		dirs = os.listdir(assetDir + '/' + assetType + '/' + assetName + '/lookdev/guerilla')

		if not dirs == []:

				for each in dirs:
					self.versionBox.addItem(each)

	def printVer(self):
		assetIndex = self.versionBox.currentIndex()
		assetType = self.versionBox.currentText()

	def openAsset(self):
		assetDir = project_dir + '/prod/assets'
		assetType = str(self.typeBox.currentText())
		assetName = str(self.assetBox.currentText())
		assetVersion= str(self.versionBox.currentText())
		asset_file = assetDir + '/' + assetType + '/' + assetName + '/lookdev/guerilla/' + assetVersion + '/lookdev.gproject'
		d = Document()
		d.load(asset_file)

	def openFolder(self):
		import subprocess
		doc = Document()
		file_name = doc.getfilename()
		charvalue = str(file_name).split('/')
		charvalue.pop(-1)
		charvalue.pop(-1)
		charvalue.pop(-1)
		file_name = '\\'.join(charvalue)
		subprocess.call('explorer ' + file_name, shell=True)

app = QtGui.QApplication.instance()
if app is None:
	app = QtGui.QApplication(sys.argv)
aO = assetOpener()
aO.show()