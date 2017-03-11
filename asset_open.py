import maya.cmds as mc
import utils
from variables import *
reload(utils)

import symbolic_link
reload(symbolic_link)

asset_location = 'd:/travail/supinfocom/final/pipe_tester/liquefacteur/prod/assets/Chars/prout'
asset_version = 'versions/prout_001.ma'
asset_name = 'prout_001.ma'
symbolic_link.sym_link(asset_location + '/versions', asset_name)


file_path = asset_location + '/' + asset_version

mc.file(file_path,open = True)