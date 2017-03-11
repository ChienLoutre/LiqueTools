import maya.cmds as mc

def toggle_slide():

	q_constraint = mc.xformConstraint(q=True, type=True)
	print(q_constraint)
	if q_constraint == 'none':
		q_constraint = mc.xformConstraint(type='edge')
		mc.warning('edge constraint activated.')
	elif q_constraint == 'edge':
		q_constraint = mc.xformConstraint(type='surface')
		mc.warning('surface constraint activated.')
	elif q_constraint == 'surface':
		q_constraint = mc.xformConstraint(type='none')
		mc.warning('No constraint activated.')
