import math
import numpy
import traceback

from scipy.spatial import Delaunay
from shapely import geometry as shape
from sympy import Point, Polygon


from aecErrorCheck import aecErrorCheck

class aecGeomCalc:
    
    def __init__(self):
        """
        aecGeomCalc Constructor
        Creates a new aecErrorCheck instance.
        """
        self.__aecErrorCheck = aecErrorCheck()    
        
    def areColinear(self, points):
        """
        bool areColinear([(2D point),])
        Returns True if all delivered points are colinear.
        """
        try:
            if shape.Polygon(points).area > 0:
                return False
            return True    
        except:
            traceback.print_exc() 
            
    def rmvColinear(self, points):
        """
        [(3D point),] rmvColinear([(3D point),])
        Returns the delivered list of points with redundundant colinear points removed.
        """
        try:
            points = (sorted(set(points), key = points.index))
            points = [point[:-1] if len(point) == 3 else point for point in points]
            points += points
            for x in range(0, 3):
                coPoints = points[x:x + 3]
                while len(coPoints) == 3:
                    if self.areColinear(coPoints):
                        points.remove(coPoints[1])
                    coPoints = points[x:x + 3]
                    x += 1
            return (sorted(set(points), key = points.index))
        except:
            traceback.print_exc()         
        
    def getBoxPoints2D(self, origin = (0, 0), vector = (1, 1)):
        """
        [(2D point),] getBoxPoints2D((2D point), (2D vector))
        Returns the 2D coordinates of a box based on the origin and vector.
        """
        try:
            xDelta = origin[0] + vector[0]
            yDelta = origin[1] + vector[1]
            return \
            [
                (origin[0], origin[1]),
                (xDelta, origin[1]),
                (xDelta, yDelta),
                (origin[0], yDelta)
            ]  
        except:
            traceback.print_exc() 

    def getMesh2D(self, points):
        """
        [[(3 indices),][(3D point),],] getMesh2D()
        Constructs a compact 2D mesh representation of a horizontal 
        surface as a list of unique points and triangle indices.
        """
        try:
            mesh = Delaunay(points)
            triangles = mesh.simplices
            points = list(map(lambda x: tuple([x[0], x[1]]), mesh.points))
            analytic = Polygon(*list(map(Point, points)))
            if analytic.is_convex():
                indices = list(map(lambda x: tuple([int(x[0]), int(x[1]), int(x[2])]), triangles))
            else:
                boundary = shape.Polygon(points)
                indices = []
                for triangle in triangles:
                    test = shape.Polygon([points[triangle[0]], 
                                             points[triangle[1]],
                                             points[triangle[2]]])
                    point = test.representative_point()
                    if boundary.contains(point):
                        indices.append(list(map(int, triangle)))         
            return [points, indices]
        except:
            traceback.print_exc() 
      
    def mirrorPoints2D (self, points, mPoints = [(0, 0), (0, 1)]):
        """
        [(2D point),] mirrorPoints2D([(2D point),], [(2D point), (2D point)])
        Accepts a set of points and a mirror axis defined by two points
        and returns a set of points reflected around the mirror axis.
        """
        try:
            mPnt1 = mPoints[0]
            mPnt2 = mPoints[1]
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
        except:
            traceback.print_exc() 
            
# end class