# dans compo
# dossier => assets/*
# dossier seq/shots
# dossier compo_out

# rendre passes separees ou non ? plutot oui

# node read nuke qui comprenne que je suis dans tel sequence/shot, et va chercher le render out du master Rendu
from variables import *
import os

# make folders compo : assets, seq, shots
def update_folders():

	assets_dir = project_dir + '\\prod\\assets'
	assets_comp_dir = project_dir + '\\post\\compo\\assets'

	seq_dir = project_dir + '\\prod\\seq'
	seq_compo_dir = project_dir + '\\post\\compo\\seq'

	# get all assets
	asset_list = []
	assets = os.listdir(assets_dir)

	for folder in assets:
		try:
			os.mkdir(assets_comp_dir + '\\' + folder)
		except WindowsError:
			print('The folder ' + folder + ' already exists !')
		subassets = os.listdir(assets_dir + '\\' + folder)

		for each in subassets:
			try:
				os.mkdir(assets_comp_dir + '\\' + folder + '\\' + each)
			except WindowsError:
				print('The folder ' + folder + ' already exists !')
			try:
				os.mkdir(assets_comp_dir + '\\' + folder + '\\' + each + '\\' + 'compo_out')
			except WindowsError:
				print('The folder compo_out already exists !')		
			asset_list.append(each)


	seqs = os.listdir(seq_dir)

	for folder in seqs:
		print(folder)

		try:
			if folder == '__old__':
				pass
			else:
				os.mkdir(seq_compo_dir + '\\' + folder)

		except WindowsError:
			print('The folder ' + folder + ' already exists !')

		try:
			if folder == '__old__':
				pass
			else:
				os.mkdir(seq_compo_dir + '\\' + folder + '\\compo_out')
				
		except WindowsError:
			print('The folder ' + folder + ' already exists !')

		subshots = os.listdir(seq_dir + '\\' + folder + '\\' + 'shots')
		for shot in subshots:
			try:
				os.mkdir(seq_compo_dir + '\\' + folder + '\\' + shot)
				os.mkdir(seq_compo_dir + '\\' + folder + '\\' + shot + '\\compo_out')

			except WindowsError:
				print('The folder ' + shot + ' already exists !')		
			print(shot)


def load_read():

	import nuke
	from variables import *
	import os

	nuke_script_path = os.path.abspath(nuke.value("root.name"))

	if not project_name in nuke_script_path.split('\\'):
		raise ValueError('You are not working in the project !')


	vars = nuke_script_path.split('\\')
	vars.remove('compo')
	vars.remove('compo.nk')
	vars.append('master')
	render_dir = '/'.join(vars)
	print(render_dir)
	out_name = 'out_Layer_####.exr'

	render_out = render_dir + '/' + out_name

	read_node = nuke.nodes.Read(file=render_out)

	for channel in channels:
	    sh_node = nuke.nodes.Shuffle()
	    sh_node.connectInput(0, read_node)
	    sh_node.setName(channel)
	    sh_node.knob('postage_stamp').setValue(True)
	    sh_node.knob('in').setValue(channel)
