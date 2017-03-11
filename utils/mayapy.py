import os
import subprocess


def launch_mayapy(flags = ' -i -c "import utils.clean_alembic.py"'):
	
	maya_path = 'C:\\Program Files\\Autodesk\\Maya2016\\bin\\mayapy.exe'

	cmd = maya_path + flags
	subprocess.Popen(cmd)