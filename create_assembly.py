# CREATE ASSEMBLY
# METTRE LES BONS CHEMINS !!!!


import maya.cmds as mc
import os
import sys
from variables import *


# Verifier que l'on est dans le projet

project_path_temp = project_path_base + '/' + project_name + '/temp/'


if not project_name in project_path_temp:

	sys.exit('You are not working in the Project !!')


export_name = 'vive_les_chiens'


filename = project_path_temp + export_name
export_settings = "-frameRange 1 1 -uvWrite -worldSpace -writeCreases -dataFormat ogawa -file " + project_path_temp + export_name + '.abc'


# Fenetre de dialogue prevenant si on a bien sauve la scene

go_on = mc.confirmDialog(title='Exporting as Alembic : ' + export_name , message = "Your current file won't be saved, are you sure ?", button =['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No')

if go_on == 'No':
    
    sys.exit('Export successfully aborted.')



mc.AbcExport( j = export_settings)
mc.file(rename =  filename)
mc.file(save=True, type = 'mayaBinary')

mc.file(new=True)

assembly_name = export_name + '_ass'

# SOCCUPER DE CA :

# DEFINIR LES LABELS GPU ET GEO

#
mc.assembly(name='MyAssembly')
#Create an assembly of type MyAssemblyType and name it MyAssembly.
#
mc.assembly(name='MyAssembly', defaultType='Bite')


mc.assembly(n=assembly_name)


mc.assembly(assembly_name, edit=True, createRepresentation='Locator', repName=export_name + '_loc', input=export_name)
mc.assembly(assembly_name, edit=True, createRepresentation='Cache', repName = export_name + '_gpu',input=filename + '.abc', type='Cache')
mc.assembly(assembly_name, edit=True, createRepresentation='Scene', repName = export_name + '_geo', input=filename + '.mb', type='Scene')


mc.file(rename =  filename + '__ass')
mc.file(save=True, type = 'mayaBinary')

mc.file(new=True)

go_on = mc.confirmDialog(title='Assembly for : ' + export_name + ' is DONE !' , message = "The assembly has been saved to " + project_path_temp, button =['Great !'], defaultButton='Great !',dismissString='Great !')


