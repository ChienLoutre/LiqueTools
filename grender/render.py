from variables import *
from guerilla import Document, pynode, Modifier
import guerilla
import utils.get_extension as ext
import padding_numbers
import os
import sys
import datetime
import grender.scene_init

li = grender.scene_init.liquerillaInit()
doc = Document()

# --------------------------------------------
#
#	RENDER WITH GUERILLA
# 
# 
# - empecher de faire des trucs si on nest pas dans le projet
# - log (lance de quelle version, quelle heure, ect...)
#
#  Parametres pour rendu
# 
#  ecrire <liquefacteur_> + <HD_/LD_/TEST_> + <nom_du_rendu>
#
# LD = frames illimitees mais timeout 10min / priority 50 max.
# HD = frames illimitees et temps illimite / priority 49 max.
# TEST = 3 frames mais temps illimite / priority 75 max.
# 
# 
# --------------------------------------------

def set_local_path():
	'''
	Search and replace the render path by a local one in the pipeline.

	'''
	print("nothing")

def get_version():
	'''
	get the version of the current document you are working on.
	'''
	version = doc.getfilename()
	version = version.split('/')
	version = version[-2]

	print('WORKING ON ==> '+ version + ' <==')
	return version

def get_paths():
	'''
	Only use this function to get the path in <%project_dir%/post/assets>

	'''
	file_name = doc.getfilename()
	charvalue = str(file_name).split('/')
	print(charvalue)

	if charvalue[4] == 'assets':

		asset_name = charvalue[-5]
		asset_type = charvalue[-6]

		# Build a folder in post for the asset

		render_folder = project_dir + '/post/assets/' + asset_type + '/'
		render_path = render_folder + asset_name
		render_path_local = render_path + '/local'

		# Build a folder in utils for the job

		job_path = project_dir + '/utils/guerilla/jobs/' + asset_name

	else:

		seq_name = charvalue[5]

		# Build a folder in post for the sequence

		render_folder = project_dir + '/post/seq/' + seq_name
		render_path = render_folder
		render_path_local = render_path + '/local'

		# Build a folder in utils for the job

		job_path = project_dir + '/utils/guerilla/jobs/' + seq_name

	return render_path, render_path_local, job_path


def build_path(file_ext='png'):

	# Get file name / path and job path

	render_path, render_path_local, job_path = get_paths()

	try:
		os.mkdir(render_path)
		os.mkdir(render_path_local)
		os.mkdir(job_path)
	except:
		print('the folder already exists')

	# create name for the turntable

	out_image_vars = 'out' + '_$04f.$x'
	out_image_name = render_path_local + '/' + out_image_vars

	print(out_image_name)

	rPass = None
	rPass = li.get_Rpass()

	with Modifier() as mod:
		
		rPass.FileName.set(out_image_name)
		rPass.DisplayDriver.set(file_ext)

def asset(mode='farm', file_ext='png', qual=1, local=False):

	'''

	'''
	# Get file name / path and job path
	render_path, render_local_path, job_path = get_paths()

	#passer  en mode hyperespace

	rPass = None
	rPass = li.get_Rpass()
	prefs = pynode('Preferences')
	
	# Versionning

	versions = os.listdir(render_path)

	if 'local' in versions:
		versions.remove('local')

	if not versions:
		os.mkdir(render_path + '/V000')

	else:
		filevalue = versions[-1]
		indexing = filevalue.split('V')
		indexing = int(indexing[-1])
		indexing += 1
		indexing = padding_numbers.padder(indexing, pad)
		filevalue = 'V' + str(indexing)
		os.mkdir(render_path + '/' + filevalue)

	last_version = os.listdir(render_path)
	last_version = last_version[-1]

	render_path = render_path + '/' + last_version
	out_image_vars = 'out' + '_.$04f.$x'
	out_image_name = render_path + '/' + out_image_vars

	with Modifier() as mod:
		rPass.FileName.set(out_image_name)


	quality_settings = var_render + quality[qual]
	with Modifier() as mod:
		prefs.RenderfarmSequence.set(quality_settings)
		rPass.FileName.set(out_image_name)
		rPass.DisplayDriver.set(file_ext)


	# Job Path => temporary ?

	job_path = render_path + '/' + 'jobs'
	os.mkdir(job_path)

	opts = dict({'JobsDirectory':job_path})

	# Render the images
	print('render place : ' + out_image_name)
	print('render jobs : ' + job_path)

	guerilla.render(mode,opts)

	# revenir en mode local

	out_image_name = render_local_path + '/' + out_image_vars
	print('new render place : ' + out_image_name)
	with Modifier() as mod:
		rPass.FileName.set(out_image_name)

def seq(mode='farm', file_ext='exr', qual=-1):

	# Get file name / path and job path

	render_path, job_path = get_paths()

	# Versionning
	versions = os.listdir(render_path)

	if not versions:

		os.mkdir(render_path + '/V000')

	else:

		filevalue = versions[-1]

		indexing = filevalue.split('V')
		indexing = int(indexing[-1])
		indexing += 1
		indexing = padding_numbers.padder(indexing, pad)
		filevalue = 'V' + str(indexing)

		os.mkdir(render_path + '/' + filevalue)

	last_version = os.listdir(render_path)
	last_version = last_version[-1]
	render_path = render_path + '/' + last_version

	out_image_vars = 'out' + '$n_.$04f.$x'
	out_image_name = render_path + '/' + out_image_vars

	quality_settings = var_render + quality[qual]

	rPass = None
	rPass = li.get_Rpass()
	prefs = pynode('Preferences')

	with Modifier() as mod:

		prefs.RenderfarmSequence.set(quality_settings)
		rPass.FileName.set(out_image_name)
		rPass.DisplayDriver.set(file_ext)

	# Render the images

	opts = dict({'JobsDirectory':job_path})
	guerilla.render(mode,opts)

def iterator(mult = 1):

	begin_frame = doc.FirstFrame.get()
	end_frame = doc.LastFrame.get()


	lister = []

	if mult != 1:

		for i in range(begin_frame,end_frame,mult):
			lister.append(str(i))


		lister = ','.join(lister)
	else:

		lister = [str(begin_frame),str(end_frame)]
		lister = '-'.join(lister)

	return lister

def format_time():
	nowtime = datetime.datetime.now()
	nowtime = str(nowtime).split('.')
	nowtime = nowtime[0]
	nowtime = nowtime.split(' ')
	day = nowtime[0]
	hour = nowtime[-1]
	day = day.split('-')
	day = '_'.join(day)
	hour = hour.split(':')
	seconds = hour[-1]
	hour.pop(-1)
	hour = 'h'.join(hour)
	hour = hour + '_' + seconds
	
	return day, hour

def launch(mode='farm', file_ext='png', qual='LD_', local=False, frames=None, multi=1):

	'''

	'''
	# Get file name / path and job path
	render_path, render_local_path, job_path = get_paths()

	#passer  en mode hyperespace

	rPass = None
	rPass = li.get_Rpass()
	prefs = pynode('Preferences')
	
	# Versionning
	day, hour = format_time()

	folder = day + '_' + hour + '.' + mode.lower()
	render_path = render_path + '/' + folder
	
	try:
		os.mkdir(render_path)
	except:
		raise Exception('ARRETE TOI')

	out_image_vars = 'out' + '_$n_$04f.$x'
	out_image_name = render_path + '/' + out_image_vars
	out_pass_name = '$o'
	with Modifier() as mod:
		rPass.FileName.set(out_image_name)


	quality_settings = var_render + qual
	with Modifier() as mod:
		prefs.RenderfarmSequence.set(quality_settings)
		rPass.FileName.set(out_image_name)
		rPass.FileLayerName.set(out_pass_name)

		rPass.DisplayDriver.set(file_ext)


	# Job Path => temporary ?

	job_path = render_path + '/' + 'jobs'
	os.mkdir(job_path)

	if frames:
		opts = dict({'JobsDirectory':job_path, 'RibsDirectory':job_path, 'Frames':frames, 'DistributedCount':multi})
	else:
		opts = dict({'JobsDirectory':job_path, 'RibsDirectory':job_path, 'DistributedCount':multi})

	# Render the images

	guerilla.render(mode,opts)

	# revenir en mode local

	out_image_name = render_local_path + '/' + out_image_vars

	with Modifier() as mod:
		rPass.FileName.set(out_image_name)


def exrId(path, filename):
	'''
	Transforms the Id pass into an exrid pass.
	This function also creates a folder
	Returns the final path for the exrId.
	Syntax :
		exrId(path=<render_path>, filename=<name_of_your_render_file>)

	example :
		new_path = exrId(path='D:\\Renders',filename='$o_ID.$f.x$')
		print(new_path)

	This prints ===> 'D:/Renders/exrid/$o_ID.$f.x$'
	'''

	rLayer =  pynode('RenderPass|Layer')

	with Modifier() as mod:

		id_aov = None

		for aov in rLayer.children():
			if aov.PlugName.get() == 'Id':
				print('ID pass found.')
				id_pass = aov.PlugName.get()
				id_aov = aov
			else:
				raise ValueError('No Id Pass found.')
		if id_aov:
			
			id_aov.OverrideSettings.set(True)
			id_aov.FileName.set(aov_path)
			id_aov.DisplayDriver.set('exrid')

	path += '\\exrid'
	if os.path.exists(path):
		if len(os.listdir(path)) > 0:
			raise ValueError('This folder already exists and has objects in it.')
		print('The folder already exists but is empty.')
	else:
		os.mkdir(path)

	aov_path = path + '\\' + filename

	return aov_path


def launch_new(mode='farm', file_ext='png', qual='LD_', local=False, frames=None, exrid=True):
	'''

	'''
	# Get file name / path and job path
	render_path, render_local_path, job_path = get_paths()

	#passer  en mode hyperespace

	rPass = None
	rPass = li.get_Rpass()
	prefs = pynode('Preferences')
	
	# Versionning
	day, hour = format_time()

	folder = day + '_' + hour + '.' + mode.lower()
	render_path = render_path + '/' + folder

	os.system('setx IMAGES ' + render_path)
	out_image_vars = 'out' + '_$n_$04f.$x'
	try:
		os.mkdir(render_path)
		if exrid == True:
			#aov_path = exrId(render_path, out_image_vars)
			pass
	except:
		raise Exception('ARRETE TOI')

	out_image_name = render_path + '/' + out_image_vars
	out_pass_name = '$o'
	with Modifier() as mod:
		rPass.FileName.set(out_image_name)


	quality_settings = var_render + qual
	with Modifier() as mod:
		prefs.RenderfarmSequence.set(quality_settings)
		rPass.FileName.set(out_image_name)
		rPass.FileLayerName.set(out_pass_name)

		rPass.DisplayDriver.set(file_ext)


	# Job Path => temporary ?

	job_path = render_path + '/' + 'jobs'
	os.mkdir(job_path)

	if frames:
		opts = dict({'JobsDirectory':job_path, 'RibsDirectory':job_path, 'Frames':frames})
	else:
		opts = dict({'JobsDirectory':job_path, 'RibsDirectory':job_path})

	# Render the images

	guerilla.render(mode,opts)

	# revenir en mode local

	out_image_name = render_local_path + '/' + out_image_vars

	with Modifier() as mod:
		rPass.FileName.set(out_image_name)