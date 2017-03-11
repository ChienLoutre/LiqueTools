# EXPORT FINAL ASSEMBLY EN ALEMBIC
# METTRE LES BONS CHEMINS !!!!
# RECUPERER MODE DANS ASSEMBLY !!!

import maya.cmds as mc
import os
from variables import *

# Verifier que l'on est dans le projet

project_path_temp = project_path_base + '/' + project_name + '/temp/'


if not project_name in project_path_temp:

	sys.exit('You are not working in the Project !!')


export_name = 'vivelesloutres'


filename = project_path_temp + export_name
export_settings = "-frameRange 1 1 -uvWrite -worldSpace -writeCreases -dataFormat ogawa -file " + project_path_temp + export_name + '.abc'


# Fenetre de dialogue prevenant si on a bien sauve la scene

go_on = mc.confirmDialog(title='Exporting as Alembic : ' + export_name , message = "Your current file won't be saved, are you sure ?", button =['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No')

mc.AbcExport( j = export_settings)
