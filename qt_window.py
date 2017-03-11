import PySide.QtGui as QtGui
import PySide.QtCore as QtCore
import sys
class Window(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        
        self.btnBite = QtGui.QPushButton("bite")
        self.btnCouille = QtGui.QPushButton("couille")
        
        hlayout = QtGui.QHBoxLayout()
        hlayout.addWidget(QtGui.QPushButton("caca", self))
        hlayout.addWidget(QtGui.QPushButton("couille", self))
        
        self.connect(self.btnBite, QtCore.SIGNAL('clicked()'), self.print_name)
        
        mainWidget = QtGui.QWidget()
        mainWidget.setLayout(hlayout)
        
        vlayout = QtGui.QVBoxLayout()
        vlayout.addWidget(mainWidget)
        vlayout.addWidget(self.btnBite)
        vlayout.addWidget(QtGui.QPushButton("poil", self))

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(mainWidget)
        self.setLayout(vlayout)
        
    def print_name(self):
        print('caca de bite')



my_window = Window()
my_window.show()