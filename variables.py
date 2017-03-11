# VARIABLES
import os

default_path = 'D:/DirSysMOPA/pref_maya_liquefacteur/projects/default'
project_path_base = 'Y:/Liquefacteur'
project_name = 'pipeline'
manager_name = 'Liquemanager'
project_dir = project_path_base + '/' + project_name
guerillabank = project_dir + '/utils/guerilla/guerillabank'
fullpath = os.path.expanduser(os.path.join(project_path_base, project_name))
pad = 3
pc_name = os.environ['COMPUTERNAME']

# compositing settings

channels = ['Beauty', 'Diffuse', 'Specular', 'SSS', 'Reflection', 'Albedo', 'Refraction', 'IndDiffuse']


# render settings

var_render = 'liquefacteur_'
quality = ['HD_','LD_','TEST_']
file_format = ['exr', 'png', 'tiff']