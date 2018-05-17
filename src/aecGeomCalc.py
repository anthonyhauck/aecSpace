import math
import numpy
import random
import traceback

from scipy.spatial import Delaunay
from shapely import geometry as shapely
from shapely import ops as shapeOps
from sympy import Point, Polygon

from aecCompass import aecCompass
from aecErrorCheck import aecErrorCheck

class aecGeomCalc:
    
    # utility objects and data shared by all instances.

    __aecErrorCheck = aecErrorCheck() # An instance of aecErrorCheck  
    __type = 'aecGeomCalc'            # Type identifier of object instances    
    
    def __init__(self):
        """
        aecGeomCalc Constructor
        """
        pass 
                
    def areColinear(self, points):
        """
        bool areColinear([(2D point),])
        Returns True if all delivered points are colinear.
        Returns False if points are not colinear.
        Returns None on failure to make a determination.
        """
        try:
            if type(points) != list or len(points) < 3:
                return None
            points = list(map(lambda pnt: self.__aecErrorCheck.checkPoint(pnt, point2D = True), points))
            if not points: return None
            if shapely.Polygon(points).area > 0: return False
            return True    
        except Exception:
            traceback.print_exc()
            return None

    def checkBoundingBox(self, boundingbox, box2D = False):
        """
        [(3D point), (3D point), (3D point), (3D point),] checkBoundingBox([(3Dpoint),])
        Attempts to return a list of 3D points describing a bounding box.
        Returns None on failure.
        """
        try:
            if type(boundingbox) != list: return None
            if len(boundingbox) < 2: return None
            if len(boundingbox) < 4:
                point = self.__aecErrorCheck.checkPoint(boundingbox[0], box2D)
                vector = self.__aecErrorCheck.checkPoint(boundingbox[1], box2D)
                if not point or not vector: return None
                return self.getBoxPoints(point, vector, box2D)
            boundingbox = boundingbox[:4]
            boundingbox = [self.__aecErrorCheck.checkPoint(x, box2D) for x in boundingbox]
            if None in boundingbox: return None
            return boundingbox
        except Exception:
            traceback.print_exc()
            return None        

    def checkPolygon(self, points):
        """
        [(2D point),] checkPolygon([(2D or 3D point),], bool)
        Returns a list of 2D points that seem capable of defining a polygonal perimeter.
        Returns False if a condition precluding a polygon is detected.
        Returns None on failure to make a determination.
        """
        try:
            if type(points) != list or len(points) < 3: return None
            points = list(map(lambda pnt: self.__aecErrorCheck.checkPoint(pnt, point2D = True), points))
            if self.areColinear(points): return None
            return points
        except Exception:
            traceback.print_exc()
            return None
    
    def containsPoint(self, boundary, point):
        """
        bool containsPoint([(2D point),], (2D Point))
        Returns True if the boundary contains the point on the shared zero plane.
        The boundary argument is assumed to be a sequential 2D point list on a perimeter.
        Returns None if the boundary and point cannot be compared.
        """
        try:
            boundary = self.checkPolygon(boundary)
            point = self.__aecErrorCheck.checkPoint(point)
            if not (boundary and point): return None
            boundary = shapely.polygon.orient(shapely.Polygon(boundary))
            point = shapely.Point(point[0], point[1])
            return boundary.contains(point)
        except Exception:
            traceback.print_exc()
            return None

    def containsShape(self, boundary, shape):
        """
        bool containsShape([(2D point),], [(2D point),])
        Returns True if the boundary wholly contains the shape on the shared zero plane.
        Both arguments are 2D point lists assumed to be sequential on two perimeters. 
        Returns None if the boundary and shape cannot be compared.
        """
        try:
            boundary = self.checkPolygon(boundary)
            shape = self.checkPolygon(shape)
            if not (boundary and shape): return None
            boundary = shapely.polygon.orient(shapely.Polygon(boundary))
            shape = shapely.polygon.orient(shapely.Polygon(shape))
            return boundary.contains(shape)
        except Exception:
            traceback.print_exc()
            return None

    def convexHull(self, points):
        """
        ([(3D point),]) convexHull ([(3D point),])
        Computes the convex hull of a set of 2D points returning the list
        of outermost points in counter-clockwise order, starting from the
        vertex with the lexicographically smallest coordinates.
        Returns None on failure.
        """
        try:
            if len(points) <= 2:
                return points
            points = list(map(lambda x:
                              (float("{:.8f}".format(x[0])),
                               float("{:.8f}".format(x[1]))),
                               points)
                         )
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
                while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
                    lower.pop()
                lower.append(p)

            # Build upper hull
            upper = []
            for p in reversed(points):
                while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
                    upper.pop()
                upper.append(p)

            # Concatenation of the lower and upper hulls gives the convex hull.
            # Last point of each list is omitted because it is repeated at the
            # beginning of the other list.

            return lower[:-1] + upper[:-1]
        
        except Exception:
            traceback.print_exc()
            return None
    
    def findPoint(self, boundary):
        """
        (2D point) findPoint([(2D or 3D point),])
        Returns a random point within the boundary defined by the list of delivered points.
        Returns None if no point can be found or on failure.
        """
        try:
            if not self.checkPolygon(boundary): return None
            boundary = shapely.polygon.orient(shapely.Polygon(boundary))           
            bounds = boundary.bounds
            box = \
            [
                (bounds[0], bounds[1]),
                (bounds[2], bounds[1]),
                (bounds[2], bounds[3]),
                (bounds[0], bounds[3])
            ]
            xBounds = [x[0] for x in box]
            xBounds.sort()
            xBounds = [int(xBounds[0]), int(xBounds[-1])]
            yBounds = [y[1] for y in box]
            yBounds.sort()
            yBounds = [int(yBounds[0]), int(yBounds[-1])]
            xCoord = random.randint(xBounds[0], xBounds[1])
            yCoord = random.randint(yBounds[0], yBounds[1])
            tstPoint = shapely.Point((xCoord, yCoord))
            while not boundary.contains(tstPoint):
                xCoord = random.randint(xBounds[0], xBounds[1])
                yCoord = random.randint(yBounds[0], yBounds[1])
                tstPoint = shapely.Point((xCoord, yCoord))               
            return (tstPoint.x, tstPoint.y)
        except Exception:
            traceback.print_exc()
            return None
        
    def getBoxPoints(self, origin = (0, 0, 0), vector = (1, 1, 1), box2D = False):
        """
        [(3D point),] getBoxPoints((2D or 3D point), (2D or 3D vector), bool)
        Returns the 2D or 3D coordinates of a box based on the origin and vector.
        Returns None on failure.
        """
        try:
            origin = self.__aecErrorCheck.checkPoint(origin, box2D)
            vector = self.__aecErrorCheck.checkPoint(vector, box2D)
            if not (origin and vector): return None
            xDelta = origin[0] + vector[0]
            yDelta = origin[1] + vector[1]
            boxPoints = \
            [
                (origin[0], origin[1]),
                (xDelta, origin[1]),
                (xDelta, yDelta),
                (origin[0], yDelta)
            ]  
            if box2D: return boxPoints
            return [(pnt[0], pnt[1], origin[2]) for pnt in boxPoints]
        except Exception:
            traceback.print_exc() 
            return None

    def getCompassPointBox(self, boundingbox, box2D = False, orient = aecCompass.C):
        """
        (3D point) getCompassPoint([(3D point),] aecCompass.constant)
        Returns a point on the delivered bounding box corresponding to the orientation of one 
        of 17 compass directions defined by aecCompass, including the default C denoting the center.
        For example, N (north) corresponds to the middle point of maximum y side of the bounding box,
        with proportionate distances along the axis represented by NNE (3/4 length from minumum X),
        and NE (bounding box maximum x, maximum y corner).
        Returns None on failure.
        """
        try:
            if type(orient) != int: return None
            if orient < aecCompass.C or orient > aecCompass.NNW: return None
            boundingbox = self.checkBoundingBox(boundingbox, box2D)
            if not boundingbox: return None
            north = self.getMidpoint(boundingbox[3], boundingbox[2])
            west = self.getMidpoint(boundingbox[0], boundingbox[3])
            south = self.getMidpoint(boundingbox[0], boundingbox[1])
            east = self.getMidpoint(boundingbox[1], boundingbox[2])
            if orient == aecCompass.C: return self.getMidpoint(boundingbox[0], boundingbox[2])
            if orient == aecCompass.N: return north
            if orient == aecCompass.W: return west
            if orient == aecCompass.S: return south
            if orient == aecCompass.E: return east
            if orient == aecCompass.SW: return boundingbox[0]
            if orient == aecCompass.SE: return boundingbox[1]
            if orient == aecCompass.NE: return boundingbox[2]
            if orient == aecCompass.NW: return boundingbox[3]
            if orient == aecCompass.NNW: return self.getMidpoint(north, boundingbox[3])
            if orient == aecCompass.WNW: return self.getMidpoint(west, boundingbox[3])
            if orient == aecCompass.WSW: return self.getMidpoint(west, boundingbox[0])
            if orient == aecCompass.SSW: return self.getMidpoint(boundingbox[0], south)
            if orient == aecCompass.SSE: return self.getMidpoint(south, boundingbox[1])
            if orient == aecCompass.ESE: return self.getMidpoint(east, boundingbox[1])
            if orient == aecCompass.ENE: return self.getMidpoint(east, boundingbox[2])
            if orient == aecCompass.NNE: return self.getMidpoint(north, boundingbox[2])
            return None
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
            boundary = self.checkPolygon(boundary)
            shape = self.checkPolygon(shape)
            if not (boundary and shape): return None
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

    def getIntersection(self, boundary, shape):
        """
        [(2D point),] getIntersection([(2D point),], [(2D point),])
        Returns the points of a perimeter representing the 
        geometric intersection of the boundary and the shape.
        Returns None if unable to determine a single intersection perimeter.
        """
        try:
            boundary = self.checkPolygon(boundary)
            shape = self.checkPolygon(shape)
            if not (boundary and shape): return None
            boundary = shapely.polygon.orient(shapely.Polygon(boundary))
            shape = shapely.polygon.orient(shapely.Polygon(shape))
            intersect = boundary.intersection(shape)
            if intersect.type == 'MultiPolygon':
                intersect = shapeOps.unary_union(intersect)
            if type(intersect) != shapely.polygon.Polygon: return None
            return intersect.exterior.coords[:-1]
        except Exception:
            traceback.print_exc() 
            return None        
    
    def getMesh2D(self, points):
        """
        [[(3 indices),][(3D point),],] getMesh2D()
        Constructs a compact 2D mesh representation of a horizontal 
        surface as a list of unique points and triangle indices.
        Returns None on failure.
        """
        try:
            mesh = Delaunay(points)
            triangles = mesh.simplices
            points = list(map(lambda x: tuple([x[0], x[1]]), mesh.points))
            analytic = Polygon(*list(map(Point, points)))
            if analytic.is_convex():
                indices = list(map(lambda x: tuple([int(x[0]), int(x[1]), int(x[2])]), triangles))
                return [points, indices]
            boundary = shapely.Polygon(points)
            indices = []
            for triangle in triangles:
                test = shapely.Polygon([points[triangle[0]], 
                                         points[triangle[1]],
                                         points[triangle[2]]])
                point = test.representative_point()
                if boundary.contains(point):
                    indices.append(list(map(int, triangle)))         
            return [points, indices]
        except Exception:
            traceback.print_exc()
            return None

    def getMidpoint(self, point1, point2):
        """
        (2D or 3D point) getMidpoint((2D or 3D point), (2D or 3D point))
        Returns the midpoint between two 3D points.
        Returns None on failure
        """
        try:
            point1 = self.__aecErrorCheck.checkPoint(point1)
            point2 = self.__aecErrorCheck.checkPoint(point2)
            if not point1 or not point2: return None
            xCoord = (point1[0] + point2[0]) * 0.5
            yCoord = (point1[1] + point2[1]) * 0.5
            if len(point1) > 2 and len(point2) > 2:
                zCoord = (point1[2] + point2[2]) * 0.5
                return (xCoord, yCoord, zCoord)
            return (xCoord, yCoord)
        except Exception:
            traceback.print_exc()
            return None
        
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
    
    def mirrorPoints2D (self, points, mPoints = [(0, 0), (0, 1)]):
        """
        [(2D point),] mirrorPoints2D([(2D point),], [(2D point), (2D point)])
        Accepts a set of points and a mirror axis defined by two 2D points
        and returns a set of points reflected around the mirror axis.
        Returns None on failure.
        """
        try:
            mPnt1 = self.__aecErrorCheck.checkPoint(mPoints[0], point2D = True)
            mPnt2 = self.__aecErrorCheck.checkPoint(mPoints[1], point2D = True)
            newPoints = []
            if mPnt1[0] == mPnt2[0]: # vertical mirror
                for point in points:
                    point = list(point)
                    distance = abs(point[0] - mPnt1[0]) * 2
                    if point[0] < mPnt1[0]:
                        point[0] += distance
                    else:
                        point[0] -= distance
                    newPoints.append(tuple(point))
                return newPoints
            if mPnt1[1] == mPnt2[1]: # horizontal mirror
                for point in points:
                    point = list(point)          
                    distance = abs(point[1] - mPnt1[1]) * 2                          
                    if point[1] < mPnt1[1]:
                        point[1] += distance
                    else:
                        point[1] -= distance
                    newPoints.append(tuple(point))
                return newPoints           
            mSlope = (mPnt2[1] - mPnt1[1]) / (mPnt2[0] - mPnt1[0])
            rSlope = (-1 / mSlope)
            dSlope = (mSlope - rSlope)
            mYint = ((mSlope * mPnt1[0]) - mPnt1[1]) * -1
            for point in points:                
                rYint = ((rSlope * point[0]) - point[1]) * -1
                xCoord = (rYint - mYint) / dSlope
                yCoord = ((mSlope * rYint) - (rSlope * mYint)) / dSlope
                xDist = abs(point[0] - xCoord)
                yDist = abs(point[1] - yCoord)
                rLength = math.sqrt(xDist + yDist) * 2
                point = numpy.array(list(point))
                mPoint = numpy.array([xCoord, yCoord])
                newPoint = (rLength * (mPoint - point)) + point
                newPoints.append(tuple(newPoint))
            return newPoints
        except Exception:
            traceback.print_exc()
            return None

    def rmvColinear(self, points):
        """
        [(3D point),] rmvColinear([(3D point),])
        Returns the delivered list of points with redundundant colinear points removed.
        Returns None on failure.
        """
        try:
            points = list(map(lambda pnt: self.__aecErrorCheck.checkPoint(pnt, point2D = True), points))
            if not points: return None
            points = (sorted(set(points), key = points.index))
            points += points
            for x in range(0, 3):
                coPoints = points[x:x + 3]
                while len(coPoints) == 3:
                    if self.areColinear(coPoints):
                        points.remove(coPoints[1])
                    coPoints = points[x:x + 3]
                    x += 1
            return (sorted(set(points), key = points.index))
        except Exception:
            traceback.print_exc()
            return None
           
# end class