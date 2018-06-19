import math
import numpy
import traceback

from matplotlib.tri import Triangulation
from shapely import geometry as shapely
from shapely import ops as shapeOps
from typing import List, NamedTuple, Tuple

from .aecPoint import aecPoint

class aecGeometry:
    
    # Defines a series of constants indicating cardinal directions.
    
    N, NNE, NE, ENE, E, ESE, SE, SSE, S, SSW, SW, WSW, W, WNW, NW, NNW = range(0, 16)
       
    # Defines a data structure of eight points with locations indicated 
    # by compass point abbreviations in counterclockwise order for the 
    # (l)ower and (U)pper boundaries.
    
    cube = \
        NamedTuple(
        'cube',
        [
            ('SWL', aecPoint), 
            ('SEL', aecPoint), 
            ('NEL', aecPoint),
            ('NWL', aecPoint),                        
            ('SWU', aecPoint), 
            ('SEU', aecPoint), 
            ('NEU', aecPoint),
            ('NWU', aecPoint)
        ])
    
    # Defines a mesh data structure listing
    # vertices and triangle indices.
    
    mesh2D = \
        NamedTuple(
        'mesh2D', 
        [
            ('vertices', List[Tuple[float, float, float]]),
            ('indices', List[Tuple[float, float, float]]),            
        ])
    
    # Defines a mesh data structure listing
    # vertices, triangle indices, and point normals.  
    
    mesh3D = \
        NamedTuple(
        'mesh3D', 
        [
            ('vertices', List[Tuple[float, float, float]]),
            ('indices', List[Tuple[float, float, float]]), 
            ('normals', List[Tuple[float, float, float]])           
        ])
    
    # Defines a mesh data structure listing vertices, triangle indices,
    # and point normals as sequences of floats.  
    
    mesh3Dgraphic = \
        NamedTuple(
        'mesh3Dgraphic', 
        [
            ('vertices', List[float]),
            ('indices', List[float]), 
            ('normals', List[float])           
        ])    
    
    # Defines a redundant mesh data structure listing
    # vertices, triangle indices, and surface normals
    # for each point.
    
    meshGraphic = \
        NamedTuple(
        'meshGraphic', 
        [
            ('vertices', List[float]),
            ('indices', List[float]), 
            ('normals', List[float])           
        ])
    
    # Defines a data structure of four points with locations indicated
    # by compass point abbreviations in counterclockwise order with an
    # associated normal.
    
    quad_points = \
        NamedTuple(
        'quad_points',
        [
            ('ID', int),
            ('SW', aecPoint), 
            ('SE', aecPoint), 
            ('NE', aecPoint),
            ('NW', aecPoint),
            ('normal', Tuple[float, float, float])
        ])    
    
    # Defines an angle data structure listing
    # the interior, exterior and convexity of
    # a polygon vertex.   
    
    vertexAngle = \
        NamedTuple(
        'aecVertexAngle',
        [
            ('interior', float), 
            ('exterior', float), 
            ('convex', bool)
        ])
    
    def __init__(self):
        """
        Constructor
        """
        pass 
                
    def areColinear(self, points: List[aecPoint]) -> bool:
        """
        Returns True if all delivered points are colinear.
        Returns False if points are not colinear.
        Returns None on failure to make a determination.
        """
        try:
            if len(points) < 3: return True
            points = [pnt.xy for pnt in points]
            if shapely.Polygon(points).area > 0: return False
            return True    
        except Exception:
            traceback.print_exc()
            return None
    
    def getAngles(self, vtxPoint: aecPoint, prvPoint: aecPoint, nxtPoint: aecPoint) -> vertexAngle:
        """
        Returns whether the delivered point is at a convex or concave angle between
        the previous and following points in a counterclockwise point sequence.
        """
        try:
            inVector = (vtxPoint.x - prvPoint.x, vtxPoint.y - prvPoint.y)
            outVector = (nxtPoint.x - vtxPoint.x, nxtPoint.y - vtxPoint.y)
            angle = self.vertexAngle
            if numpy.cross(inVector, outVector) >= 0: angle.convex = True
            else: angle.convex = False
            cosAngle = numpy.dot(inVector, outVector)
            sinAngle = numpy.linalg.norm(numpy.cross(inVector, outVector))
            vtxAngle = numpy.arctan2(sinAngle, cosAngle)
            if angle.convex: angle.interior = vtxAngle
            else: angle.interior = (math.pi * 2) - vtxAngle
            angle.exterior = (math.pi * 2) - angle.interior
            return angle
        except Exception:
            traceback.print_exc()
            return None

    def getBoxPoints(self, origin: aecPoint, xDelta: float, yDelta: float) -> List[aecPoint]:
        """
        Returns the 3D coordinates of a cube based on diagonally opposite corners.
        Returns None on failure.
        """
        try:
            return \
            [
                aecPoint(origin.x, origin.y),
                aecPoint(origin.x + xDelta, origin.y),
                aecPoint(origin.x + xDelta, origin.y + yDelta),
                aecPoint(origin.x, origin.y + yDelta)
            ]
        except Exception:
            traceback.print_exc() 
            return None

    def getCompassLine(self, box: quad_points, orient: int = 0) -> List[aecPoint]:
        """
        Returns two points describing a line from the center of the
        the delivered bounding box to a compass point on the box.
        """
        try:
            center = self.getMidpoint(box.SW, box.NE)
            compass = self.getCompassPoint(box, orient)
            if center and compass: return [center, compass]
            return None
        except Exception:
            traceback.print_exc()
            return None

    def getCompassPoint(self, box: quad_points, orient: int = 0) -> aecPoint:
        """
        Returns a point on the delivered bounding box corresponding to the 
        orientation of 16 compass direction constants defined by aecGeometry.
        N (north) corresponds to the middle point of maximum y side of the bounding box,
        with proportionate distances along the axis represented by NNE 
        (3/4 length from minumum X), and NE (bounding box maximum x, maximum y corner).
        Returns None on failure.
        """
        try:
            if type(orient) != int: return None
            if orient < self.N or orient > self.NNW: return None
            north = self.getMidpoint(box.NW, box.NE)
            west = self.getMidpoint(box.SW, box.NW)
            south = self.getMidpoint(box.SW, box.SE)
            east = self.getMidpoint(box.SE, box.NE)
            if orient == self.N: return north
            if orient == self.W: return west
            if orient == self.S: return south
            if orient == self.E: return east
            if orient == self.SW: return box.SW
            if orient == self.SE: return box.SE
            if orient == self.NE: return box.NE
            if orient == self.NW: return box.NW
            if orient == self.NNW: return self.getMidpoint(north, box.NW)
            if orient == self.WNW: return self.getMidpoint(west, box.NW)
            if orient == self.WSW: return self.getMidpoint(west, box.SW)
            if orient == self.SSW: return self.getMidpoint(south, box.SW)
            if orient == self.SSE: return self.getMidpoint(south, box.SE)
            if orient == self.ESE: return self.getMidpoint(east, box.SE)
            if orient == self.ENE: return self.getMidpoint(east, box.NE)
            if orient == self.NNE: return self.getMidpoint(north, box.NE)
            return None
        except Exception:
            traceback.print_exc()
            return None        

    def getConvexHull(self, points: List[aecPoint]) -> List[aecPoint]:
        """
        Computes the convex hull of a set of 2D points returning the list
        of outermost points in anticlockwise order, starting from the
        vertex with the lexicographically smallest coordinates.
        Returns None on failure.
        """
        try:
            if len(points) <= 3: return None
            points = [(float("{:.8f}".format(pnt.x)),             
                       float("{:.8f}".format(pnt.y)))
                       for pnt in points]
            points = sorted(set(points))            
            
            # float cross(float, float, float)
            # Computes the 2D cross product of OA and OB vectors, i.e. z-component
            # of their 3D cross product.
            # Returns a positive value, if OAB makes a counter-clockwise turn, or a
            # negative value for clockwise turn, or zero if the points are collinear.

            def cross(o, a, b):
                return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

            # Build lower hull
            lower = []
            for p in points:
                while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0: lower.pop()
                lower.append(p)

            # Build upper hull
            upper = []
            for p in reversed(points):
                while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0: upper.pop()
                upper.append(p)

            # Concatenation of the lower and upper hulls gives the convex hull.
            # Last point of each list is omitted because it is repeated at the
            # beginning of the other list.

            hull_points = lower[:-1] + upper[:-1]
            return [aecPoint(pnt[0], pnt[1]) for pnt in hull_points]
        except Exception:
            traceback.print_exc()
            return None

    def getDifference(self, boundary, shape):
        """
        [[(2D point),], [(2D point),]]  getDifference([(2D point),], [(2D point),])
        Returns the points of perimeter(s) not shared between boundary and shape.
        If more than one perimeter is found, the return value is a list of lists of points
        defining each perimeter.
        Returns None if unable to determine the difference perimeter(s).
        """
        try:
            boundary = shapely.polygon.orient(shapely.Polygon(boundary))
            shape = shapely.polygon.orient(shapely.Polygon(shape))
            difference = boundary.difference(shape)
            if difference.type == 'MultiPolygon':
                differs = []
                for polygon in list(difference.geoms):
                    differs.append(polygon.exterior.coords[:-1])
                return differs
            return difference.exterior.coords[:-1]
        except Exception:
            traceback.print_exc() 
            return None        

    def getIntersect(self, boundary: List[aecPoint], shape: List[aecPoint]) -> List[aecPoint]:
        """
        Returns the points of a perimeter representing the 
        geometric intersection of the boundary and the shape.
        Returns None if unable to determine a single intersection perimeter.
        """
        try:
            bnd_pnts = [pnt.xy for pnt in boundary]
            shp_pnts = [pnt.xy for pnt in shape]
            bnd = shapely.polygon.orient(shapely.Polygon(bnd_pnts))
            shp = shapely.polygon.orient(shapely.Polygon(shp_pnts))
            intersect = bnd.intersection(shp)
            if intersect.type == 'MultiPolygon': intersect = shapeOps.unary_union(intersect)
            if type(intersect) != shapely.polygon.Polygon: return None
            return [aecPoint(pnt[0], pnt[1]) for pnt in intersect.exterior.coords[:-1]]
        except Exception:
            traceback.print_exc() 
            return None        
    
    def getMesh2D(self, points: List[aecPoint]) -> mesh2D:
        """
        Constructs a compact 2D mesh representation of a horizontal 
        surface as a list of unique points and triangle indices.
        Returns None on failure.
        """
        try:
            bndPoints= [point.xyz for point in points]
            boundary = shapely.polygon.orient(shapely.Polygon(bndPoints))
            xPoints = [point.x for point in points]
            yPoints = [point.y for point in points]
            meshD = Triangulation(xPoints, yPoints)
            triangles = meshD.triangles
            indices = []
            for item in triangles:
                triPoints = \
                [
                    points[item[0]].xyz, 
                    points[item[1]].xyz, 
                    points[item[2]].xyz,
                ]
                triangle = shapely.polygon.orient(shapely.Polygon(triPoints))
                tstPoint = triangle.representative_point()
                if boundary.contains(tstPoint): 
                    indices.append(tuple([int(element) for element in list(item)]))
            mesh = self.mesh2D
            mesh.vertices = [pnt.xyz for pnt in points]
            mesh.indices = indices
            return mesh
        except Exception:
            traceback.print_exc()
            return None

    def getMidpoint(self, point1: aecPoint, point2: aecPoint) -> aecPoint:
        """
        Returns the midpoint between two 3D points.
        Returns None on failure.
        """
        try:
            xCoord = (point1.x + point2.x) * 0.5
            yCoord = (point1.y + point2.y) * 0.5
            zCoord = (point1.z + point2.z) * 0.5
            return aecPoint(xCoord, yCoord, zCoord)
        except Exception:
            traceback.print_exc()
            return None              
    
    def getNormal(self, point: aecPoint, prePoint: aecPoint, nxtPoint: aecPoint) -> Tuple[float, float, float]:
        """
        Returns the normal from three points.
        """
        try:
            preVector = prePoint.xyz_array - point.xyz_array
            nxtVector = nxtPoint.xyz_array - point.xyz_array
            preNormal = numpy.cross(preVector, nxtVector)
            normal = preNormal / (math.sqrt(sum(preNormal**2)))
            return tuple(normal)
        except Exception:
            traceback.print_exc()
            return None

    def isConvex(self, points: List[aecPoint]) -> bool:
        """
        Determines from a set of counterclockwise points 
        whether the implied polygon is convex.
        Returns None on failure.
        """
        try:
            index = 0
            length = len(points)
            while index < length:
                angles = self.getAngles(points[index], 
                                        points[(index - 1) % length], 
                                        points[(index + 1) % length])
                if not angles.convex: return False
                index += 1
            return True
        except Exception:
            traceback.print_exc()
            return None          
        
    
    def mirrorPoints2D (self, points: List[aecPoint], mPoint1: aecPoint, mPoint2: aecPoint):
        """
        [(2D point),] mirrorPoints2D([(2D point),], [(2D point), (2D point)])
        Accepts a set of points and a mirror axis defined by two 2D points
        and returns a set of points reflected around the mirror axis.
        Returns None on failure.
        """
        try:
            newPoints = []
            if mPoint1.x == mPoint2.x: # vertical mirror
                for point in points:
                    distance = abs(point.x - mPoint1.x) * 2
                    if point.x < mPoint1.x: point.x += distance
                    else: point.x -= distance
                    newPoints.append(point)
                return newPoints
            if mPoint1.y == mPoint2.y: # horizontal mirror
                for point in points:
                    distance = abs(point.y - mPoint1.y) * 2                          
                    if point.y < mPoint1.y: point.y += distance
                    else: point.y -= distance
                    newPoints.append(point)
                return newPoints  
            mSlope = (mPoint2.y - mPoint1.y) / (mPoint2.x - mPoint1.x)
            rSlope = (-1 / mSlope)
            dSlope = (mSlope - rSlope)
            mYint = ((mSlope * mPoint1.x) - mPoint1.x) * -1
            for point in points:                
                rYint = ((rSlope * point.x) - point.y) * -1
                xCoord = (rYint - mYint) / dSlope
                yCoord = ((mSlope * rYint) - (rSlope * mYint)) / dSlope
                xDist = abs(point.x - xCoord)
                yDist = abs(point.y - yCoord)
                rLength = math.sqrt(xDist + yDist) * 2
                nPoint = point.xy_array
                mPoint = numpy.array([xCoord, yCoord])
                newPoint = (rLength * (mPoint - nPoint)) + nPoint
                point.x = newPoint[0]
                point.y = newPoint[1]
                newPoints.append(point)
            return newPoints
        except Exception:
            traceback.print_exc()
            return None

    def rmvColinear(self, points: List[aecPoint]) -> List[aecPoint]:
        """
        Returns the delivered list of points with redundundant colinear points removed.
        Returns None on failure.
        """
        try:
            level = points[0].z
            points = [point.xy for point in points]
            points = (sorted(set(points), key = points.index))
            points += points
            for x in range(0, 3):
                coPoints = points[x:x + 3]
                while len(coPoints) == 3:
                    if shapely.Polygon(coPoints).area == 0: points.remove(coPoints[1])
                    coPoints = points[x:x + 3]
                    x += 1
            points = (sorted(set(points), key = points.index))
            return [aecPoint(pnt[0], pnt[1], level) for pnt in points]
        except Exception:
            traceback.print_exc()
            return None
           
# end class