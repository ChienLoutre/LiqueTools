import sys
import subprocess
from variables import *
import os

def sym_link(file_path = project_dir, file_name = 'project_sym_link'):

	print("creating symbolic link file...")
	print(file_path)
	bat_file_dir = project_dir + '/04_sandbox/' + file_name
	bat_file_dir_list = bat_file_dir.split('/')
	bat_file_dir = '\\'.join(bat_file_dir_list)
	print bat_file_dir
	name_pathlist = file_path.split('/')
	name_path = '\\'.join(name_pathlist)

	print('name_path ===' + name_path)

	extension='.bat'

	# inserer fonction pour faire degager l'extension
	# en attendant je le code salement

	name = file_name

	print ('file_name de base ===' + name)

	namelist = name.split('.')
	name = namelist[0]

	print name

	bat_file_dir = project_dir + '/04_sandbox/' + name
	bat_file_dir_list = bat_file_dir.split('/')
	bat_file_dir = '\\'.join(bat_file_dir_list)
	bat_file_dir = bat_file_dir + extension
	name = name + extension

	# fin du code sale a remplacer

	name = file_path + '/' + name

	print name
	namelist = name.split('/')
	name = '\\'.join(namelist)

	
	work_dir = 'D:%sDirSysMOPA%sProfilesUsers%sliquefacteur%s' %(os.sep,os.sep,os.sep,os.sep)

	print ('bat_file_dir   =  ' + bat_file_dir)
	try:
		
		file=open(bat_file_dir,'w')
		
		file.write('mklink /j "' + work_dir + project_name + '" "' + name_path+ '"')

		file.close()
		
		
		os.chdir(work_dir)
		retval = os.getcwd()

		print "Working directory changed to : %s" % retval

		filepath=bat_file_dir

		print("filepath === " + filepath)
		p = subprocess.Popen(filepath, shell=True, stdout = subprocess.PIPE)

		stdout, stderr = p.communicate()
		print p.returncode # is 0 if success
		print ('Lien symbolique cree entre : ' + name_path + '   <========>   ' + work_dir)


		
	except:
			print("error occured")
			sys.exit(0)