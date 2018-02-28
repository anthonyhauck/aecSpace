import math
import random
import traceback
import uuid

from sympy import geometry

from aecErrorCheck import aecErrorCheck

class aecSpace:
    """
    aecSpace
    
    Defines the geometric enclosure of a region defined
    by a list of 2D coordinates and a height.
    
    Current Assumptions + Limitations
    
    Spaces are prisms with bases parallel to the ground plane
    and vertical boundaries.
    
    No curved walls yet.
    """

    # An instance of aecErrorCheck.
    __aecErrorCheck = None

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
    
    # __perimeter is a sympy 2D polygon representing the boundary..
    __perimeter = None
    
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
        self.unit()
        self.setColor()
        self.Identifier = uuid.uuid4()
        self.__aecErrorCheck = aecErrorCheck()

    def getArea(self):
        """
        float getArea()
        Returns the area.
        """
        try:           
            return float(self.__perimeter.area)
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)
            
    def getBoundingBox2D(self):
        """
        [[2 floats], [2 floats], [2 floats], [2 floats]]  getBoundingBox()
        Returns the bounding box as four 2D points in counter-clockwise
        order from the minimum vertex in the coordinate plane.
        """
        try:   
            bounds = list(map(float, list(self.__perimeter.bounds)))
            bounds = \
                [
                    [bounds[0], bounds[1]],
                    [bounds[2], bounds[1]],
                    [bounds[2], bounds[3]],
                    [bounds[0], bounds[3]]
                ]
            return bounds
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)

    def getBoundingBox3D(self):
        """
        [[3 floats], [3 floats], [3 floats], [3 floats]]  getBoundingBox()
        Returns the bounding box of as four 3D points.
        """
        try:   
            bounds = list(map(float, list(self.__perimeter.bounds)))
            bounds = \
                [
                    [bounds[0], bounds[1], self.__level],
                    [bounds[2], bounds[1], self.__level],
                    [bounds[2], bounds[3], self.__level],
                    [bounds[0], bounds[3], self.__level]
                ]
            return bounds
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)
    
    def getCentroid2D(self):
        """
        [2 floats] getCentroid2D()
        Returns the centroid of the space as a 2D point.
        """
        try:           
            centroid = self.__perimeter.centroid
            return [float(centroid.x), float(centroid.y)]
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)

    def getCentroid3D(self): 
        """
        [3 floats] getCentroid3D()
        Returns the centroid as a 3D point.
        """
        try:           
            centroid = self.__perimeter.centroid
            return [float(centroid.x), float(centroid.y), float(self.__level)]
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
        [3 integers] getColor256()
        Returns the color as an RGB in the 0 - 255 range.
        """
        try:           
            return \
            [
                self.__colorR, 
                self.__colorG,
                self.__colorB
            ]
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)
    
    def getHeight(self):
        """
        float getHeight()
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

    def getPoints2D(self):     
        """
        [[2 floats],...] getPoints2D()
        Returns the list of 2D perimeter points.
        """
        try:
            return \
                list(map (lambda point: \
                [
                    float(point.x), 
                    float(point.y)
                ], 
                self.__perimeter.vertices))
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)

    def getPoints3D(self):   
        """
        [[3 floats],...] getPoints3D()
        Returns the list of 3D perimeter points by combining
        the 2D Perimeter points with the Level.
        """
        try:
            return \
                 list(map (lambda point: \
                 [
                    float(point.x), 
                    float(point.y), 
                    float(self.__level)
                 ],
                 self.__perimeter.vertices))
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
            return float(self.__perimeter.area * self.__height)
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
            newColor = list(newColor)
            if len(newColor) > 0:
                newColor = self.__aecErrorCheck.inRange([0, 255], newColor)
                newColor = list(map(int, newColor))
                if newColor[0]:
                    self.__colorR = newColor[0]
                if newColor[1]:
                    self.__colorG = newColor[1]
                if newColor[2]:
                    self.__colorB = newColor[2]
            else:
                newColor = \
                [
                    random.randint(0, 255), 
                    random.randint(0, 255), 
                    random.randint(0, 255)
                ]
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

    def setPerimeter(self, points):
        """
        bool setPerimeter([2 numbers],...)
        Creates a new Perimeter from the delivered 2D points.
        Returns True if successful.
        TODO:
        Add error checking here.
        """
        try:
            self.__perimeter = geometry.Polygon(*points)
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
            newTrans = self.__aecErrorCheck.inRange([0, 1], [float(newTrans)])
            self.__transparency = float(newTrans[0])
            return True
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)

    def encloses(self, point = [0, 0, 0]):
        """
        bool encloses([3 numbers])
        Returns whether the delivered point falls within the 3D aecSpace.
        """
        try:
            point = self.__aecErrorCheck.isPoint(point)
            pointZ = point[2]
            point = geometry.Point2D(point[0], point[1])
            enclosed = self.__perimeter.encloses_point(point)
            if enclosed and pointZ > self.__level and pointZ < self.__height:
                return True
            else:
                return False
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)

    def makeBox(self, origin = [0, 0, 0], vector = [1, 1, 1]):
        """
        bool makeBox([3 numbers], [3 numbers])
        Creates a rectangular aecSpace constructed from an origin point
        and dimensions for length, width, and height.
        Returns True if successful.
        """
        try:
            origin = self.__aecErrorCheck.isPoint(origin, True)
            vector = self.__aecErrorCheck.isPoint(vector, True)
            self.setPerimeter(
                [
                    [origin[0], origin[1]],
                    [vector[0], origin[1]],
                    [vector[0], vector[1]],
                    [origin[0], vector[1]]
                ])
            self.setLevel(origin[2])
            self.setHeight(vector[2])
            return True
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)

    def move (self, moveBy = [0, 0, 0]):  
        """
        bool move([3 numbers])
        Moves the origin point accoding to the delivered vector
        aand reconstructs the perimeter.
        Returns True if successful.
        """
        try:
            moveBy = self.__aecErrorCheck.isPoint(moveBy)
            self.__perimeter = self.__perimeter.translate(float(moveBy[0]), float(moveBy[1]))
            self.__level += float(moveBy[2])
            return True
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)
    
    def rotate(self, rotation = math.pi, pivot = None):
        """
        bool rotate (float, [2 floats])
        Rotates the aecSpace counterclockwise around the 2D pivot point
        by the delivered rotation in radians.
        If no pivot point is provided, the aecSpace will rotate around
        its centroid.
        Return True if successful.
        """
        try:
            if pivot:
                pivot = self.__aecErrorCheck.isPoint(pivot)
            else:
                pivot = self.getCentroid2D()
            pivot = geometry.Point2D(pivot[0], pivot[1])
            self.__perimeter = self.__perimeter.rotate(rotation, pivot)
            return True
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)

    def scale(self, scaleBy = [1, 1, 1], scalePoint = None):
        """
        bool scale ([3 floats], [2 floats])
        Scales the aecSpace by a vector from the delivered point.
        by the delivered rotation in radians.
        If no scale point is provided, the aecSpace will scale from
        its centroid.
        Return True if successful.        
        """
        try:
            if len(scaleBy) > 0:
                if not scaleBy[1]:
                    scaleBy.append(1)
                if not scaleBy[2]:
                    scaleBy.append(1)
                if not scalePoint:
                    scalePoint = self.getCentroid2D()
                self.__perimeter = self.__perimeter.scale(scaleBy[0], scaleBy[1], scalePoint)
                self.__height *= scaleBy[2]
            return True
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)
    
    def unit(self):
        """
        unit()
        Sets the aecSpace to a unit cube with one corner 
        at the coordinate system origin.
        """
        try:
            self.__height = float(1)
            self.__level = float(0)
            self.__perimeter = geometry.Polygon([0, 0], [1, 0], [1, 1], [0, 1])
            return True
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)       

# end class