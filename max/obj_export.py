import MaxPlus as mc
import time
import os
import sys
from variables import *
import padding_numbers
import max.save as save
import utils.get_extension as ext
import pymxs
reload(ext)

def export():

	mx = pymxs.runtime
	fm = mc.FileManager

	asset_name = fm.GetFileNameAndPath()
	charvalue = asset_name.split('\\')
	asset_name, extension = ext.get_ext(charvalue[-1])

	print(asset_name)
	print(charvalue)
	print(charvalue[-4])

	if not project_name in charvalue:

		sys.exit('You are not working in the Project !!')



	go_on = mx.queryBox("You are about to export the asset " + charvalue[-4] + " to Maya. Continue ?", title='Exporting to Maya : ' + charvalue[-4] )

	if go_on == False:
		
		sys.exit('Export of the asset : ' + charvalue[-4] + ' aborted.')

	current_asset = save.folder_only()
	print(current_asset)

	temp_dir = project_dir + '\\utils\\export\\' + asset_name
	print(temp_dir)
	with open(temp_dir  + '.txt', "w") as f:
		f.write(current_asset + '\\')
		f.close()

	temp_dir = temp_dir + '.obj'



	exp_maxscript = 'exportFile ("' + temp_dir + '")using:theClasses[13]'
	print(exp_maxscript)
	mc.Core.EvalMAXScript("theClasses = exporterPlugin.classes")
	mc.Core.EvalMAXScript(exp_maxscript)

	print('export still in progress...')

	run_maya = "Y:\\Liquefacteur\\utils\\scripts\\max\\maya_export.bat"
	max_maya = 'ShellLaunch "' + run_maya + '" ""'
	print(max_maya)
	mc.Core.EvalMAXScript(max_maya)
