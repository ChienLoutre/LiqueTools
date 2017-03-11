import pymel.core as pmc
import maya.cmds as mc
from math import *
from random import *
import utils.autorig as ar
import utils.padding_numbers as pn

def coin_toss():
	result = choice([0,1])
	return result


def floatToInt(value):
	value = ceil(value)
	value = int(value)
	return value


def paperbloc_base(w,d,h,name):

	name_fill = name + '_fill'
	d=d
	w=w
	h=h
	sw = floatToInt(w)
	sh = floatToInt(h)
	sd = floatToInt(d)

	bloc = pmc.polyCube(n=name + '__temp', w=w, d=d, h=h, sx=sw, sz=sd, sy=sh)
	fill = pmc.polyPlane(n=name_fill + '__temp', w=w, h=d, sx=sw, sy=sd)


	fCount =  pmc.polyEvaluate(bloc[0],f=True)
	sel = pmc.select(bloc[0].f + '[0:'+str(fCount)+']')
	pmc.move(h/2,y=True, r=True)
	pmc.select(cl=True)

	sel = pmc.ls(fill[0], bloc[0])


	return sel




def paperbloc_gen(sel=None, w=21.0, d=29.7, h=2 ,num_sheets=10, max_xz = 0.5, max_rot = 10.0, name='paperbloc'):

	sel = paperbloc_base(w,d,h,name)

	if not sel:
		# Get Current selection
		sel = pmc.ls(sl = True)

	elif not isinstance(sel,list):
		sel = [sel]

	if len(sel) != 2:
		raise ValueError('Select Two Objects please, the fill paper and the paper bloc.')
	
	sSel = sel

	bloc_paper = sel[-1]
	sel= sel[0]
	print(bloc_paper)
	# check if the name already is in the scene

	i = 0
	num = 1
	while i < num:
		chk = pmc.ls(name + '_' + str(i))
		if chk:
			num +=1
		i += 1
		if i == num:
			num -= 1


	name_grp = name + '_grp_' + str(num)
	name_fill = name + '_fill_' + str(num)
	name = name + '_' + str(num)
	bloc_paper = pmc.duplicate(bloc_paper, n=name)
	fill_sheets = [bloc_paper[0]]
	#raise ValueError('STOP DOGGIE')

	for i in range(num_sheets):
	

		r_seed_x = random()*max_xz
		r_seed_y = random()*h
		r_seed_z = random()*max_xz
		r_seed_rot = random()*max_rot

		coin = coin_toss()
		if coin == 1:
			r_seed_rot = -r_seed_rot
		coin = coin_toss()
		if coin_toss == 1:
			r_seed_z = -r_seed_z
		coin = coin_toss()
		if coin_toss == 1:
			r_seed_x = -r_seed_x

		base_y = pmc.getAttr(sel.translateY)
		y_val = r_seed_y + base_y
		n_paper = pmc.duplicate(sel, n=name_fill)
		n_paper = n_paper[0]
		
		coin = coin_toss()
		if coin == 1:

			r_pivotx = random()*10.0
			r_pivotz = random()*10.0

			coin = coin_toss()
			if coin == 1:
				r_pivotx = -r_pivotx
			coin = coin_toss()
			if coin == 1:
				r_pivotz = -r_pivotz
			pmc.move(n_paper.rotatePivot, r_pivotx,0,r_pivotz)
	
		pmc.setAttr(n_paper.ty, y_val)
		pmc.setAttr(n_paper.tx, r_seed_x)
		pmc.setAttr(n_paper.tz, r_seed_z)
		pmc.setAttr(n_paper.ry, r_seed_rot)
		
		fill_sheets.append(n_paper)

	print('---------feuilles placees -----------')

	print(fill_sheets)


	bender = pmc.nonLinear(fill_sheets, type='bend')

	print('bend creation')

	pmc.rename(bender[0], name + '__bend')
	pmc.rename(bender[-1], name + '__bendHandle')
	
	print('---------bend done -----------')

	pmc.setAttr(bender[-1].rotateZ, 90)
	fill_sheets.append(bender[0])
	fill_sheets.append(bender[-1])
	grp = pmc.group(em=True, n=name_grp)
	pmc.setAttr(grp.ty, base_y)
	pmc.parent(fill_sheets, grp)
	ar.zero_out(mc.ls(str(bender[-1])))
	
	pmc.addAttr(grp, ln='bend_me', at='float', k=True)
	pmc.addAttr(grp, ln='bend_shift', at='float', k=True)
	pmc.addAttr(grp, ln='bend_min', at='float', min=-10, dv=-1, max=0, k=True)
	pmc.addAttr(grp, ln='bend_max', at='float', min=0, dv=1, max=10, k=True)
	pmc.addAttr(grp, ln='pos_bendx', at='float', k=True)
	pmc.addAttr(grp, ln='pos_bendz', at='float', k=True)


	pmc.connectAttr(grp.bend_me, bender[0].curvature)
	pmc.connectAttr(grp.bend_shift, bender[-1].rx)
	pmc.connectAttr(grp.bend_min, bender[0].lowBound)
	pmc.connectAttr(grp.bend_max, bender[0].highBound)
	pmc.connectAttr(grp.pos_bendx, bender[-1].ty)
	pmc.connectAttr(grp.pos_bendz, bender[-1].tz)

	pmc.delete(sSel)
	pmc.select(pmc.ls(grp))
	return grp