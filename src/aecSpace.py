import math
import random
import traceback
import uuid
import numpy
from sympy import Point, Polygon
from scipy.spatial import Delaunay
from shapely import affinity
from shapely import geometry
from shapely import ops

from aecErrorCheck import aecErrorCheck
from aecGeomCalc import aecGeomCalc

class aecSpace:
    """
    class aecSpace   
    Defines the geometric enclosure of a region described by a list
    of 2D coordinates, a level in relation to the zero plane, and
    a height in relation to the level.
    
    Current Assumptions + Limitations
    
    aecSpaces are prisms with bases parallel to the ground plane
    and having only vertical boundaries.
    
    Curved walls must be represented by a series of straight segments.
    """

    # An instance of aecErrorCheck.
    __aecErrorCheck = None
    
    # __aecGeomCalc is an instance of aecGeometryCalc    
    __aecGeomCalc = None
    
    # __boundary is a 2D polygon representing the boundary.
    __boundary = None

    # __color[R G B] variables designate the RGB color
    # components as integers in the 0 - 255 range.  
    __colorR = 0
    __colorG = 0
    __colorB = 0
        
    # __height is the height of the prism.
    __height = 0

    # __id is a UUID.
    __id = ""
    
    # __level is the position of the perimeter above the zero plane.
    __level = 0
    
    # __name is a custom string designation.
    __name = ""
       
    # __transparency sets the percentage of transparency of the volume
    # for a compatible rendering system as a value from 0 to 1.
    __transparency = 0

    def __init__(self):
        """
        aecSpace Constructor
        Sets the dimensions to a unit cube with a corner at (0, 0, 0).
        Sets the color to random RGB values.
        Sets the ID to a new UUID.
        Creates a new aecErrorCheck object.
        """
        self.makeBox()
        self.setColor()
        self.Identifier = uuid.uuid4()
        self.__aecErrorCheck = aecErrorCheck()
        self.__aecGeomCalc = aecGeomCalc()

    def getArea(self):
        """
        float getArea()
        Returns the area.
        """
        try:           
            return self.__boundary.area
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)
            
    def getAxes2D(self):
        """
        [[[2 floats], [2 floats]], [[2 floats], [2 floats]]] getAxes2D()
        Returns two sets of 2D endpoints of the two axes 
        of the bounding box, X-Axis followed by Y-Axis.
        """
        try:
            box = self.getBoundingBox2D()
            xDisplace = self.getBoxYsize() * 0.5
            yDisplace = self.getBoxXsize() * 0.5
            xPoint1 = (box[0][0], box[0][1] + xDisplace)
            xPoint2 = (box[1][0], box[1][1] + xDisplace)
            yPoint1 = (box[0][0] + yDisplace, box[0][1])
            yPoint2 = (box[3][0] + yDisplace, box[3][1])
            xAxis = [xPoint1, xPoint2]
            yAxis = [yPoint1, yPoint2]
            return [xAxis, yAxis]
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)
            
    def getAxes3D(self):
        """
        [[[3 floats], [3 floats]], [[3 floats], [3 floats]]] getAxes3D()
        Returns two sets of 3D endpoints of the two axes 
        of the bounding box, X-Axis followed by Y-Axis.       
        """
        try:
            level = self.getLevel() + (self.getHeight() * 0.5)
            axes = self.getAxes2D()
            xAxis = list(map(list, (axes[0])))
            yAxis = list(map(list, (axes[1])))
            xAxis[0].append(level)
            xAxis[1].append(level)           
            yAxis[0].append(level)
            yAxis[1].append(level)
            xAxis = list(map(tuple, xAxis))
            yAxis = list(map(tuple, yAxis))
            return [xAxis] + [yAxis]
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)  
            
    def getAxisMajor2D(self):
        """
        [[2 floats], [2 floats]] getAxisMajor2D()
        Returns the 2D endpoints of the major axis of the bounding box.
        If axes are are equal, returns the X-Axis endpoints.
        """
        try:
            axes = self.getAxes2D()
            if self.getBoxXsize() >= self.getBoxYsize():
                return axes[0]
            else:
                return axes[1]
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)
            
    def getAxisMajor3D(self):
        """
        [[3 floats], [3 floats]] getAxisMajor3D()
        Returns the 3D endpoints of the major axis of the bounding box
        at half the height of the space.
        If axes are are equal, returns the X-Axis endpoints.
        """
        try:
            axes = self.getAxes3D()
            if self.getBoxXsize() >= self.getBoxYsize():
                return axes[0]
            else:
                return axes[1]
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)
            
    def getAxisMinor2D(self):
        """
        [[2 floats], [2 floats]] getAxisMinor2D()
        Returns the 2D endpoints of the minor axis of the bounding box.
        If axes are are equal, returns the Y-Axis endpoints.
        """
        try:
            axes = self.getAxes2D()
            if self.getBoxXsize() >= self.getBoxYsize():
                return axes[1]
            else:
                return axes[0]
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)
            
    def getAxisMinor3D(self):
        """
        [[3 floats], [3 floats]] getAxisMinor3D()
        Returns the 3D endpoints of the major axis of the bounding box
        at half the height of the space.
        If axes are are equal, returns the Y-Axis endpoints.
        """
        try:
            axes = self.getAxes3D()
            if self.getBoxXsize() < self.getBoxYsize():
                return axes[0]
            else:
                return axes[1]
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)
           
    def getBoundary(self):
        """
        polygon getBoundary()
        Returns the polygon object representing the current boundary.
        """
        try:
            return self.__boundary
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)   

    
    def getBoundaryLength(self):
        """
        float getBoundaryLength()
        Returns the length of the perimeter.
        """
        try:
            return self.__boundary.length
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)   

    def getBoundingBox2D(self):
        """
        [[2 floats], [2 floats], [2 floats], [2 floats]] getBoundingBox()
        Returns the bounding box as four 2D points in counter-clockwise
        order from the minimum vertex in the coordinate plane.
        """
        try:   
            bounds = self.__boundary.bounds
            return \
                [
                    (bounds[0], bounds[1]),
                    (bounds[2], bounds[1]),
                    (bounds[2], bounds[3]),
                    (bounds[0], bounds[3])
                ]
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)

    def getBoundingBox3D(self):
        """
        [[3 floats], [3 floats], [3 floats], [3 floats]] getBoundingBox3D()
        Returns the bounding box of as four 3D points.
        """
        try: 
            level = self.getLevel()
            bounds = self.getBoundingBox2D()
            return list(map(lambda x: tuple([x[0], x[1], level]), bounds))
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)
            
    def getBoundingCube(self):
        """
        [
            [[3 floats], [3 floats], [3 floats], [3 floats]],
            [[3 floats], [3 floats], [3 floats], [3 floats]]
        ]
        getBoundingCube()
        Returns the bounding cube of as two lists of four 3D points, 
        the first list of the four vertices of the lower cube boundary,
        and the second list the four vertices of the upper cube boundary.
        """
        try: 
            top = self.getHeight() + self.getLevel()
            bounds = self.getBoundingBox3D()
            upper = list(map(lambda x: tuple([x[0], x[1], top]), bounds))
            return [bounds, upper]
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)
            
    def getBoxXsize(self):
        """
        float getBoxXdistance()
        Returns the 2D X-axis distance between the 
        first two points of the aecSpace bounding box.
        """
        try:
            bounds = self.getBoundingBox2D()
            return geometry.Point(bounds[0]).distance(geometry.Point(bounds[1]))
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback) 
            
    def getBoxYsize(self):
        """
        float getBoxYdistance()
        Returns the 2D Y-axis distance between the first and
        third points of the aecSpace bounding box.
        """
        try:
            bounds = self.getBoundingBox2D()
            return geometry.Point(bounds[0]).distance(geometry.Point(bounds[3]))
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback) 
    
    def getCentroid2D(self):
        """
        [2 floats] getCentroid2D()
        Returns the centroid as a 2D point.
        """
        try:           
            return self.__boundary.centroid.bounds[:2]
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)

    def getCentroid3D(self): 
        """
        [3 floats] getCentroid3D()
        Returns the centroid as a 3D point at half the height.
        """
        try:           
            centroid = self.getCentroid2D()
            midHeight = self.getLevel() + (self.getHeight() * 0.5)
            return (centroid[0], centroid[1], midHeight)
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)

    def getColor01(self):     
        """
        [3 floats] getColor01()
        Returns the color as an RGB in the 0 - 1 range.
        """
        try:
            return \
            [
                (self.__colorR / 255),
                (self.__colorG / 255),
                (self.__colorB / 255)
            ]
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)

    def getColor256(self):
        """
        [int, int, int] getColor256()
        Returns the color as an RGB in the 0 - 255 range.
        """
        try:           
            return \
            [
                int(self.__colorR), 
                int(self.__colorG),
                int(self.__colorB)
            ]
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)
    
    def getHeight(self):
        """
        number getHeight()
        Returns the height.
        """
        try:           
            return float(self.__height)
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)
            
    def getID(self):
        """
        string getID()
        Returns the UUID.
        """
        try:           
            return str(self.__id)
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)
            
    def getLevel(self):
        """
        float getLevel()
        Returns the level.
        """
        try:           
            return float(self.__level)
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)

    def getMesh3D(self):
        """
        [[(3 integer index),...][(3 number point),...]] getMesh3D()
        Constructs a 3D mesh representation of the aecSpace as a list of
        indices and a list of points.
        """
        try:
            points = self.getPointsExterior2D()
            mesh = Delaunay(numpy.array(points))
            triangles = mesh.simplices
            points = list(map(lambda x: tuple([x[0], x[1]]), mesh.points))
            analytic = Polygon(*list(map(Point, points)))
            if analytic.is_convex():
                indices = list(map(tuple, triangles))
            else:
                shape = geometry.Polygon(points)
                indices = []
                for triangle in triangles:
                    test = geometry.Polygon([points[triangle[0]], 
                                             points[triangle[1]],
                                             points[triangle[2]]])
                    point = test.representative_point()
                    if shape.contains(point):
                        indices.append(list(triangle))
            level = self.getLevel()
            height = level + self.getHeight()
            offset = len(points)
            offidx = list(map(lambda x: (x[0] + offset, x[1] + offset, x[2] + offset), indices))
            botPoints = list(map(lambda x: (x[0], x[1], level), points))
            topPoints = list(map(lambda x: (x[0], x[1], height), points))
            indices = indices + offidx
            points = botPoints + topPoints
            sides = self.getSides()
            for side in sides:
                indices.append((points.index(side[0]), points.index(side[1]), points.index(side[2])))
                indices.append((points.index(side[0]), points.index(side[2]), points.index(side[3])))
            return [indices, points]
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)
                
    def getName(self):
        """
        string getName()
        Returns the custom designation.
        """
        try:           
            return str(self.__name)
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)

    def getOrigin2D(self):
        """
        [float, float] getOrigin2D()
        Returns the first 2D point in the sequence 
        defining the current perimeter.
        """
        try:           
            return self.getPointsExterior2D()[0]
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)        
        
    def getOrigin3D(self):
        """
        [float, float] getOrigin()
        Returns the first 3D point in the sequence 
        defining the current perimeter.        
        """
        try:
            return self.getPointsExterior3D()[0][0]
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)  
     
    def getPointsExterior2D(self):     
        """
        [[float, float],...] getPointsExterior2D()
        Returns the list of 2D exterior boundary points.
        """
        try:
            return list(self.__boundary.exterior.coords)[:-1]
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)

    def getPointsExterior3D(self):   
        """
        [[(3 numbers),...][(3 numbers),...] getPointsExterior3D()
        Returns the list of 3D boundary points by combining
        the 2D boundary points with the aecSpace level and level + height.
        """
        try:
            points = self.getPointsExterior2D()
            bottom = self.getLevel()
            top = bottom + self.getHeight()
            lower = list(map(lambda x: tuple([x[0], x[1], bottom]), points))
            upper = list(map(lambda x: tuple([x[0], x[1], top]), points))
            return [lower, upper]
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)
            
    def getPointsInterior2D(self):     
        """
        [[float, float],...] getPointsInterior2D()
        Returns the list of interior 2D boundary points.
        """
        try:
            return list(self.__boundary.interior.coords)[:-1]
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)

    def getPointsInterior3D(self):   
        """
        [[float, float, float],...] getPointsInterior3D()
        Returns the list of internal 3D boundary points by combining
        the 2D boundary points with the aecSpace level.
        """
        try:
            points = self.getPointsInterior2D()
            level = self.getLevel()
            return list(map(lambda x: tuple([x[0], x[1], level]), points))
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)            
 
    def getSides(self):
        """
        [[(3 numbers)(3 numbers)(3 numbers)(3 numbers)],...] getSides()
        Returns the quadrilateral sides of the aecSpace prism 
        as a  grouped series of 4 points.
        """
        try:
            points = self.getPointsExterior3D()
            bottom = points[0]
            top = points[1]
            sides = []
            index = 0
            sideQuantity = len(bottom)
            while index < sideQuantity:
                if index < (sideQuantity - 1):
                    side = [bottom[index], bottom[index + 1], top[index + 1], top[index]]
                else:
                    side = [bottom[index], bottom[0], top[0], top[index]]
                sides.append(side)          
                index += 1
            return sides
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)          
    
    def getTransparency(self):
        """
        float getTransparency()
        Returns the Transparency as a percentage between 0 and 1.
        """
        try:           
            return float(self.__transparency)
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)

    def getVolume(self):  
        """
        float getVolume()
        Returns the volume.
        """
        try:           
            return float(self.getArea() * self.getHeight())
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)
            
    def setBoundary(self, points):
        """
        bool setPerimeter([2 numbers],...)
        Creates a new Perimeter from the delivered 2D points.
        Returns True if successful.
        TODO:
        Add error checking here.
        """
        try:
            self.__boundary = geometry.polygon.orient(geometry.Polygon(points))
            return True
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)            

    def setColor(self, newColor = []):
        """
        bool setColor (integers [0 - 255], [0 - 255], [0 - 255])
        Sets the Color[R G B] values or without argument randomizes the color.
        Returns True if successful.
        """
        try:
            
            if newColor:
                newColor = list(map(int, list(newColor)))
                self.__colorR = newColor[0]
                self.__colorG = newColor[1]
                self.__colorB = newColor[2]
            else:
                self.__colorR = random.randint(0, 255)
                self.__colorG = random.randint(0, 255)
                self.__colorB = random.randint(0, 255)
            return True
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)

    def setHeight(self, newHeight = 1):
        """
        bool setHeight(number | string)
        Sets the Height as a float.
        Returns True if successful.
        """
        try:
            self.__height = float(newHeight)
            return True
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)

    def setLevel(self, newLevel = 0):
        """
        bool setLevel(number | string)
        Sets the Level as a float.
        Returns True if successful.
        """
        try:
            self.__level = float(newLevel)
            return True
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)

    def setName(self, newName = ""):
        """
        bool setName(string)
        Sets the Name as a string.
        Returns True if successful.
        """
        try:
            self.__name = str(newName)
            return True
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)
    
    def setTransparency(self, newTrans = 0):
        """
        bool setTransparency(number | string)
        Sets the Transparent percentage or without argument sets Transparency to 0.
        Converts inputs to a range from 0 to 1.
        Returns True if successful.
        """
        try:
            newTrans = self.__aecErrorCheck.makePercentage(newTrans)
            self.__transparency = newTrans
            return True
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)

    def addBoundary(self, points, restart = False):
        """
        bool addBoundary((number, number, number),..., bool)
        If restart is True, constructs a new boundary by combining the
        list of delivered boundaries. If restart is false, combines
        the current boundary with the the delievered boundaries.
        """    
        try:
            if restart:
                boundaries = []
            else:
                boundaries = [self.__boundary]
            self.setBoundary(points)
            boundaries.append(self.__boundary)
            boundaries = geometry.MultiPolygon(boundaries)
            boundary = ops.unary_union(boundaries)
            self.__boundary = boundary
            return True
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)        
    
    def contains(self, point = (0, 0, 0)):
        """
        bool contains((3 numbers))
        Returns True if the delivered point is within the 2D boundary of
        the aecSpace, regardless of their relative Z-Axis positions.
        """
        try:
            point = geometry.Point(point[0], point[1])
            return self.__boundary.contains(point)
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)
            
    def encloses(self, point = (0, 0, 0)):
        """
        bool encloses((3 numbers))
        Returns whether the delivered point falls within the 3D aecSpace,
        respecting the boundary, level, and height of the aecSpace relative
        to the point's position.
        """
        try:
            
            contain = self.contains(point)
            pointZ = point[2]
            if contain and pointZ > self.getLevel() and pointZ < self.getHeight():
                return True
            else:
                return False
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)

    def makeBox(self, origin = (0, 0, 0), vector = (1, 1, 1)):
        """
        bool makeBox((3 numbers]), (3 numbers), float)
        Creates a rectangular aecSpace constructed from an origin point
        and dimensions for length, width, and height.
        Returns True if successful.
        """
        try:
            self.setBoundary(self.makeBoxPoints(origin, vector))
            self.setLevel(origin[2])
            self.setHeight(vector[2])
            return True
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)
            
    def makeBoxPoints(self, origin = (0, 0, 0), vector = (1, 1, 1)):
        """
        [(3 numbers),...] makeBoxPoints((3 numbers]), (3 numbers))
        Returns the coordinates of a box based on the origin and vector.
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
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)
            
    def makeBoxes(self, boxes = [[(0, 0, 0), (1, 1, 1)]]):
         """
         bool makeBoxes([[(3 numbers), (3 numbers)],...]
         Attempts to construct a new shape from a list of orthogonal 
         rectangles described by paired origins and vectors.
         """
         try:
            self.makeBox(boxes[0][0], boxes[0][1])
            for box in boxes[1:]:
                self.addBoundary(self.makeBoxPoints(box[0], box[1]))
            return True
         except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)  

    def makeCircle(self, origin = (0, 0, 0), radius = 1):
         """
         bool makeCircle((3 numbers), number)
         Contructs the aecSpace as an approximate circle, setting
         a ratio from radius to the number of sides.
         """
         try:
             
             if radius < 3:
                 sides = 3
             else:
                 sides = radius
             return self.makePolygon(origin, radius, sides)
         except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)
    
    def makePolygon(self, origin = (0, 0, 0), radius = 1, sides = 3):
         """
         bool makePolygon((3 numbers), number, integer)
         Constructs the aecSpace as a regular polygon 
         centered on the delivered origin point with the first
         vertex at the maximum Y.
         """
         try:
            radius = abs(radius)
            if radius == 0:
                return
            sides = int(abs(sides))
            if sides < 3:
                sides = 3
            angle = math.pi * 0.5
            incAngle = (math.pi * 2) / sides
            points = []
            count = 0
            while count < sides:
                x = origin[0] + (radius * math.cos(angle))
                y = origin[1] + (radius * math.sin(angle))
                points.append((x, y, origin[2]))
                angle += incAngle
                count += 1
            self.setBoundary(points)
            return True
         except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)                
    
    def mirror(self, mPoints = None):
        """
        bool mirror([(float, float), (float, float)])
        Mirrors the aecSpace orthogonally around the  specified line
        as defined by two points, or by default around the major
        orthogonal axis.
        Returns True if successful.
        """
        try:
            if not mPoints:
                mPoints = self.getAxisMajor2D()
            mPnt1 = mPoints[0]
            mPnt2 = mPoints[1]           
            if mPnt1[0] == mPnt2[0]: # vertical mirror
                self.scale([-1, 1, 1], mPnt1)
                return True
            if mPnt1[1] == mPnt2[1]: # horizonal mirror
                self.scale([1, -1, 1], mPnt1)
                return True
            newPoints = \
            self.__aecGeomCalc.mirrorPoints2D(self.getPointsExterior2D(), mPoints)
            self.setBoundary(newPoints)
            return True
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)       

    def move (self, moveBy = (0, 0, 0)):  
        """
        bool move((3 numbers))
        Moves the origin point accoding to the delivered vector
        aand reconstructs the perimeter.
        Returns True if successful.
        """
        try:
            self.__boundary = affinity.translate(
                    self.__boundary,
                    float(moveBy[0]), 
                    float(moveBy[1]),
                    0)
            newLevel = self.getLevel() + float(moveBy[2])
            self.setLevel(newLevel)
            return True
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)  
    
    def rotate(self, angle = 180, pivot = None):
        """
        bool rotate (float, [2 floats])
        Rotates the aecSpace counterclockwise around the 2D pivot point
        by the delivered rotation in degrees.
        If no pivot point is provided, the aecSpace will rotate around
        its centroid.
        Return True if successful.
        """
        try:
            if not pivot:
                pivot = self.getCentroid2D()
            self.__boundary = affinity.rotate(self.__boundary, angle, pivot)
            return True
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)

    def scale(self, scaleBy = (1, 1, 1), scalePoint = None):
        """
        bool scale ((3 numbers]), (3 numbers]))
        Scales the aecSpace by a vector from the delivered point.
        by the delivered rotation in radians.
        If no scale point is provided, the aecSpace will scale from
        its centroid.
        Return True if successful.        
        """
        try:
            if not scalePoint:
                scalePoint = self.getCentroid2D()
            self.__boundary = affinity.scale(
                self.__boundary, 
                scaleBy[0], 
                scaleBy[1], 
                1, 
                scalePoint)
            self.__height *= scaleBy[2]
            return True
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)
            
    def wrap(self, points):
        """
        bool wrapBoundary([[float, float],...])
        Computes the convex hull of a set of 2D points returning the list
        of outermost points in counter-clockwise order, starting from the
        vertex with the lexicographically smallest coordinates. Sets the
        new boundary of the aecSpace to the final list of points.
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
            
            self.setBoundary(lower[:-1] + upper[:-1])
            return True
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)
            
# end class