import math
import numpy
import traceback
import uuid

from sympy import geometry as symGeometry

from aecErrorCheck import aecErrorCheck
from aecGeomCalc import aecGeomCalc

class aecVertex:
    """
    class aecVertex
    Defines a 3D vertex as a component of the boundary of an aecSpace,
    with additional information for geometric and graphic calculations.
    The XY plane is considered horizontal, the Z dimension vertical.
    """
    
    def __init__(self, points, index, nrmPoint):
        """
        aecPoint Constructor
        Sets the ID to a new UUID.
        Creates a new aecErrorCheck object.
        if point coordinates are delivered, checks and uses them,
        otherwise sets the coordinates to the origin.
        """
        self.__identifier = uuid.uuid4()
        self.__aecErrorCheck = aecErrorCheck()
        self.__aecGeomCalc = aecGeomCalc()
        # __angleExterior is the angle in radians of the horizontal vectors 
        # at the exterior point of the polygon from which the vertex is derived.
        self.__angleExterior = None  
        # __angleInterior is the angle in radians of the horizontal vectors 
        # at the interior point of the polygon from which the vertex is derived.
        self.__angleInterior = None
        self.__normal = None # __normal is the normal vector of the vertex 
        self.__point = None # __point contains the x,y,z coordinates as a 3 digit tuple
        self.setVertex(points, index, nrmPoint)
                 
    def getAngle(self, exterior = False, degrees = False):
        """
        float getAngleInterior(bool, bool)
        Returns the value of the polygon's interior or exterior angle 
        at the vertex in radians by default or degrees if degrees = True.
        """
        try:
            if exterior:
                angle = self.__angleExterior
            else:
                angle = self.__angleInterior
            if degrees:
                return angle * (180 / math.pi)
            return angle
        except:
            traceback.print_exc() 
    
    def getID(self):
        """
        string getID()
        Returns the UUID.
        """
        try:           
            return str(self.__id)
        except:
            traceback.print_exc() 
            
    def getNormal(self):
        """
        (3D vector) getNormal()
        Returns the point normal of the vertex.
        """
        try:           
            return self.__normal
        except:
            traceback.print_exc()       
    
    def getPoint(self):
        """
        (3D point) getCoordinates()
        Returns the coordinates of the vertex as a 3D point.
        """
        try:
            return self.__point
        except:
            traceback.print_exc()        
               
    def __setNormal(self, point, prvPoint, nxtPoint, nrmPoint):
        """
        INTERNAL
        bool __setNormal((3D point), (3D point), (3D point), (3D point))
        Sets a point normal calculated from the delivered list
        of points asserted to be adjacent on a 3D polyhedron.
        """
        try:
            point = numpy.array(point)
            prvPoint = numpy.array(prvPoint)
            nxtPoint = numpy.array(nxtPoint)
            nrmPoint = numpy.array(nrmPoint)
            prvVector = prvPoint - point
            nxtVector = nxtPoint - point
            nrmVector = nrmPoint - point
            normal = prvVector + nxtVector + nrmVector
            if self.__angleInterior <= self.__angleExterior:
                normal *= -1
            normal = list(normal)   
            self.__normal = tuple([1 if n > 0 else -1 if n < 0 else 0 for n in normal])
            return True
        except:
            traceback.print_exc()    
 
    def setVertex(self, points, index, nrmPoint):
        """
        bool setVertex((3D point),], int, (3D point))
        Sets the vertex 3D point, angle, and point normal.
        """
        try:
            points = list(map(self.__aecErrorCheck.checkPoint, points))
            point = points[index]
            polygon = symGeometry.Polygon(*list(map(lambda x: symGeometry.Point(x[0], x[1]), points)))
            polyAngles = polygon.angles
            angles = {}
            for key in polyAngles:
                angles[(key.x, key.y)] = polyAngles[key].evalf()
            prvPoint = points[(index - 1) % len(points)]
            nxtPoint = points[(index + 1) % len(points)]
            self.__angleInterior = angles[point[:-1]]
            self.__angleExterior = (math.pi * 2) - self.__angleInterior
            self.__setNormal(point, prvPoint, nxtPoint, nrmPoint)
            self.__point = point
            return True
        except:
            traceback.print_exc() 

# end class
