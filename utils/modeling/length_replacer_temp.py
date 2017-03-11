import pymel.core as pmc
dist = pmc.ls('distanceDimensionShape1')
dist = pmc.getAttr(dist[0].distance)
print(dist)

base = pmc.ls('base_distance')
base = base[0]

sel = pmc.ls(sl=True)


offset = 0.0
new_locs = []


for each in sel:
    loc = pmc.createNode('locator')
    loc = pmc.listRelatives(loc, p=True)
    loc = loc[0]

    pmc.rename(loc, 'temp_loc_01')


    pmc.parent(loc, base)
    pmc.xform(loc, t=[0,0,0], r=True)
    
    for axis in ['x','y','z']:
        pmc.setAttr(str(loc) + '.t'+axis,0)
    
    offset = offset + dist/len(sel)
    pmc.setAttr(str(loc) + '.tx', offset)
    new_locs.append(loc)

for loc, new_loc in zip(sel, new_locs):
	print(loc, new_loc)
	
	cstr = pmc.pointConstraint(new_loc, loc, mo=False)
	pmc.delete(cstr)
    