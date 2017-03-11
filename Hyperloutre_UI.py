# INTERFACE 


import maya.cmds as mc
import os
import sys
from functools import partial
from variables import *
#import padding_numbers
import computer_working_directory as cwd

from utils import *


def doAsset(a, b, c):
    
    a = mc.textField('asset_name', query=True, text=True)
    b = mc.optionMenu('asset_type', query=True, value=True)
    b = b.lower()
    
    if a == '':
        sys.exit('No name given for the asset !')
    

    print (a)
    print (b)
    print (c)
    
    asset_creator.create_asset(a,b)


def openAsset(asset_path, asset_type, c):

    asset_name = mc.textField('asset_op_name', query=True, text=True)
    asset_type = mc.optionMenu('asset_op_type', query=True, value=True)
    fullpath = project_path_base + '/' + project_name + '/prod/assets/' + asset_type.lower() + '/' + asset_name
    pc_name = str(os.environ['COMPUTERNAME'])
    test = cwd.work_dir(pc_name)
    print(fullpath)
    print(test)
    
    # regarder si on veut ouvrir une certaine version d'asset
    # choper l'asset seul dans la liste des versions
    # virer son versionning
    # le copier dans un dossier temporaire
    # ecrire l'adresse de l'asset original quelque part
    # lancer l'asset    
    


asset_name = ''
asset_type = ''
asset_path = ''

asset_path = project_path_base + '/' + project_name + '/prod/assets/' + asset_type + '/' + asset_name + '/versions'

#asset_versions = os.listdir(asset_path)


# MAIN UI WINDOWS FOR PROJECT
proj_ui = project_name.capitalize() + '_Asset_Manager'

if mc.window(proj_ui, exists=True):
    mc.deleteUI(proj_ui)

mc.window(proj_ui, widthHeight=(400,400))

mc.columnLayout(adjustableColumn=True)
#mc.image(image = project_path_base + '/' + project_name + '/temp/doge_icon')
mc.separator(height = 10, style='none')
mc.text(label = proj_ui)
mc.separator(height = 30)


mc.columnLayout(adjustableColumn=True)

mc.text(label = 'Asset Creator')

mc.textField('asset_name', text='')
mc.optionMenu('asset_type', label='Type')
mc.menuItem( label='Chars' )
mc.menuItem( label='Props' )
mc.menuItem( label='Sets' )

mc.button(label='Create Asset', command = partial(doAsset, asset_name, asset_type))
mc.setParent('..')



mc.columnLayout(adjustableColumn=True)

mc.setParent('..')

mc.separator(height = 10)


# Asset Opener

mc.columnLayout(adjustableColumn=True)
mc.columnLayout(adjustableColumn=True)

mc.text(label='Asset Opener')
mc.separator(height = 6, style='none')

mc.textField('asset_op_name', text='')
mc.optionMenu('asset_op_type', label='Type')


mc.menuItem( label='Chars' )
mc.menuItem( label='Props' )
mc.menuItem( label='Sets' )

mc.button(label='Open Asset', command = partial(openAsset, asset_path, asset_type))

mc.separator(height = 6, style='none')





#mc.optionMenu( label='Version')

#for each in asset_versions:

#    mc.menuItem( label=each )

mc.setParent('..')    

mc.showWindow( proj_ui )



    

