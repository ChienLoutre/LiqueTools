import PySide.QtGui as QtGui

class Window(QtGui.Widget):
	def __init__(self):
		QtGui.Widget.__init__(self)


my_window = Window()
my_window.show()