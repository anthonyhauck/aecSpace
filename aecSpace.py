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
    
    # __boundary is a sympy 2D polygon representing the boundary.
    __boundary = None
    
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
            return float(self.__boundary.area)
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
            boundingBoxX = self.getBoundingBox2D()
            boundingBoxY = self.getBoundingBox2D()
            xAxis = [boundingBoxX[0], boundingBoxX[1]]
            yAxis = [boundingBoxY[0], boundingBoxY[3]]          
            xDisplace = (abs(xAxis[1][0] - xAxis[0][0])) / 2
            yDisplace = (abs(yAxis[1][1] - yAxis[0][1])) / 2
            xAxis[0][1] = yDisplace
            xAxis[1][1] = yDisplace
            yAxis[0][0] = xDisplace
            yAxis[1][0] = xDisplace
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
            axes = self.getAxes2D()
            level = self.getLevel()
            axes[0][0].append(level)
            axes[0][1].append(level)
            axes[1][0].append(level)
            axes[1][1].append(level)
            return axes
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)  
            
    def getAxisMajor2D(self):
        """
        [[2 floats], [2 floats]] getAxisMajor2D()
        Returns the 2D endpoints of the major axis of the bounding box.
        If axes are of equal length, the X-Axis endpoints are returned.
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
        If axes are of equal length, the X-Axis endpoints are returned.
        """
        try:
            majorAxis = self.getAxisMajor2D()
            midHeight = self.getLevel() + (self.getHeight() / 2)
            majorAxis[0].append(midHeight)
            majorAxis[1].append(midHeight)
            return majorAxis
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)
            
    def getAxisMinor2D(self):
        """
        [[2 floats], [2 floats]] getAxisMinor2D()
        Returns the 2D endpoints of the minor axis of the bounding box.
        If axes are of equal length, the Y-Axis endpoints are returned.
        """
        try:
            axes = self.getAxes2D()
            if self.getBoxXsize() > self.getBoxYsize():
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
        If axes are of equal length, the X-Axis endpoints are returned.
        """
        try:
            minorAxis = self.getAxisMinor2D()
            midHeight = self.getLevel() + (self.getHeight() / 2)
            minorAxis[0].append(midHeight)
            minorAxis[1].append(midHeight)
            return minorAxis
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)
           
    def getBoundaryLength(self):
        """
        float getPerimeterLength()
        Returns the length of the perimeter.
        """
        try:
            return self.__boundary.perimeter.evalf()
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
            bounds = list(map(float, list(self.__boundary.bounds)))
            return \
                [
                    [bounds[0], bounds[1]],
                    [bounds[2], bounds[1]],
                    [bounds[2], bounds[3]],
                    [bounds[0], bounds[3]]
                ]
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)

    def getBoundingBox3D(self):
        """
        [[3 floats], [3 floats], [3 floats], [3 floats]]  getBoundingBox3D()
        Returns the bounding box of as four 3D points.
        """
        try: 
            level = self.getLevel()
            bounds = list(map(float, list(self.__boundary.bounds)))
            return \
                [
                    [bounds[0], bounds[1], level],
                    [bounds[2], bounds[1], level],
                    [bounds[2], bounds[3], level],
                    [bounds[0], bounds[3], level]
                ]
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
            bounds = list(map(float, list(self.__boundary.bounds)))
            lower = self.getBoundingBox3D()
            upper = \
                [
                    [bounds[0], bounds[1], top],
                    [bounds[2], bounds[1], top],
                    [bounds[2], bounds[3], top],
                    [bounds[0], bounds[3], top]
                ]           
            return [lower, upper]
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
            boundpoints = self.getBoundingBox2D()
            point1 = geometry.Point2D(boundpoints[0])
            point2 = geometry.Point2D(boundpoints[1])
            return float(point1.distance(point2))
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
            boundpoints = self.getBoundingBox2D()
            point1 = geometry.Point2D(boundpoints[1])
            point2 = geometry.Point2D(boundpoints[2])
            return float(point1.distance(point2))
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback) 
    
    def getCentroid2D(self):
        """
        [2 floats] getCentroid2D()
        Returns the centroid of the space as a 2D point.
        """
        try:           
            centroid = self.__boundary.centroid
            return [float(centroid.x), float(centroid.y)]
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)

    def getCentroid3D(self): 
        """
        [3 floats] getCentroid3D()
        Returns the centroid as a 3D point at half the height.
        """
        try:           
            centroid = self.__boundary.centroid
            midHeight = self.getLevel() + (self.getHeight() / 2)
            return [float(centroid.x), float(centroid.y), midHeight]
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

    def getOrigin2D(self):
        """
        [float, float] getOrigin2D()
        Returns the first 2D point in the sequence 
        defining the current perimeter.
        """
        try:           
            return self.getPoints2D()[0]
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
            point = self.getOrigin2D()
            point.append(self.getLevel())
            return point
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)  
     
    def getPoints2D(self):     
        """
        [[float, float],...] getPoints2D()
        Returns the list of 2D perimeter points.
        """
        try:
            return \
                list(map (lambda point: \
                [
                    float(point.x), 
                    float(point.y)
                ], 
                self.__boundary.vertices))
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)

    def getPoints3D(self):   
        """
        [[float, float, float],...] getPoints3D()
        Returns the list of 3D perimeter points by combining
        the 2D Perimeter points with the Level.
        """
        try:
            return \
            list(map (lambda point: \
            [
                float(point.x), 
                float(point.y), 
                self.getLevel()
            ],
            self.__boundary.vertices))
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
            return float(self.__boundary.area * self.__height)
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
            self.__boundary = geometry.Polygon(*points)
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
            enclosed = self.__boundary.encloses_point(point)
            if enclosed and pointZ > self.getLevel() and pointZ < self.getHeight():
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
            origin = self.__aecErrorCheck.isPoint(origin)
            vector = self.__aecErrorCheck.isPoint(vector)
            self.setBoundary(
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
            
    # TODO: def makePolygon(self, )        
            
    def mirror(self, mirrorLine = None):
        """
        bool mirror([[float, float], [float, float]])
        Changes the perimeter of the aecSpace to correspond to a mirror
        image of the original perimeter about a line defined by the 
        delivered list of two 2D points, or by default around the 
        major axis of the aecSpace.
        Returns True if successful.
        """
        try:
           # if not mirrorLine:
            mirrorLine = self.getAxisMajor2D()
            mirrorLine = geometry.Line(
                geometry.Point2D(mirrorLine[0]), 
                geometry.Point2D(mirrorLine[1]))
            self.__boundary = self.__boundary.reflect(mirrorLine)
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
            self.__boundary = self.__boundary.translate(float(moveBy[0]), float(moveBy[1]))
            newLevel = self.getLevel() + float(moveBy[2])
            self.setLevel(newLevel)
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
            self.__boundary = self.__boundary.rotate(rotation, pivot)
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
                self.__boundary = self.__boundary.scale(scaleBy[0], scaleBy[1], scalePoint)
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
            self.__boundary = geometry.Polygon([0, 0], [1, 0], [1, 1], [0, 1])
            return True
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)       

# end class