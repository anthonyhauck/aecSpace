import traceback

from math import cos, sin, pi
from shapely import geometry as shapely
from shapely import ops as shapelyOps
from typing import List

from aecSpace.aecGeometry import aecGeometry
from aecSpace.aecPoint import aecPoint
from aecSpace.aecValid import aecValid

class aecShaper():
    """
    Provides functions for a limited vocabulary of plan shapes.
    """
         
    __aecGeometry = aecGeometry()
    __aecValid = aecValid()
    
    def __init__(self, x:float = 0, y:float = 0, z:float = 0):
        """
        Constructor defaults to origin point coordinates.
        """
        pass
   
    def __add(self, pointSet: List[List[aecPoint]]) -> bool:
        """
        Returns False if the delivered points do not resolve to a single non-crossing
        polygon and leaves the current boundary unchanged.
        Returns True if successful.
        """
        try:
            boundaries = []
            for points in pointSet:
                polygon = shapely.polygon.orient(shapely.Polygon([point.xy for point in points]))
                if type(polygon) != shapely.polygon.Polygon: raise Exception
                boundaries.append(polygon)
            boundary = shapelyOps.unary_union(shapely.MultiPolygon(boundaries))
            if type(boundary) != shapely.polygon.Polygon: return False
            return [aecPoint(pnt[0], pnt[1]) for pnt in list(boundary.exterior.coords)[:-1]]                
        except Exception:
            traceback.print_exc()
            return False
      
    def makeBox(self, origin: aecPoint = aecPoint(), 
                      xSize: float = 1.0, 
                      ySize: float = 1.0) -> bool:
        """
        Creates a rectangular boundary from two diagonal points.
        """
        try:
            return [aecPoint(origin.x, origin.y),
                    aecPoint(origin.x + xSize, origin.y),
                    aecPoint(origin.x + xSize, origin.y + ySize),
                    aecPoint(origin.x, origin.y + ySize)]
        except Exception:
            traceback.print_exc()
            return False    

    def makeCross(self, origin: aecPoint = aecPoint(0, 0, 0), 
                        xSize: float = 1, 
                        ySize: float = 1,
                        xWidth = None, 
                        yDepth = None,
                        xAxis: float = 0.5, 
                        yAxis: float = 0.5) -> bool:
        """
        Constructs a cross-shaped boundary within the box defined by the origin and xy deltas.
        xWidth and yDepth define the widths of the two arms.
        xAxis and yAxis are percentages of overall x-axis and y-axis distances that
        determine the centerline of each cross arm.
        Returns None on failure.
        """
        try:
            if not xWidth: xWidth = xSize * 0.5
            if not yDepth: yDepth = ySize * 0.5
            xPnt = aecPoint(origin.x + ((yAxis * xSize) - (xWidth * 0.5)), origin.y)
            yPnt = aecPoint(origin.x, origin.y + ((xAxis * ySize) - (yDepth * 0.5)))
            armX = self.makeBox(xPnt, xWidth, ySize)
            armY = self.makeBox(yPnt, xSize, yDepth)
            return self.__add([armX, armY])
        except Exception:
            traceback.print_exc()
            return None

    def makeCylinder(self, origin: aecPoint = aecPoint(), 
                           radius = 1) -> bool:
        """
        Contructs the perimeter as an approximate circle, setting 
        a ratio from the delivered radius to the number of sides.
        Returns True on success.
        Returns False on failure.
        """
        try:
            if radius < 3: sides = 3
            else: sides = radius
            return self.makePolygon(origin, radius, sides)
        except Exception:
            traceback.print_exc()
            return False

    def makeH(self, origin: aecPoint = aecPoint(),
                    xSize: float = 1, 
                    ySize: float = 1,
                    xWidth1 = None, 
                    xWidth2= None, 
                    yDepth = None) -> bool:
        """
        Constructs an H-shaped boundary within the box defined by point and xy deltas.
        xWidth1, xWidth2, and yDepth are percentages of overall x-axis and y-axis distances that
        determine the width of each vertical and cross bar, respectively.
        Returns True on success.
        Returns False on failure.
        """
        try:
            if not xWidth1: xWidth1 = xSize * 0.3
            if not xWidth2: xWidth2 = xSize * 0.3
            if not yDepth: yDepth = ySize * 0.3            
            if xWidth1 >= xSize * 0.5: return None
            if xWidth2 >= xSize * 0.5: return None            
            if yDepth >= ySize: return None             
            arm1 = self.makeBox(origin, xWidth1, ySize)
            oPnt = aecPoint(origin.x + (xSize - xWidth2), origin.y)
            arm2 = self.makeBox(oPnt, xWidth2, ySize)
            oPnt = aecPoint(origin.x, origin.y + ((ySize * 0.5) - (yDepth * 0.5)))
            arm3 = self.makeBox(oPnt, xSize, yDepth)
            return self.__add([arm1, arm2, arm3])
        except Exception:
            traceback.print_exc()
            return False

    def makeL(self, origin: aecPoint = aecPoint(), 
                    xSize: float = 1, 
                    ySize: float = 1,
                    xWidth = None, 
                    yDepth = None) -> bool:
        """
        Constructs a L-shaped boundary within the box defined by point and 
        xy deltas, with distinct values for the width of each arm.
        Returns None on failure.
        """
        try:
            if not xWidth: xWidth = xSize * 0.5
            if not yDepth: yDepth = ySize * 0.5            
            if xWidth >= xSize: return None
            if yDepth >= ySize: return None
            armX = self.makeBox(origin, xWidth, ySize)
            armY = self.makeBox(origin, xSize, yDepth)
            return self.__add([armX, armY])
        except Exception:
            traceback.print_exc()
            return False

    def makePolygon(self, origin: aecPoint = aecPoint(), 
                          radius = 1, sides = 3) -> bool:
        """
        Constructs the boundary as a regular polygon centered on the delivered
        origin point with the first vertex at the maximum y-coordinate.
        Returns True on success.
        Returns False on failure.
        """
        try:
            radius = abs(radius)
            if radius == 0: return False
            sides = int(abs(sides))
            if sides < 3: sides = 3
            angle = pi * 0.5
            incAngle = (pi * 2) / sides
            points = []
            count = 0
            while count < sides:
                x = origin.x + (radius * cos(angle))
                y = origin.y + (radius * sin(angle))
                points.append(aecPoint(x, y))
                angle += incAngle
                count += 1
            return points
        except Exception:
            traceback.print_exc()
            return False
 
    def makeT(self, origin = aecPoint(), 
                    xSize: float = 1, 
                    ySize: float = 1,
                    xWidth = None, 
                    yDepth = None) -> bool:
        """
        Constructs a T-shaped boundary within the box defined by point and xy deltas.
        xWidth and yDepth are percentages of overall x-axis and y-axis distances that
        determine the width of the vertical and horizonatl bars, respectively.
        Returns True on success.
        Returns False on failure.
        """
        try:
            if not xWidth: xWidth = xSize * 0.5
            if not yDepth: yDepth = ySize * 0.5            
            if xWidth >= xSize: return None
            if yDepth >= ySize: return None
            oPnt = aecPoint(origin.x, origin.y + (ySize - yDepth))
            arm1 = self.makeBox(oPnt, xSize, yDepth)
            oPnt = aecPoint(origin.x + ((xSize * 0.5) - (xWidth * 0.5)), origin.y)
            arm2 = self.makeBox(oPnt, xWidth, ySize)
            return self.__add([arm1, arm2])
        except Exception:
            traceback.print_exc()
            return False
        
    def makeU(self, origin = aecPoint(),
                    xSize: float = 1,
                    ySize: float = 1,
                    xWidth1 = None, 
                    xWidth2= None, 
                    yDepth = None):
        """
        Constructs a U-shaped boundary within the box defined by point and xy deltas.
        xWidth1, xWidth2, and yDepth are percentages of overall x-axis and y-axis distances
        that determine the width of each vertical and cross bar, respectively.
        Returns True on success.
        Returns False on failure.
        """
        try:
            if not xWidth1: xWidth1 = xSize * 0.3
            if not xWidth2: xWidth2 = xSize * 0.3
            if not yDepth: yDepth = ySize * 0.3            
            if xWidth1 >= xSize * 0.5: return None
            if xWidth2 >= xSize * 0.5: return None            
            if yDepth >= ySize: return None            
            pointsL = self.makeL(origin, xSize, ySize, xWidth1, yDepth)
            xPoint = aecPoint(origin.x + (xSize - xWidth2), origin.y)
            pointsU = self.makeBox(xPoint, xWidth2, ySize)
            return self.__add([pointsL, pointsU])
        except Exception:
            traceback.print_exc()
            return False