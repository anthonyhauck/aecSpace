import traceback

from OCC.Display.SimpleGui import init_display
import OCC.AIS
import OCC.Quantity
from OCC.gp import gp_Pnt
from OCC.gp import gp_Vec

from OCC.Display import OCCViewer
from OCC.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCC.BRepBuilderAPI import BRepBuilderAPI_MakeWire
from OCC.BRepBuilderAPI import BRepBuilderAPI_MakeFace
from OCC.BRepPrimAPI import BRepPrimAPI_MakePrism

"""
aecSpaceDraw accepts lists of aecSpaces or an
aecSpaceGroup instance to render in pythonOCC.
"""

class aecSpaceDrawOCC:
 
   
   
    def __init__(self):
        """
        aecSpaceDrawOCC Constructor
        Creates a new aecErrorCheck object.
        """
        pass

    def getType(self):
        """
        string getType()
        Returns a string constant to identify the object type.
        Returns None on failure.
        """
        try:
            return self.__type
        except Exception:
            traceback.print_exc()
            return None

    def makeEdges(self, pointPairs):
        """
        [Topo_DS_Edge,] makeEdges([[gp_Pnt, gp_Pnt],])
        Returns a list of Topo_DS_Edges derived from a list of gp_Pnt pairs.
        Returns None on failure.
        """
        try:
            edges = []
            for pair in pointPairs:
                newEdge = BRepBuilderAPI_MakeEdge(pair[0], pair[1])
                edges.append(newEdge.Edge())
            return edges
        except Exception:
            traceback.print_exc()
            return None
    
    def makePointPairs(self, points):
        """
        [[gp_Pnt, gp_Pnt],] makePointPairs([gp_Pnt,])
        Returns a list of point pairs derived from a list of gp_Pnt points.
        Returns None on failure.
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
        except Exception:
            traceback.print_exc()
            return None
    
    def makePoints(self, space):
        """
        [gp_Pnt,] makePoints(aecSpace)
        Returns a list of gp_Pnts compatible with pythonOCC
        derived from the delivered aecSpace object.
        Returns None on failure.
        """
        try:
            points = space.points_floor
            if not points: return None
            return [gp_Pnt(pnt.x, pnt.y, pnt.z) for pnt in points]
        except Exception:
            traceback.print_exc()
            return None
    
    def makeWire(self, edges):
        """
        Topo_DS_Wire makeWire([Topo_DS_Edge, Topo_DS_Edge,...])
        Returns a pythonOCC Wire object constructed
        from the delivered list of Topo_DS_Edges.
        Returns None on failure.
        """
        try:
            wire = BRepBuilderAPI_MakeWire(edges[0])
            del edges[0] 
            for edge in edges:
                wire.Add(edge)
            return wire
        except Exception:
            traceback.print_exc()
            return None
    
    def draw3D(self, spaces, displaySize = (1024, 768), update = False):
        """
        draw3D(aecSpaceGroup)
        Accepts an aecSpaceGroup object and renders its list of aecSpaces to the pythonOCC display.
        Returns True on success failure.
        Returns False on failure.
        """
        try:
            if not spaces: return False
            if type(spaces) != list: spaces = spaces.spaces
            if not spaces: return False
            __display, __start_display, __add_menu, __add_function_to_menu = init_display(size = displaySize)            
            for space in spaces:
                points = self.makePoints(space)
                if not points: continue
                pointPairs = self.makePointPairs(points)
                if not pointPairs: continue
                edges = self.makeEdges(pointPairs)
                if not edges: continue
                wire = self.makeWire(edges)
                if not wire: continue
                face = BRepBuilderAPI_MakeFace(wire.Wire())
                if not face: continue
                vector = gp_Vec(0, 0, space.height)
                spaceVolume = BRepPrimAPI_MakePrism(face.Face(), vector).Shape()
                if not spaceVolume: continue
                displayColor = space.color.color_01
                spaceColor = OCC.Quantity.Quantity_Color_Name(
                    displayColor[0],
                    displayColor[1],
                    displayColor[2])
                __display.DisplayShape(
                        spaceVolume, 
                        color = spaceColor,
                        transparency = space.color.alpha_01,
                        update = update)
            __display.FitAll()
            __start_display()
            __display = None
            return True
        except Exception:
            traceback.print_exc()
            return False

# end class

