import os
import subprocess


file = 'Y:\\Liquefacteur\\utils\\scripts\\max\\maya_export.py'


flags = ' -i -c "import max.maya_export.py"'
#file = 'Y:\\Liquefacteur\\pipeline\\prod\\assets\\chars\\gerard\\mod\\V006\\mod.ma'
maya_path = 'C:\\Program Files\\Autodesk\\Maya2016\\bin\\mayapy.exe'

cmd = maya_path + flags
print(maya_path)
subprocess.Popen(cmd)