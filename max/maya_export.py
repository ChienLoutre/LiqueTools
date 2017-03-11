import maya.standalone
maya.standalone.initialize()
maya.standalone.initialize('Python')

import maya.cmds as mc
import utils.save as save
import os
from variables import *
import time





obj_path = project_dir + '\\utils\\export\\mod'


file_path = open(obj_path + '.txt', 'r')
asset_path = file_path.read()
file_path.close()
charvalue = asset_path.split('\\')
version = charvalue[-2]
charvalue = charvalue[-4]


print('______________________________________________')
print('                                              ')
print('                                              ')

print('hello ! You are about to export the asset "' + charvalue + '" to Maya !')
print('                                              ')
print('Do NOT panic at the sight of this terrible black Window, it is totally NORMAL !!')

print('                                              ')
print('______________________________________________')


mc.file(obj_path + '.obj', i=True, type='OBJ', namespace=':')

mc.file(rename = asset_path + '\\' + 'mod.ma')
mc.file(save = True, type = 'mayaAscii')

os.remove(obj_path + '.obj')
os.remove(obj_path + '.txt')



print('______________________________________________')
print('                                              ')
print('                                              ')


print('The asset "' + charvalue + '" has been exported in Maya under the version : ' + version)
print('Thank you for your time ! You are AWESOME.')

print('You can now close this window.')



print('                                              ')
print('                                              ')
print('______________________________________________')
