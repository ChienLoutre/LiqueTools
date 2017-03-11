import sys
import nuke
import nukes.plugins.nuke_opener

def lique_menu():

	menubar = nuke.menu('Nuke')
	toolbar = nuke.toolbar('Nodes')

	print("Loading Liquefacteur's Awesome Toolbar...")
	m = toolbar.addMenu('LiqueNuke', icon='Y:/Liquefacteur/utils/icons/liquenuke.png')
	m.addCommand("Asset Opener", lambda:nukes.plugins.nuke_opener.main())