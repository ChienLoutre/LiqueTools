import maya.cmds as mc
import re

def ch4_rivet( name='rivet' ):
    '''
    Launch build rivet for between given edges or on each given faces
    name : string > to define the rivet name
    '''
    
    #--- Load needed plugin
    load_plugin( toLoad= ['rotateHelper', 'matrixNodes' ] )
    
    #--- Get subComponent Selection
    sels = mc.ls(sl=True)
    
    #--- keep only edges and faces
    edges = mc.filterExpand(sels, sm=32) or []
    faces = mc.filterExpand(sels, sm=34) or []
    
    #--- Launch Build
    if len(edges) == 2 :
        #--- Create a rivet inbetween to edges
        ch4_build_rivet(name, edges[0], edges[1])
    elif faces :
        for face in faces:
            #--- Create a rivet for each face selected
            edges = ch4_convert_face_to_edges(face)
            print edges
            ch4_build_rivet(name, edges[0], edges[1])
    else:
        print 'select 2 edges or faces to build rivet'

def load_plugin( toLoad= list() ):
    '''
    Check if the needed plugin already load. if not loaded, load and autoload check for the plugin
    
    :param toLoad: A list of the plugin name to load.
    :type toLoad: list
    '''
    # Get the plugin already loaded
    plugin_loaded = mc.pluginInfo( query=True, listPlugins=True )
    
    for plugin in toLoad:
        # Check if the plugin wasn't already load
        if not plugin in plugin_loaded:
            # Load plugin
            mc.loadPlugin( plugin )
        # autoLoad plugin
        if not mc.pluginInfo( plugin, query=True, autoload=True ):
            mc.pluginInfo( plugin, edit=True, autoload=True )

def ch4_convert_face_to_edges(face):
    '''
    For a given face return two uncontinus edges
    face : string > the full face name
    '''
    #--- convert face to edges
    edges = mc.ls( mc.polyListComponentConversion( face, ff=True, te=True ), fl=True )

    #--- For 3edges Faces return the 2 first edges
    if len(edges) == 3:
        return [edges[0], edges[1]]

    #--- Create a vertex set with the first edge
    setEdgeA = set(mc.ls(mc.polyListComponentConversion(edges[0], fe=True, tv=True), fl=True))
    
    #--- Search an edge without commun vertex
    for i in range( 1, len(edges) ):
        setEdgeB = set(mc.ls(mc.polyListComponentConversion(edges[i], fe=True, tv=True), fl=True))
        if not setEdgeA & setEdgeB:
            #--- return uncontinus edges
            return [edges[0], edges[i]]


def ch4_build_rivet(name, edgeA, edgeB):
    '''
    Build a rivet between two given edges
    Edges can be from different mesh
    returns the created rivet name

    name  : string > to define the rivet name
    edgeA : string > the full edge name
    edgeB : string > the full edge name
    '''
    #---  init
    objA = edgeA.split('.')[0]
    objB = edgeB.split('.')[0]
    

    #--- Create Locator Rivet
    rivet = mc.spaceLocator(n=name)[0]
    
    #---  Create nodes
    nodes = []
    nodes.append( mc.createNode('curveFromMeshEdge', n= rivet + '_%s_Crv' %(objA)) )        # 0
    nodes.append( mc.createNode('curveFromMeshEdge', n= rivet + '_%s_Crv' %(objB)) )        # 1
    nodes.append( mc.createNode('loft', n= rivet + '_loft') )                               # 2
    nodes.append( mc.createNode('pointOnSurfaceInfo', n= rivet + 'pointOnSurfaceInfo') )    # 3
    nodes.append( mc.createNode('rotateHelper', n= rivet + '_rotateHelper') )               # 4
    nodes.append( mc.createNode('decomposeMatrix', n= rivet + '_decomposeMatrix') )         # 5
    
    #--- Set Nodes Connections
    #- Crv 1
    mc.setAttr( nodes[0] + '.ei[0]', int(re.findall('\d+', edgeA)[-1]))
    mc.connectAttr( objA + '.w', nodes[0] + '.im', f=True)
    
    #- Crv 2
    mc.setAttr( nodes[1] + '.ei[0]', int(re.findall('\d+', edgeB)[-1]))
    mc.connectAttr( objB + '.w', nodes[1] + '.im', f=True)
    
    #- Loft
    mc.setAttr( nodes[2] + '.ic', size=2)
    mc.setAttr( nodes[2] + '.u', True)
    mc.setAttr( nodes[2] + '.rsn', True)
    mc.connectAttr( nodes[0] + '.oc', nodes[2] + '.ic[0]', f=True) # COnnect Crv 1 to Loft
    mc.connectAttr( nodes[1] + '.oc', nodes[2] + '.ic[1]', f=True) # COnnect Crv 2 to Loft

    #- Point on surface info
    mc.setAttr( nodes[3] + '.turnOnPercentage', True)
    mc.connectAttr( nodes[2] + '.os', nodes[3] + '.is', f=True) # Connect Loft to Point on Surface Info

    #- Get Rotate
    mc.connectAttr( nodes[3] + '.normal', nodes[4] + '.up' ) # Connect PtsOnSurface normal to rotateHelper
    mc.connectAttr( nodes[3] + '.tangentV', nodes[4] + '.forward' ) # Connect PtsOnSurface tangentv to rotateHelper
    mc.connectAttr( nodes[4] + '.rotateMatrix', nodes[5] + '.inputMatrix' ) # Connect rotateHelper to decomposeMatrix

    #--- Drive Rivet
    mc.connectAttr( nodes[3] + '.positionX', rivet + '.translateX' )
    mc.connectAttr( nodes[3] + '.positionY', rivet + '.translateY' )
    mc.connectAttr( nodes[3] + '.positionZ', rivet + '.translateZ' )
    
    mc.connectAttr( nodes[5] + '.outputRotateX', rivet + '.rotateX' )
    mc.connectAttr( nodes[5] + '.outputRotateY', rivet + '.rotateY' )
    mc.connectAttr( nodes[5] + '.outputRotateZ', rivet + '.rotateZ' )

    #--- Add Ctrl attributes to rivet
    mc.addAttr(rivet, ln='posU', at='float', min=.0, max=1.0, dv=.5, k=True)
    mc.addAttr(rivet, ln='posV', at='float', min=.0, max=1.0, dv=.5, k=True)
    
    mc.connectAttr( rivet + '.posU', nodes[3] + '.parameterU', f=True)
    mc.connectAttr( rivet + '.posV', nodes[3] + '.parameterV', f=True) 

    #--- Historical intereset
    for node in nodes :
        mc.setAttr( node + '.ihi', 0)
    
    mc.setAttr( rivet + 'Shape.ihi', 0)
    
    #--- Clean
    for attr in ['t', 'r', 's'] :
        for axis in ['x', 'y', 'z'] :
            mc.setAttr('%s.%s%s' %(rivet, attr, axis), k=False)
    for axis in ['X', 'Y', 'Z'] :
        mc.setAttr('%sShape.localPosition%s' %(rivet, axis), k=False, cb=False)

    return rivet
