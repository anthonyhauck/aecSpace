import OCC.AIS
import OCC.Quantity
from OCC.gp import gp_Pnt
from OCC.gp import gp_Vec
from OCC.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCC.BRepBuilderAPI import BRepBuilderAPI_MakeWire
from OCC.BRepBuilderAPI import BRepBuilderAPI_MakeFace
from OCC.BRepPrimAPI import BRepPrimAPI_MakePrism
import traceback
from aecSpace import aecSpace
from aecErrorCheck import aecErrorCheck

# -------------------------------------------------------------------------   
# aecSpaceDraw accepts lists of spaces to draw in 3D
# -------------------------------------------------------------------------   

class aecSpaceDrawOCC:
    
    # __aecErrorCheck is an instance of aecErrorCheck
    
    __aecErrorCheck = None
    
# -------------------------------------------------------------------------    
# aecSpaceDrawOCC Constructor
# -------------------------------------------------------------------------    
    
    def __init__(self):
        self.__aecErrorCheck = aecErrorCheck()
    # end constructor    

# -------------------------------------------------------------------------   
# makeEdges(point pairs)
#
# Returns a list of edges derived from a list of gp_Pnt pairs.
# -------------------------------------------------------------------------       
    
    def makeEdges(self, pointPairs):
        try:
            edges = []
            for pair in pointPairs:
                newEdge = BRepBuilderAPI_MakeEdge(pair[0], pair[1])
                edges.append(newEdge.Edge())
            # end for
            return edges
        except:
            return self.__aecErrorCheck.aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)
    # end def

# -------------------------------------------------------------------------   
# makePointPairs(points)
#
# Returns a list of point pairs derived from a list of gp_Pnt points.
# -------------------------------------------------------------------------       
    
    def makePointPairs(self, points):
        try:
            listLength = len(points)
            pointPairs = []
            x = 0
            while x < listLength:
                if x < (listLength - 1):
                    pointPairs.append([points[x], points[x + 1]])
                else:
                    pointPairs.append([points[x], points[0]])
                # end if
                x += 1
            # end for
            return pointPairs
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)
    # end def
    
# -------------------------------------------------------------------------   
# makePoints(space)
#
# Returns a list of display points derived from the delivered Space
# -------------------------------------------------------------------------       
    
    def makePoints(self, space):
        try:
            return list(map (lambda pnt: gp_Pnt(pnt[0], pnt[1], pnt[2]), space.getPoints3D()))
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)
    # end def
    
# -------------------------------------------------------------------------   
# makeWire(list of edges)
#
# Returns a wire from a list of Topo_DS_Edges.
# -------------------------------------------------------------------------       
    
    def makeWire(self, edges):
       try:
            wire = BRepBuilderAPI_MakeWire(edges[0])
            del edges[0] 
            for edge in edges:
                wire.Add(edge)
            # end for
            return wire
       except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)
    # end def

# -------------------------------------------------------------------------   
# spacedraw3D(list of space objects)
#
# Draws one or more Space volumes
# -------------------------------------------------------------------------   
    
    def Draw3D(self, display, spaces):
#        try:           
            for space in spaces:         
                points = self.makePoints(space)
                pointPairs = self.makePointPairs(points)
                edges = self.makeEdges(pointPairs)
                wire = self.makeWire(edges)
                face = BRepBuilderAPI_MakeFace(wire.Wire())
                vector = gp_Vec(0, 0, space.getHeight())
                spaceVolume = BRepPrimAPI_MakePrism(face.Face(), vector).Shape()
                displayColor = space.getColor01()
                spaceColor = OCC.Quantity.Quantity_Color_Name(
                    displayColor[0],
                    displayColor[1],
                    displayColor[2])
                aisSpace = display.DisplayShape(
                    spaceVolume,
                    color = spaceColor,
                    update = True)
                display.Context.SetTransparency(
                    aisSpace, 
                    space.getTransparency())
            # end for
            return True
#        except:
#            return self.__aecErrorCheck.errorMessage \
#            (self.__class__.__name__, traceback)

#end class

