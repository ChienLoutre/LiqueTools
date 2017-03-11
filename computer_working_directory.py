# Computer switch directory
#
# This script chooses the path for each computer and allows each person to work on a local directory (by the person's choosing)

from utils import *

def work_dir(pc_name):

	if pc_name != 'CHIENLOUTRE-PC':
		
		pc_path = 'd:/travail/supinfocom/final'

	else:

		pc_path = 'D:/travail/supinfocom/final/pipe_tester/liquefacteur/temp'


	return pc_path