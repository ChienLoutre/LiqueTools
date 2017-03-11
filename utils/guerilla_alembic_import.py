# IMPORT ALEMBIC ASSEMBLY INTO GUERILLA


from guerilla import Modifier, pynode
with Modifier() as mod:

	assembly_path = 'D:\\travail\\supinfocom\\final\\pipe_tester\\liquefacteur\\temp\\test.abc'
	parent_name = 'shot_01'
	ref_name = 'test'
	parent_name = mod.createnode(parent_name, type = 'SceneGraphNode')
	refNode, topNodes = mod.createref(ref_name, assembly_path, parent_name, {'prefixnodes':False,'containschildren':False})