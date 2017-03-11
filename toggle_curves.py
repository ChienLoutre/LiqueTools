import maya.cmds as mc

current_panel = mc.getPanel(up=True)
curves_visibility = mc.modelEditor(current_panel, q=True, nurbsCurves=True)
if curves_visibility == True:
    try:
        mc.modelEditor(current_panel, e=True, nurbsCurves=False)
    except:
        pass
else:
    try:
        mc.modelEditor(current_panel, e=True, nurbsCurves=True)
    except:
        pass