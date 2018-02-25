import fractions
import math
import random
import traceback
import uuid

from sympy import geometry

from aecErrorCheck import aecErrorCheck

# -------------------------------------------------------------------------
# aecSpace
#
# Defines the geometric enclosure of a region defined
# by a list of 2D coordinates and a height.
#
# Current Assumptions + Limitations
#
# Spaces are prisms with bases parallel to the ground plane and
# vertical boundaries.
#
# No curved walls yet.
# -------------------------------------------------------------------------   

class aecSpace:

# __aecErrorCheck is an instance of aecErrorCheck
    
    __aecErrorCheck = None
    
    # __color[R G B] variables designate the RGB 
    # color components of a Spacein the 0 - 255 range.
    
    __colorR = 0
    __colorG = 0
    __colorB = 0
        
    # __height is the height of the Space prism.
    
    __height = 0
    
    # __identifier is a UUID for the Space.
    
    __id = ""
    
    # __level is the position of the Space perimeter above the zero plane.
    
    __level = 0
    
    # __perimeter is a sympy 2D polygon representing the boundary of the Space.
    
    __perimeter = None
    
    # __name is a custom string designation for the Space.
    
    __name = ""
       
    # Transparency sets the percentage of transparency of the Space
    # for a compatible rendering system as a value from 0 to 1.
    
    __transparency = 0

# -------------------------------------------------------------------------    
# aecSpace Constructor
# -------------------------------------------------------------------------    
    
    def __init__(self):
        self.unit()
        self.setColor()
        self.Identifier = uuid.uuid4()
        self.__aecErrorCheck = aecErrorCheck()

# -------------------------------------------------------------------------
# float getArea()
# Returns the area of the Space.
# -------------------------------------------------------------------------

    def getArea(self):     
        try:           
            return float(self.__perimeter.area)
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)
            
# -------------------------------------------------------------------------
# [[3 floats], [3 floats], [3 floats], [3 floats]]  getBoundingBox()
# Returns the bounding box of the Space as four 3D points
# -------------------------------------------------------------------------

    def getBoundingBox(self):     
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
    
# -------------------------------------------------------------------------
# [float, float] getCentroid2D()
# Returns the centroid of the space as a 2D point.
# -------------------------------------------------------------------------

    def getCentroid2D(self):     
        try:           
            centroid = self.__perimeter.centroid
            return [float(centroid.x), float(centroid.y)]
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)

# -------------------------------------------------------------------------
# [float, float, float] getCentroid3D()
# Returns the centroid of the space as a 3D point.
# -------------------------------------------------------------------------

    def getCentroid3D(self):     
        try:           
            centroid = self.__perimeter.centroid
            return [float(centroid.x), float(centroid.y), float(self.__level)]
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)

# -------------------------------------------------------------------------
# [float, float, float] getColor01()
# Returns the color of the Space as an RGB 0 - 1 list.
# -------------------------------------------------------------------------

    def getColor01(self):     
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

# -------------------------------------------------------------------------
# [int, int, int] getColor256()
# Returns the color of the space as a [R G B] list in the 0 - 255 range.
# -------------------------------------------------------------------------

    def getColor256(self):     
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
    
# -------------------------------------------------------------------------
# float getHeight()
# Returns the Space height
# -------------------------------------------------------------------------
           
    def getHeight(self):     
        try:           
            return float(self.__height)
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)

# -------------------------------------------------------------------------
# string getID()
# Returns the Space UUID.
# -------------------------------------------------------------------------
           
    def getID(self):     
        try:           
            return str(self.__id)
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)

# -------------------------------------------------------------------------
# float getLevel()
# Returns the Space level
# -------------------------------------------------------------------------
           
    def getLevel(self):     
        try:           
            return float(self.__level)
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)

# -------------------------------------------------------------------------
# string getName()
# Returns the Space Name.
# -------------------------------------------------------------------------
           
    def getName(self):     
        try:           
            return str(self.__name)
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)

# -------------------------------------------------------------------------
# [[float float],] getPoints2D()
# Returns a list of 2D points of the Space perimeter.
# -------------------------------------------------------------------------

    def getPoints2D(self):     
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

# -------------------------------------------------------------------------
# [[float float float],]getPoints3D()
# Returns a list of 3D points of the Space perimeter vertices by combining
# the Space's 2D Perimeter points with the Level of the Space.
# -------------------------------------------------------------------------

    def getPoints3D(self):     
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

# -------------------------------------------------------------------------
# float getTransparency()
# Returns the Space Transparency as a float between 0 and 1.
# -------------------------------------------------------------------------
           
    def getTransparency(self):     
        try:           
            return float(self.__transparency)
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)

# -------------------------------------------------------------------------
# float getVolume()
# Returns the volume of the Space.
# -------------------------------------------------------------------------

    def getVolume(self):     
        try:           
            return float(self.__perimeter.area * self.__height)
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)

# -------------------------------------------------------------------------
# bool setColor ([0 - 255], [0 - 255], [0 - 255])
# Sets the Color[R G B] values or without argument randomizes the color.
# -------------------------------------------------------------------------

    def setColor(self, newColor = []):
        try:
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

# -------------------------------------------------------------------------
# bool setHeight(number | string)
# Sets the Space Height, converting it to a float.
# -------------------------------------------------------------------------

    def setHeight(self, newHeight = 1):
        try:
            self.__height = float(newHeight)
            return True
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)
    
# -------------------------------------------------------------------------
# bool setLevel(number)
# Sets the Space Level, converting it to a float.
# -------------------------------------------------------------------------

    def setLevel(self, newLevel = 0):
        try:
            self.__level = float(newLevel)
            return True
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)

# -------------------------------------------------------------------------
# bool setName(string)
# Sets the Space Name, converting it to a string.
# -------------------------------------------------------------------------

    def setName(self, newName = ""):
        try:
            self.__name = str(newName)
            return True
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)

# -------------------------------------------------------------------------
# bool setPerimeter(list of points)
# Creates a new Perimeter from the delivered 2D points.
# -------------------------------------------------------------------------

    def setPerimeter(self, points):
        try:
            # might need some error checking here
            self.__perimeter = geometry.Polygon(*points)
            return True
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)        
    
# -------------------------------------------------------------------------
# bool setTransparency(number | string)
# Sets the Transparent percentage or without argument turns the Space opaque
# by setting Transparency to 0. Converts inputs to a range from 0 to 1.
# 
# -------------------------------------------------------------------------

    def setTransparency(self, newTrans = 0):
        try:
            newTrans = self.__aecErrorCheck.inRange([0, 1], [float(newTrans)])
            self.__transparency = float(newTrans[0])
            return True
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)

# -------------------------------------------------------------------------
# bool encloses([number, number, number])
# Returns whether the delivered point is inside the Space.
# -------------------------------------------------------------------------

    def encloses(self, point = [0, 0, 0]):     
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

# -------------------------------------------------------------------------
# bool makeBox([number, number, number], [number, number, number])
# Creates a rectangular space from constructed from an origin point
# and dimensions fror length, width, and height.
# -------------------------------------------------------------------------

    def makeBox(self, origin = [0, 0, 0], vector = [1, 1, 1]):     
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

# -------------------------------------------------------------------------
# bool move([number, number, number])
# Moves the origin point of the Space along the delivered vector.
# -------------------------------------------------------------------------

    def move (self, moveBy = [0, 0, 0]):     
        try:
            moveBy = self.__aecErrorCheck.isPoint(moveBy)
            self.__perimeter = self.__perimeter.translate(float(moveBy[0]), float(moveBy[1]))
            self.__level += float(moveBy[2])
            return True
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)

# -------------------------------------------------------------------------
# bool rotate ([float, float], float)
# Rotates of the Space by a vector.
# -------------------------------------------------------------------------    
    
    def rotate(self, rotation = math.pi, pivot = None):
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

# -------------------------------------------------------------------------
# bool scale ([float, float, float], [float, float, float])
# Scales the Space by a vector.
# -------------------------------------------------------------------------    
    
    def scale(self, scaleBy = [1, 1, 1], fromPoint = None):
        try:
            if len(scaleBy) > 0:
                if not scaleBy[1]:
                    scaleBy.append(1)
                if not scaleBy[2]:
                    scaleBy.append(1)
                if not fromPoint:
                    fromPoint = self.getCentroid2D()
                self.__perimeter = self.__perimeter.scale(scaleBy[0], scaleBy[1], fromPoint)
                self.__height *= scaleBy[2]
            return True
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)
 
# -------------------------------------------------------------------------    
# unit()
# Resets the space volume to the default unit Space 
# at the coordinate system origin.
# -------------------------------------------------------------------------    
    
    def unit(self):
        try:
            self.__height = float(1)
            self.__level = float(0)
            self.__perimeter = geometry.Polygon([0, 0], [1, 0], [1, 1], [0, 1])
            return True
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)
    # end def       

# end class