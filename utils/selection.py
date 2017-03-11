# Selection functions

import maya.cmds as mc
import os


def by_name(sel = ''):

	sel = mc.select(sel)
	print('selection.by_name => ' + str(sel))
	sel = mc.ls(sl=True)
	return sel

def simple_txt_ui(def_window='select_by_name', def_title = 'Select By Name', txtfield = 'sel_by_name', ok_button= 'Select Objects', function_launch = by_name):

	w = 300

	# check to see if the window exists
	if mc.window(def_window + '__ui', exists = True):
		mc.deleteUI(def_window + '__ui')

	# create the window

	window = mc.window(def_window + '__ui', title = def_title, w = w, h=80,mnb = False, mxb = False, sizeable = False, rtf=True)

	# create a main layout

	mainLayout = mc.columnLayout(w = w, h=50)

	mc.text(l = def_title, align='center', w=w)

	sl_field = mc.textField(txtfield, tx = '', w=w, ec=button_proceed, aie=True)

	mc.button(l=ok_button, w=w, c=lambda *args: button_proceed(txtfield, function_launch))

	mc.showWindow(window)

def button_proceed(txtfield, function_launch):
	sel = mc.textField(txtfield, q=True, tx=True)
	function_launch(sel)


def blendshape_ui():

	w = 300

	# check to see if the window exists
	if mc.window('blensdshape' + '__ui', exists = True):
		mc.deleteUI('blendshape' + '__ui')

	# create the window

	window = mc.window('blendshape' + '__ui', title = 'Set Blendshape Name', w = w, h=80,mnb = False, mxb = False, sizeable = False, rtf=True)

	# create a main layout

	mainLayout = mc.columnLayout(w = w, h=50)

	mc.text(l = 'Set Blendshape Name', align='center', w=w)

	sl_field = mc.textField('txt_field', tx = '', w=w, ec=button_proceed, aie=True)

	mc.button(l=ok_button, w=w, c=lambda *args: button_proceed('txt_field', create_blendshape))

	mc.showWindow(window)
