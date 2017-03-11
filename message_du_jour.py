from variables import *
import ctypes  # An included library with Python install.
import os

def le_message_du_jour(pc_name=pc_name):


	msg = 'Quell belle journee !'
	title = 'Bonjour a toi !'

	if pc_name == 'M5PC03':


	elif pc_name == 'M5PC04':


	elif pc_name == 'M5PC05':


	elif pc_name == 'M5PC06':


	elif pc_name == 'M5PC07':


	elif pc_name == 'M5PC08':


	ctypes.windll.user32.MessageBoxA(0, msg, title, 0)