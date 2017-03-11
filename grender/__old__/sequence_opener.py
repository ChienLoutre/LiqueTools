import os, sys
from guerilla import Document
from PySide import QtGui
from variables import *
class liqueOpener(QtGui.QWidget):
	def __init__(self):
		super(liqueOpener, self).__init__()
		self.setWindowTitle('LiqueOpener')

		QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
		self.resize(200,200)
		# scroll buttons

		self.asset_seq = QtGui.QPushButton('ASSET MODE')
		self.asset_seq.setCheckable(True)

		self.openButton = QtGui.QPushButton('Open !!!')

		self.folderButton = QtGui.QPushButton('Open Working Folder')


		# ...in a vertical layout
		vbox = QtGui.QVBoxLayout()

		contentWidget = QtGui.QWidget()


		vbox.addWidget(self.asset_seq)
		self.assetSeq(contentWidget, vbox)

		vbox.addWidget(self.openButton)
		vbox.addWidget(self.folderButton)
		# set our vertical layout
		self.setLayout(vbox)


		self.fillTypes()
		self.fillAssets()
		self.fillVersions()


		# connect signals
		self.asset_seq.toggled.connect(lambda: self.assetSeq(contentWidget, vbox))


		self.typeBox.currentIndexChanged.connect(self.fillAssets)
		self.assetBox.currentIndexChanged.connect(self.fillVersions)
		self.openButton.clicked.connect(self.openAsset)
		self.folderButton.clicked.connect(self.openFolder)

	def assetSeq(self, contentWidget, vbox):
		as_state = self.asset_seq.isChecked()

		v_content_box = QtGui.QVBoxLayout()

		if as_state == False:
			self.asset_seq.setText('ASSET MODE')
			self.typeBox = QtGui.QComboBox(self)
			self.assetBox = QtGui.QComboBox(self)
			self.versionBox = QtGui.QComboBox(self)
			v_content_box.addWidget(self.typeBox)
			v_content_box.addWidget(self.assetBox)
			v_content_box.addWidget(self.versionBox)

		else:
			self.asset_seq.setText("SEQUENCE")
			v_content_box.removeWidget(self.typeBox)
			v_content_box.removeWidget(self.assetBox)
			v_content_box.removeWidget(self.versionBox)
    		self.typeBox.setParent(None)
		contentWidget.setLayout(v_content_box)
		vbox.addWidget(contentWidget)
		self.setLayout(vbox)

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
		print(assetIndex)
		print(assetType)

	def openAsset(self):
		assetDir = project_dir + '/prod/assets'
		assetType = str(self.typeBox.currentText())
		assetName = str(self.assetBox.currentText())
		assetVersion= str(self.versionBox.currentText())
		asset_file = assetDir + '/' + assetType + '/' + assetName + '/lookdev/guerilla/' + assetVersion + '/lookdev.gproject'
		d = Document()
		print(asset_file)
		d.load(asset_file)

	def openFolder(self):
		import subprocess
		doc = Document()
		file_name = doc.getfilename()
		charvalue = str(file_name).split('/')
		charvalue.pop(-1)
		charvalue.pop(-1)
		charvalue.pop(-1)
		print(charvalue)
		file_name = '\\'.join(charvalue)
		print(file_name)
		subprocess.call('explorer ' + file_name, shell=True)

app = QtGui.QApplication.instance()
if app is None:
	app = QtGui.QApplication(sys.argv)
lO = liqueOpener()
lO.show()