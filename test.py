import maya.cmds as mc
import os
import sys
from variables import *

# PROJECT CREATOR

retval = os.getcwd()

print "Working directory is : %s" % retval

os.chdir(project_path_base)
retval = os.getcwd()

print "Working directory changed to : %s" % retval

project_path = project_path_base + '/' + project_name
