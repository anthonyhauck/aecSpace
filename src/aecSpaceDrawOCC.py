import traceback

from OCC.Display.SimpleGui import init_display
import OCC.AIS
import OCC.Quantity
from OCC.gp import gp_Pnt
from OCC.gp import gp_Vec

#from OCC.Display import OCCViewer
from OCC.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCC.BRepBuilderAPI import BRepBuilderAPI_MakeWire
from OCC.BRepBuilderAPI import BRepBuilderAPI_MakeFace
from OCC.BRepPrimAPI import BRepPrimAPI_MakePrism

from aecErrorCheck import aecErrorCheck

"""
aecSpaceDraw accepts lists of aecSpaces to render in pythonOCC.
"""

class aecSpaceDrawOCC:
    
    def __init__(self):
        """
        aecSpaceDrawOCC Constructor
        Creates a new aecErrorCheck object.
        """
        self.__aecErrorCheck = aecErrorCheck()

    def makeEdges(self, pointPairs):
        """
        [Topo_DS_Edge,] makeEdges([[[gp_Pnt, gp_Pnt], [gp_Pnt, gp_Pnt]],...])
        Returns a list of Topo_DS_Edges derived from a list of gp_Pnt pairs.
        """
        try:
            edges = []
            for pair in pointPairs:
                newEdge = BRepBuilderAPI_MakeEdge(pair[0], pair[1])
                edges.append(newEdge.Edge())
            return edges
        except:
            traceback.print_exc()
    
    def makePointPairs(self, points):
        """
        [[[gp_Pnt, gp_Pnt], [gp_Pnt, gp_Pnt]],...] makePointPairs([gp_Pnt, gp_Pnt...])
        Returns a list of point pairs derived from a list of gp_Pnt points.
        """
        try:
            listLength = len(points)
            pointPairs = []
            x = 0
            while x < listLength:
                if x < (listLength - 1):
                    pointPairs.append([points[x], points[x + 1]])
                else:
                    pointPairs.append([points[x], points[0]])
                x += 1
            return pointPairs
        except:
            traceback.print_exc()
    
    def makePoints(self, space):
        """
        [gp_Pnt,] makePoints(aecSpace)
        Returns a list of gp_Pnts compatible with pythonOCC
        derived from the delivered aecSpace object.
        """
        try:
            return list(map (lambda pnt: gp_Pnt(pnt[0], pnt[1], pnt[2]), space.getPointsFloor()))
        except:
            traceback.print_exc()
    
    def makeWire(self, edges):
        """
        Topo_DS_Wire makeWire([Topo_DS_Edge, Topo_DS_Edge,...])
        Returns a pythonOCC Wire object constructed
        from the delivered list of Topo_DS_Edges.
        """
        try:
            wire = BRepBuilderAPI_MakeWire(edges[0])
            del edges[0] 
            for edge in edges:
                wire.Add(edge)
            return wire
        except:
            traceback.print_exc()
    
    def draw3D(self, spaces):
        """
        draw3D(pythonOCC display, [aecSpace,])
        Accepts a list of aecSpaces and renders them to the pythonOCC display.
        """
        try:
            display, start_display, add_menu, add_function_to_menu = init_display()
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
                display.DisplayShape(
                        spaceVolume, 
                        color = spaceColor,
                        transparency = space.getTransparency(),
                        update = False)
            display.FitAll()
            start_display()
            return True
        except:
            traceback.print_exc()

# end class

