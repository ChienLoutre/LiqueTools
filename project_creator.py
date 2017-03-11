import os
import sys
import mkfolder
from variables import *

# PROJECT CREATOR

retval = os.getcwd()

print "Working directory is : %s" % retval

os.chdir(project_path_base)
retval = os.getcwd()

print "Working directory changed to : %s" % retval

project_path = project_path_base + '/' + project_name


if not os.path.exists(project_path):
#    os.mkdir(project_path)
#    os.chmod(project_path, 777)
	mkfolder.cr_folder(project_path, 777)

else :
    print 'folder already exists !'
    sys.exit('folder already existing => please choose another name or location, or delete the folder if you created one by mistake.')

subpath = project_path + '/preprod'

# sous dossiers

os.mkdir(subpath)
os.mkdir(subpath + '/refs')
os.mkdir(subpath + '/concept')
os.mkdir(subpath + '/scenario')
os.mkdir(subpath + '/animatic')


subpath = project_path + '/prod'
os.mkdir(subpath)

# sous dossiers
# assets, sequences

os.mkdir(subpath + '/seq')

subpath = project_path + '/prod'
subpath = subpath + '/assets'
os.mkdir(subpath)



subpath = project_path + '/prod/assets'
os.mkdir(subpath + '/chars')
os.mkdir(subpath + '/props')
os.mkdir(subpath + '/sets')


subpath = project_path + '/prod/seq'

# meme arborescence que PROD

subpath = project_path + '/post'
os.mkdir(subpath)
os.mkdir(subpath + '/seq')


subpath = project_path + '/sandbox'
os.mkdir(subpath)

subpath = project_path + '/utils'
os.mkdir(subpath)
os.mkdir(subpath + '/scripts')
os.mkdir(subpath + '/icons')


#mc.workspace(fullpath, n=True)
#mc.workspace(fullpath, o=True)
#mc.workspace(fullpath, s=True)
#mc.workspace(lw=True)

print "Project successfully created in " + project_path_base + " !!"






