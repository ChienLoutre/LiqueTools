import maya.standalone
maya.standalone.initialize()
maya.standalone.initialize('Python')

import maya.cmds as mc
import utils.save as save
from variables import *
import time

print('hello !')

file_path = 'Y:/Liquefacteur/pipeline/prod/assets/chars/gerard/mod/V006/mod.ma'
mc.file(file_path , open=True)

save.version()

print('il se passe koua')
