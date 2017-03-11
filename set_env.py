# Set the Env Variable to the Project
# Ne pas utiliser // Conflit avec les scripts de Colin


import os
from shutil import copy

gversion = 'Guerilla_Render1.4.8'
os.system('setx GUERILLA_ROOT \\\\PLUG-MOPA\\GUERILLA_ROOT')
os.system('setx GUERILLA_CONF Y:\Liquefacteur\utils\guerilla_conf\guerilla.conf')
os.system('setx GUERILLA %GUERILLA_ROOT%\\' + gversion + '_py27')
os.system('setx GUERILLA_VERSION ' + gversion)
os.system('setx GUERILLA_PYTHON_LIBRARY C:\Python27')

# Maya Plugs

os.system('setx MAYA_PLUG_IN_PATH ' + '%MAYA_PLUG_IN_PATH%;Y:\\Liquefacteur\\utils\\plug-ins')
os.system('setx MAYA_SCRIPT_PATH ' + '%MAYA_SCRIPT_PATH%;Y:\\Liquefacteur\\utils\\scripts')
os.system('setx MAYA_MODULE_PATH ' + '%MAYA_MODULE_PATH%;Y:\\Liquefacteur\\utils\\modules')
os.system('setx MAYA_SHELF_PATH ' + '%MAYA_SHELF_PATH%;Y:\\Liquefacteur\\utils\\shelves')
os.system('setx PYTHONPATH ' + '%PYTHONPATH%;Y:\\Liquefacteur\\utils\\scripts')
#os.system('setx GUERILLA_PYTHON_LIBRARY C:\Windows\System32\python27.dll;C:\Windows\System32\python26.dll')
os.system('setx XBMLANGPATH  Y:\Liquefacteur\utils\icons')
os.system('setx PATH Y:\Liquefacteur\utils\scripts')
#os.system('setx LD_LIBRARY_PATH C:\Windows\System32\python27.dll')

# Nuke Plugs

os.system('setx NUKE_PATH Y:/Liquefacteur/utils/scripts/nukes/')


# Guerilla Shortcut

src = 'Y:\Liquefacteur\utils\icons\Liquerilla.lnk'
dst = 'D:\DirSysMOPA\ProfilesUsers\liquefacteur\Desktop'
copy(src, dst)

import ctypes
from variables import *
