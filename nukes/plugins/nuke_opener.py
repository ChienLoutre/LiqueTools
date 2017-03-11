import os, sys
import nuke
from PySide import QtGui, QtCore

from variables import *
class assetOpener(QtGui.QWidget):
	def __init__(self):
		super(assetOpener, self).__init__()
		self.setWindowTitle('LiqueNuke Opener')
		QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
		self.resize(250,200)

		# scroll buttons

		self.assSeq = QtGui.QComboBox(self)
		self.typeBox = QtGui.QComboBox(self)
		self.assetBox = QtGui.QComboBox(self)
		self.versionBox = QtGui.QComboBox(self)

		self.openButton = QtGui.QPushButton('Open Nuke Script !')

		# ...in a vertical layout
		vbox = QtGui.QVBoxLayout()
		vbox.addWidget(self.assSeq)
		vbox.addWidget(self.typeBox)
		vbox.addWidget(self.assetBox)
		vbox.addWidget(self.versionBox)
		vbox.addWidget(self.openButton)
		# set our vertical layout
		self.setLayout(vbox)

		self.fillAssSeq()
		self.fillTypes()
		self.fillAssets()
		self.fillVersions()

		# connect signals
		self.assSeq.currentIndexChanged.connect(self.fillTypes)
		self.typeBox.currentIndexChanged.connect(self.fillAssets)
		self.assetBox.currentIndexChanged.connect(self.fillVersions)
		self.openButton.clicked.connect(self.openAsset)

	def fillAssSeq(self):
		self.assSeq.clear()
		dirs = ['assets', 'seq']
		for each in dirs:
			self.assSeq.addItem(each)

	def fillTypes(self):
		self.typeBox.clear()
		assSeq = self.assSeq.currentText()
		dirs = os.listdir(project_dir + '/post/compo/'+ assSeq)
		if 'compo_out' in dirs:
			dirs.remove('compo_out')
		for each in dirs:
			self.typeBox.addItem(each)

	def fillAssets(self):
		self.assetBox.clear()
		assSeq = self.assSeq.currentText()
		assetDir = project_dir + '/post/compo/' + assSeq
		assetType = self.typeBox.currentText()
		dirs = os.listdir(assetDir + '/' + assetType)
		if 'compo_out' in dirs:
			dirs.remove('compo_out')
		for each in dirs:
			self.assetBox.addItem(each)

	def fillVersions(self):
		self.versionBox.clear()
		assSeq = self.assSeq.currentText()
		assetDir = project_dir + '/post/compo/' + assSeq
		assetType = self.typeBox.currentText()
		assetName = self.assetBox.currentText()
		dirs = os.listdir(assetDir + '/' + assetType + '/' + assetName)
		if 'compo_out' in dirs:
			dirs.remove('compo_out')

		if not dirs == []:

				for each in dirs:
					self.versionBox.addItem(each)

	def printVer(self):
		assetIndex = self.versionBox.currentIndex()
		assetType = self.versionBox.currentText()


	def openAsset(self):
		assSeq = self.assSeq.currentText()
		assetDir = project_dir + '/post/compo/' + assSeq
		assetType = str(self.typeBox.currentText())
		assetName = str(self.assetBox.currentText())
		assetVersion= str(self.versionBox.currentText())
		if not assetVersion:
			asset_file = assetDir + '/' + assetType + '/' + assetName
		else:
			asset_file = assetDir + '/' + assetType + '/' + assetName + '/' + assetVersion
		print(asset_file)
		nuke.scriptOpen(asset_file)


def main():
	
	aO = assetOpener()
	aO.show()
	app = QtGui.QApplication.instance(aO)
	if app is None:
		app = QtGui.QApplication(sys.argv)
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()