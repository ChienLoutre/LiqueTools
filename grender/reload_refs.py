import guerilla
from variables import *
import os
doc = guerilla.Document()

def getMissingRefs():

	assets_dir = project_dir + '/prod/assets'
	asset_look = '/lookdev/guerilla/master'

	asset_list = ['chars','props','sets']
	asset=None
	print('---------------------')
	print('---------------------')
	print('  Getting Lost Refs  ')
	print('---------------------')
	print('---------------------')

	# get all the references in the document

	print('acquiring references in the scene...')

	refs = doc.getreferences()
	refs_name = []

	with guerilla.Modifier() as mod:
		for each in asset_list:

			mod.select([each], mode='replace')
			asset = doc.selection()[0]
			for child in asset.children():
				hasref = False
				name = child.getname()

				try:
					name = name.split(':')
					name = name[-1]
				except ValueError:
					pass
				for ref in refs:
					ref_name = ref.getname()
					ref_name = ref_name.split('__')
					ref_name = ref_name[0]

					if ref_name == name:
						hasref = True
				if hasref == True:
					print('The master for ' + name + ' is already referenced in this scene')
				else:
					print(name + ' has no referenced master')
					asset_path = assets_dir + '/' + each + '/' + name + asset_look
					if os.path.exists(assets_dir + '/' + each + '/' + name + asset_look) == True:
						a = dict({'prefixnodes':False,'containschildren':False})
						refNode, topNodes = mod.createref(name + '__ref', asset_path + '/lookdev.gproject', parent=None, options=a)
						print('----------------------------------------------------------')
						print('IMPORTED RENDERGRAPH FROM ASSET ' + name + ' SUCCESSFULLY !')
						print('----------------------------------------------------------')

					else:
						print('This directory does not exist')
	print('---------------------')
	print('---------------------')
	print('Referencer job done !')
	print('---------------------')
	print('---------------------')
