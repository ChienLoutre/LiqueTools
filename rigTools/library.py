import math
from maya import cmds
from constants import PARSELIST, JNT_SUFFIX, SPACE
 
""" 
The MIT License (MIT)

Copyright (c) 2015 Mat Leonard

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
class Vector(object):
    def __init__(self, *args):
        """ Create a vector, example: v = Vector(1,2) """
        if len(args)==0: self.values = (0,0,0)
        else: self.values = args

        
    def norm(self):
        """ Returns the norm (length, magnitude) of the vector """
        return math.sqrt(sum( comp**2 for comp in self ))
        
    def argument(self):
        """ Returns the argument of the vector, the angle clockwise from +y."""
        arg_in_rad = math.acos(Vector(0,1,0)*self/self.norm())
        arg_in_deg = math.degrees(arg_in_rad)
        if self.values[0]<0: return 360 - arg_in_deg
        else: return arg_in_deg

    def normalize(self):
        """ Returns a normalized unit vector """
        norm = self.norm()
        normed = tuple( comp/norm for comp in self )
        return Vector(*normed)
    
    def rotate(self, *args):
        """ Rotate this vector. If passed a number, assumes this is a 
            2D vector and rotates by the passed value in degrees.  Otherwise,
            assumes the passed value is a list acting as a matrix which rotates the vector.
        """
        if len(args)==1 and type(args[0]) == type(1) or type(args[0]) == type(1.):
            # So, if rotate is passed an int or a float...
            if len(self) != 2:
                raise ValueError("Rotation axis not defined for greater than 2D vector")
            return
        elif len(args)==1:
            matrix = args[0]
            if not all(len(row) == len(v) for row in matrix) or not len(matrix)==len(self):
                raise ValueError("Rotation matrix must be square and same dimensions as vector")
            return self.matrix_mult(matrix)
        
        
    def matrix_mult(self, matrix):
        """ Multiply this vector by a matrix.  Assuming matrix is a list of lists.
        
            Example:
            mat = [[1,2,3],[-1,0,1],[3,4,5]]
            Vector(1,2,3).matrix_mult(mat) ->  (14, 2, 26)
         
        """
        if not all(len(row) == len(self) for row in matrix):
            raise ValueError('Matrix must match vector dimensions') 
        
        # Grab a row from the matrix, make it a Vector, take the dot product, 
        # and store it as the first component
        product = tuple(Vector(*row)*self for row in matrix)
        
        return Vector(*product)
    
    def inner(self, other):
        """ Returns the dot product (inner product) of self and other vector
        """
        return sum(a * b for a, b in zip(self, other))
    
    def __mul__(self, other):
        """ Returns the dot product of self and other if multiplied
            by another Vector.  If multiplied by an int or float,
            multiplies each component by other.
        """
        if type(other) == type(self):
            return self.inner(other)
        elif type(other) == type(1) or type(other) == type(1.0):
            product = tuple( a * other for a in self )
            return Vector(*product)
    
    def __rmul__(self, other):
        """ Called if 4*self for instance """
        return self.__mul__(other)
            
    def __div__(self, other):
        if type(other) == type(1) or type(other) == type(1.0):
            divided = tuple( a / other for a in self )
            return Vector(*divided)
    
    def __add__(self, other):
        """ Returns the vector addition of self and other """
        added = tuple( a + b for a, b in zip(self, other) )
        return Vector(*added)
    
    def __sub__(self, other):
        """ Returns the vector difference of self and other """
        subbed = tuple( a - b for a, b in zip(self, other) )
        return Vector(*subbed)
    
    def __iter__(self):
        return self.values.__iter__()
    
    def __len__(self):
        return len(self.values)
    
    def __getitem__(self, key):
        return self.values[key]
        
    def __repr__(self):
        return str(self.values)
        
    def x(self):
        return self.values[0]
        
    def y(self):
        return self.values[1]
        
    def z(self):
        return self.values[2]

# -------------------------------------
# Create orig on selected objects
# by felixlechA and xtof
# -------------------------------------




def create_orig_on_selected(cSelection = None, suffix = 'zero'):
    ''''''
    returnList = []
    if not cSelection:
        # Get Current selection
        cSelection = cmds.ls( sl = True )
    elif not isinstance(cSelection,list):
        cSelection = [cSelection]
        
    for sSel in cSelection:
        # Get Parent
        s_parent = cmds.listRelatives( sSel, p= True )
        if s_parent:
            s_parent= s_parent[0]

        # Get current Obj Transform
        lPos_Sel = cmds.xform( sSel, q=True, t=True, ws=True )
        lRot_Sel = cmds.xform( sSel, q=True, ro=True, ws=True )
        
        # Create a group
        s_name = sSel
        
        # extract suffix from current object
        parse_suffix = s_name.rpartition(SPACE)[2]
        
        if parse_suffix == s_name:
            parse_suffix =""
            
        # remove suffix from current object
        if parse_suffix in PARSELIST:
            suffix_in_List = PARSELIST[PARSELIST.index(parse_suffix)]
            s_name= s_name.replace(suffix_in_List, '')
            
        # add Orig suffix to orig name        s_name = s_name + suffix
        s_name += suffix
        
        typ = cmds.objectType(sSel)
        
        if typ == 'joint':
            sGroup = cmds.createNode( 'joint', name= s_name )
            cmds.setAttr(sGroup + '.drawStyle',2)
        elif typ == 'transform':
            sGroup = cmds.group( em=True, name= s_name )
        else:
            return
        
        # Set in place
        cmds.xform( sGroup, a=True, t=lPos_Sel, ro=lRot_Sel, s=[1,1,1] )
        
        # Parent current to orig Group
        cmds.parent( sSel, sGroup, relative= False )
        
        # reParent group to original parent
        if s_parent:
            cmds.parent( sGroup, s_parent, relative= False )
        returnList.append(sGroup)
    return returnList

	
def create_bones_from_length( nb_joints, length, name='spine', suffix=JNT_SUFFIX, axis= [1.0,0.0,0.0]):
    returnList = []
    length_per_bone = 1.0 * length / nb_joints
    
    for iter in range(0,nb_joints+1,1):
        
        if iter == 0:
            mult = 0
        else:
            mult = 1.0
            
        if iter == nb_joints:
            iter='x'
            
        jnt = cmds.joint(p=[length_per_bone*mult*axis[0], length_per_bone*mult*axis[1], length_per_bone*mult*axis[2]], r=True, n=name + '_'+ str(iter) + suffix)
        returnList.append( jnt )
        
    return returnList