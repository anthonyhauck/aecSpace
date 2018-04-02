import math
import random
import traceback
import uuid

import numpy

from shapely import affinity
from shapely import geometry as shape
from shapely import ops as shapeOps

from aecErrorCheck import aecErrorCheck
from aecGeomCalc import aecGeomCalc
from aecVertex import aecVertex

class aecSpace:
    """
    class aecSpace
    Defines the geometric enclosure of a region described by a list of 3D points, 
    a level in relation to the zero plane, and a positive height in relation to the level.

    Current Assumptions + Limitations

    The XY plane is considered horizontal, the Z dimension vertical.

    aecSpaces are prisms with bases parallel to the ground plane
    and having only vertical boundaries.

    Curved walls must be represented by a series of straight segments.

    Note:
    Method comments will refer to "2D point", "3D point", and "3D vector".
    In all cases these data types should should be understood as tuples
    of 2 or 3 numbers as indicated.
    """
 
    # __abandon is a shared list of of self.__property
    # values that will not be serialized.
    # TODO: Implement serialization features.
    
    __abandon = \
    (
        'aecErrorCheck',
        'aecGeomCalc',
        'verticesCeiling',
        'verticesFloor',
        'verticesSides'
    ) # end __abandon
    
    #__preserve is a shared list of self.__property keys of
    # values to be preserved through a call to __initialize

    __preserve = \
    (
        'aecErrorCheck',
        'aecGeomCalc',
        'colorR',
        'colorG',
        'colorB',
        'height',
        'ID',
        'level',
        'name',
        'transparency'
    ) # end __preserve

    def __init__(self):
        """
        INTERNAL
        aecSpace Constructor
        Creates the dictionary of all internal keys and values.        
        Sets the dimensions to a unit cube with a corner at (0, 0, 0).
        Sets the color to random RGB values.
        Sets the ID to a new UUID.
        Creates a new aecErrorCheck instance.

        """
        self.__properties = \
        {
            """
            INTERNAL
            __properties is a dictionary of all aecSpace variables
            """
    
            # The following property values are preserved through a call to __invalidate
    
            'aecErrorCheck' : None,    # An instance of aecErrorCheck.
            'aecGeomCalc' : None,      # An instance of aecGeometryCalc
            'colorR' : 0,              # Red component of the RGB color
            'colorG' : 0,              # Green component of the RGB color
            'colorB' : 0,              # Blue component of the RGB color
            'height' : 0,              # Height of the ceiling above the floor at level.
            'ID' : None,               # A UUID
            'level' : 0,               # The position of the floor above the zero plane.
            'name' : None,             # A custom string designation.
            'transparency' : 0,        # Percentage of transparency for rendering from 0 to 1
    
            # The following properties are reset by __invalidate()
    
            'area' : None,             # Floor area
            'boundaryShape' : None,    # A 2D Shapely polygon of the floor
            'boundingBox' : None,      # Coordinates of the floor bounding box
            'centroid' : None,         # 3D point floor centroid
            'centroid2D' : None,         # 2D point floor centroid
            'circumference' : None,    # Floor perimeter length
            'meshCeiling' : None,      # Compact ceiling mesh with surface normals
            'meshFloor' : None,        # Compact floor mesh with surface normals
            'meshSides' : None,        # Compact meshes of each side  with surface normals
            'meshGeometric' : None,    # Compact mesh without redundancies
            'meshGraphic' : None,      # Verbose mesh with redundancies for each surface
            'normalCeiling' : None,    # Ceiling surface normal
            'normalFloor' : None,      # Floor surface normal
            'normalSides' : None,      # Sides surface normals
            'normalsCeiling' : None,   # List of ceiling 3D points and normals
            'normalsFloor' : None,     # list of floor 3D points and normals
            'normalsSides' : None,     # List of Side 3D points and normals
            'origin' : None,           # first point in the floor point list
            'pointsCeiling' : None,    # List of ceiling 3D points
            'pointsCeiling2D' : None,  # List of ceiling 2D points
            'pointsFloor' : None,      # List of floor 3D points
            'pointsFloor2D' : None,    # List of floor 2D points
            'pointsSides' : None,      # [[(3D point),...]] list of side points
            'verticesCeiling' : None,  # aecVertex list at the ceiling
            'verticesFloor' : None,    # aecVertex list at the floor
            'verticesSides': None,     # aecVertex list of listed sides
            'volume' : None,           # area multiplied by height
            'xAxis' : None,            # 3D endpoints of 'boundingBox' x-axis at level
            'yAxis' : None,            # 3D endpoints of 'boundingBox' y-axis at level
            'xAxis2D' : None,          # 2D endpoints of 'boundingBox' x-axis
            'yAxis2D' : None,          # 2D endpoints of 'boundingBox' y-axis
            'xSize' : None,            # x-axis length
            'ySize' : None             # y-axis length
    
        } # end dictionary        
        
        self.__properties['ID'] = uuid.uuid4()
        self.__properties['aecErrorCheck'] = aecErrorCheck()
        self.__properties['aecGeomCalc'] = aecGeomCalc()
        self.setColor()
        self.makeBox()

    def __initialize(self):
        """
        INTERNAL
        __initialize()
        Resets specific internal variables to NONE
        to ensure on-demand recompute.
        """
        for key in self.__properties:
            if not key in self.__preserve:
                self.__properties[key] = None

    def __setBoundingBox(self):
        """
        INTERNAL
        bool __setBoundingBox()
        Sets bounding box and orthogonal sizes and axes.
        """
        try:
            bounds = self.__properties['boundaryShape'].bounds
            box = self.__properties['boundingBox'] = \
            [
                (bounds[0], bounds[1]),
                (bounds[2], bounds[1]),
                (bounds[2], bounds[3]),
                (bounds[0], bounds[3])
            ]
            self.__properties['xSize'] = shape.Point(box[0]).distance(shape.Point(box[1]))
            self.__properties['ySize'] = shape.Point(box[0]).distance(shape.Point(box[3]))
            level = self.getLevel()
            xDisplace = self.__properties['xSize'] * 0.5
            yDisplace = self.__properties['ySize'] * 0.5
            xPoint1 = (box[0][0], box[0][1] + yDisplace, level)
            xPoint2 = (box[1][0], box[1][1] + yDisplace, level)
            yPoint1 = (box[0][0] + xDisplace, box[0][1], level)
            yPoint2 = (box[3][0] + xDisplace, box[3][1], level)
            self.__properties['xAxis'] = [xPoint1, xPoint2]
            self.__properties['yAxis'] = [yPoint1, yPoint2]
            self.__properties['xAxis2D'] = [xPoint1[:-1], xPoint2[:-1]]
            self.__properties['yAxis2D'] = [yPoint1[:-1], yPoint2[:-1]]
            return True
        except:
            traceback.print_exc()

    def getAngles(self, degrees = False):
        """
        [[(3D point), interior angle float, exterior angle float],] getAngles(bool)
        Returns the interior and exterior horizontal angles at each point 
        defining the floor and ceiling, in radians by default, or in 
        degrees if degrees = True.
        """
        try:
            angles = []
            for vertex in self.getVerticesFloor() + self.getVerticesCeiling():
                angles.append([vertex.getPoint(), 
                               vertex.getAngle(exterior = False, degrees = degrees),
                               vertex.getAngle(exterior = True, degrees = degrees)])
            return angles
        except:
            traceback.print_exc()

    def getArea(self):
        """
        float getArea()
        Returns the area of the floor.
        """
        try:
            if not self.__properties['area']:
                self.__properties['area'] = \
                self.__properties['boundaryShape'].area
            return self.__properties['area']
        except:
            traceback.print_exc()

    def getAxisX(self, points2D = False):
        """
        [(3D point), (3D point)] getAxisX()
        By default returns the 3D x-axis endpoints of the bounding box at floor level.
        If points2D = True returns 2D endpoints.
        """
        try:
            if not self.__properties['xAxis']:
                self.__setBoundingBox()
            if points2D:
                return self.__properties['xAxis2D']
            return self.__properties['xAxis']
        except:
            traceback.print_exc()

    def getAxisY(self, points2D = False):
        """
        [(3D point), (3D point)] getAxisX()
        By default returns the 3D y-axis endpoints of the bounding box at floor level.
        If points2D = True returns 2D endpoints.
        """
        try:
            if not self.__properties['yAxis']:
                self.__setBoundingBox()
            if points2D:
                return self.__properties['yAxis2D']
            return self.__properties['yAxis']
        except:
            traceback.print_exc()

    def getAxisMajor(self, points2D = False):
        """
        [(3D point), (3D point)] getAxisMajor(bool)
        By default returns the 3D endpoints of the longer bounding box at floor level.
        If points2D = True returns 2D endpoints.
        """
        try:
            if not self.__properties['xAxis']:
                self.__setBoundingBox()
            if self.getXsize() >= self.getYsize():
                return self.getAxisX(points2D)
            return self.getAxisY(points2D)
        except:
            traceback.print_exc()

    def getAxisMinor(self, points2D = False):
        """
        [(3D point), (3D point)] getAxisMinor(bool)
        By default returns the 3D endpoints of the shorter bounding box at floor level.
        If points2D = True returns 2D endpoints.
        """
        try:
            if not self.__properties['yAxis']:
                self.__setBoundingBox()
            if self.getXsize() < self.getYsize():
                return self.getAxisX(points2D)
            return self.getAxisY(points2D)
        except:
            traceback.print_exc()

    def getBoundingBox(self):
        """
        [(2D point), (2D point), (2D point), (2D point)] getBoundingBox()
        Returns the bounding box as four 2D points in counter-clockwise
        order from the minimum vertex in the coordinate plane.
        """
        try:
            if not self.__properties['boundingBox']:
                self.__setBoundingBox()
            return self.__properties['boundingBox']
        except:
            traceback.print_exc()

    def getBoundingBoxCeiling(self):
        """
        [(3D point), (3D point), (3D point), (3D point)] getBoundingBoxCeiling()
        Returns the upper bounding box as four 3D points.
        """
        try:
            level = self.getLevel() + self.getHeight()
            bounds = self.getBoundingBox()
            return list(map(lambda x: tuple([x[0], x[1], level]), bounds))
        except:
            traceback.print_exc()

    def getBoundingBoxFloor(self):
        """
        [(3D point), (3D point), (3D point), (3D point)] getBoundingBoxFloor()
        Returns the lower bounding box as four 3D points.
        """
        try:
            level = self.getLevel()
            bounds = self.getBoundingBox()
            return list(map(lambda x: tuple([x[0], x[1], level]), bounds))
        except:
            traceback.print_exc()

    def getCentroid(self, point2D = False):
        """
        (3D point) getCentroid(bool)
        By default returns the centroid as a 3D point at the floor level.
        If points2D = True returns a 2D point.
        """
        try:
            if not self.__properties['centroid']:
                centroid2D = self.__properties['boundaryShape'].centroid.bounds[:2]
                self.__properties['centroid2D'] = (centroid2D[0], centroid2D[1])
                self.__properties['centroid'] = (centroid2D[0], centroid2D[1], self.getLevel())
            if point2D:
                return self.__properties['centroid2D']
            return self.__properties['centroid']
        except:
            traceback.print_exc()

    def getCircumference(self):
        """
        float getCircumference()
        Returns the length of the polygon floor perimeter.
        """
        try:
            if not self.__properties['circumference']:
                self.__properties['circumference'] = \
                self.__properties['boundaryShape'].length
            return self.__properties['circumference']
        except:
            traceback.print_exc()

    def getColor01(self):
        """
        (3 floats) getColor01()
        Returns the color as an RGB in the 0 - 1 range.
        """
        try:
            return \
            (
                (self.__properties['colorR'] / 255),
                (self.__properties['colorG'] / 255),
                (self.__properties['colorB'] / 255)
            )
        except:
            traceback.print_exc()

    def getColor256(self):
        """
        (3 ints) getColor256()
        Returns the color as RGB values in the 0 - 255 range.
        """
        try:
            return \
            (
                int(self.__properties['colorR']),
                int(self.__properties['colorG']),
                int(self.__properties['colorB'])
            )
        except:
            traceback.print_exc()

    def getHeight(self):
        """
        float getHeight()
        Returns the height.
        """
        try:
            return self.__properties['height']
        except:
            traceback.print_exc()

    def getID(self):
        """
        string getID()
        Returns the UUID.
        """
        try:
            return self.__properties['ID']
        except:
            traceback.print_exc()

    def getLevel(self):
        """
        float getLevel()
        Returns the level.
        """
        try:
            return float(self.__properties['level'])
        except:
            traceback.print_exc()

    def getMeshCeiling(self):
        """
        [[(3D point),], [(3 indices),], (3D surface normal)] getMeshCeiling()
        Returns a mesh representation of the ceiling including points, triangles
        in the form of indices into the point list, and a surface normal.
        """
        try:
            if not self.__properties['meshCeiling']:
                points, indices = \
                self.__properties['aecGeomCalc'].getMesh2D(self.getPointsCeiling(points2D=True))
                level = self.getLevel() + self.getHeight()
                points = list(map(lambda x: (x[0], x[1], level), points))
                normal = self.getNormalCeiling()
                normals = []
                x = 0
                while x < len(points):
                    normals.append([points[x], normal])
                    x += 1
                self.__properties['meshCeiling'] = [points, indices, normal]
            return self.__properties['meshCeiling']
        except:
            traceback.print_exc()

    def getMeshFloor(self):
        """
         [[(3D point),], [(3 indices),], (3D surface normal)] getMeshFloor()

        Returns a mesh representation of the floor including points, triangles
        in the form of indices into the point list, and a surface normal.
        """
        try:
            if not self.__properties['meshFloor']:
                points, indices = \
                self.__properties['aecGeomCalc'].getMesh2D(self.getPointsFloor(points2D=True))
                level = self.getLevel()
                points = list(map(lambda x: (x[0], x[1], level), points))
                normal = self.getNormalFloor()
                self.__properties['meshFloor'] = [points, indices, normal]
            return self.__properties['meshFloor']
        except:
            traceback.print_exc()

    def getMeshSides(self):
        """
        [[(3D point) x 4,], (3D surface normal)], [(3 indices),] getMeshSides()
        Returns a mesh representation of the sides including points and surface
        normals for each side, and triangles in the form of indices into the point list.
        """
        try:
            if not self.__properties['meshSides']:
                sides = self.getPointsSides()
                sidNormals = self.getNormalSides()
                points = self.getPointsExterior()
                points = points[0] + points[1]
                sidLen = len(sides)
                indices = []
                normals = []
                x = 0
                while x < sidLen:
                    side = sides[x]
                    indices.append((points.index(side[0]), points.index(side[1]), points.index(side[2])))
                    indices.append((points.index(side[0]), points.index(side[2]), points.index(side[3])))
                    normals.append(sidNormals[x])
                    x += 1
                self.__properties['meshSides'] = [normals, indices]
            return self.__properties['meshSides']
        except:
            traceback.print_exc()

    def getMeshGeometric(self):
        """
        ([[[(3D point),] (3D normal)]],[(3 int index),]] getMeshGeometric()
        Returns points, point normals, and triangle indices into the point list.
        """
        try:
            if not self.__properties['meshGeometric']:
                flrMesh = self.getMeshFloor()
                clgMesh = self.getMeshCeiling()
                indices = flrMesh[1]
                flrIndices = []
                for index in indices:
                    flrIndices.append(index)
                offset = len(self.getPointsFloor())
                indices = clgMesh[1]
                clgIndices = []
                for index in indices:
                    offidx = (index[0] + offset, index[1] + offset, index[2] + offset)
                    clgIndices.append(offidx)
                sides = self.getPointsSides()
                sidIndices = []
                points = self.getPointsFloor() + self.getPointsCeiling()
                for side in sides:
                    sidIndices.append((points.index(side[0]), points.index(side[1]), points.index(side[2])))
                    sidIndices.append((points.index(side[0]), points.index(side[2]), points.index(side[3])))
                indices = flrIndices + clgIndices + sidIndices
                flrVertices = self.getVerticesFloor()
                clgVertices = self.getVerticesCeiling()
                pointnormals = []
                for vertex in flrVertices + clgVertices:
                    pointnormals.append([vertex.getPoint(), vertex.getNormal()])
                self.__properties['meshGeometric'] = [pointnormals, indices]
            return self.__properties['meshGeometric']
        except:
            traceback.print_exc()
            
    def getMeshGraphic(self):
        """
        {[float,],[int,],[float,]} getMeshGraphic()
        Returns points, triangle indices into the points list, and surface normals
        as three flat dictionary entry lists of f;oats for rendering compatibility 
        with some graphic display systems.
        """
        try:
            if not self.__properties['meshGraphic']:
                flrMesh = self.getMeshFloor()
                clgMesh = self.getMeshCeiling()
                sidMeshes = self.getMeshSides()
                points = []
                for point in flrMesh[0] + clgMesh[0]:
                    points.append(point[0])
                    points.append(point[1])
                    points.append(point[2])
                indices = flrMesh[1]
                flrIndices = []
                for index in indices:
                    flrIndices.append(index[0])
                    flrIndices.append(index[1])
                    flrIndices.append(index[2])
                indices = clgMesh[1]
                offset = len(self.getPointsFloor())
                clgIndices = []
                for index in indices:
                    clgIndices.append(index[0] + offset)
                    clgIndices.append(index[1] + offset)
                    clgIndices.append(index[2] + offset)
                offset += offset
                indices = sidMeshes[1]
                sidIndices = []
                for index in indices:
                    sidIndices.append(index[0] + offset)
                    sidIndices.append(index[1] + offset)
                    sidIndices.append(index[2] + offset)
                indices = flrIndices + clgIndices + sidIndices            
                x = 0
                normals = []
                while x < len(self.getPointsFloor()):
                    normals.append(flrMesh[-1][0])
                    normals.append(flrMesh[-1][1])
                    normals.append(flrMesh[-1][2])
                    x += 1
                x = 0
                while x < len(self.getPointsCeiling()):
                    normals.append(clgMesh[-1][0])
                    normals.append(clgMesh[-1][1])
                    normals.append(clgMesh[-1][2])
                    x += 1                
                for item in sidMeshes[0]:
                    side = item[0]
                    normal = item[-1]
                    for point in side:
                        points.append(point[0])
                        points.append(point[1])
                        points.append(point[2])
                        normals.append(normal[0])
                        normals.append(normal[1])
                        normals.append(normal[2])
                self.__properties['meshGraphic'] = \
                { 
                    'points' : points, 
                    'normals' : normals, 
                    'indices' : indices
                }
            return self.__properties['meshGraphic']
        except:
            traceback.print_exc()

    def getName(self):
        """
        string getName()
        Returns the custom designation.
        """
        try:
            return self.__properties['name']
        except:
            traceback.print_exc()

    def getNormalCeiling(self):
        """
        (3D vector) getNormalCeiling()
        Returns the ceiling surface normal.
        """
        try:
            if not self.__properties['normalCeiling']:
                normals = self.getNormalsCeiling()
                srfNormal = normals[0][1]
                for normal in normals[1:]:
                    srfNormal = numpy.add(srfNormal, numpy.array(normal[1]))
                srfNormal = tuple(numpy.divide(srfNormal, len(normals)))
                self.__properties['normalCeiling'] = srfNormal
            return self.__properties['normalCeiling']
        except:
            traceback.print_exc()

    def getNormalFloor(self):
        """
        (3D vector) getNormalFloor()
        Returns the floor surface normal.
        """
        try:
            if not self.__properties['normalFloor']:
                normals = self.getNormalsFloor()
                srfNormal = normals[0][1]
                for normal in normals[1:]:
                    srfNormal = numpy.add(srfNormal, numpy.array(normal[1]))
                srfNormal = tuple(numpy.divide(srfNormal, len(normals)))
                self.__properties['normalFloor'] = srfNormal
            return self.__properties['normalFloor']
        except:
            traceback.print_exc()

    def getNormalSides(self):
        """
        (3D vector) getNormalFloor()
        Returns the floor surface normal.
        """
        try:
            if not self.__properties['normalSides']:
                sides = self.getNormalsSides()
                sidNormals = []
                for side in sides:
                    normals = []
                    srfNormal = side[0][1]
                    normals.append(side[0][0])
                    for item in side[1:]:
                        normals.append(item[0])
                        srfNormal = numpy.add(srfNormal, numpy.array(item[1]))
                    srfNormal = tuple(numpy.divide(srfNormal, len(side)))
                    sidNormals.append([normals, srfNormal])
                self.__properties['normalSides'] = sidNormals
            return self.__properties['normalSides']
        except:
            traceback.print_exc()

    def getNormalsCeiling(self):
        """
        [[(3D point),(3D point)],] getNormalsCeiling()
        Returns the point normals for each of the ceiling 3D points
        in a list of paired points and normals.
        """
        try:
            if not self.__properties['normalsCeiling']:
                normals = []
                vertices = self.getVerticesCeiling()
                for vertex in vertices:
                    normals.append([vertex.getPoint(), vertex.getNormal()])
                self.__properties['normalsCeiling'] = normals
            return self.__properties['normalsCeiling']
        except:
            traceback.print_exc()

    def getNormalsFloor(self):
        """
        [[(3D point),(3D point)],] getNormalsFloor()
        Returns the point normals for each of the floor 3D points
        in a list of paired points and normals.
        """
        try:
            if not self.__properties['normalsFloor']:
                normals = []
                vertices = self.getVerticesFloor()
                for vertex in vertices:
                    normals.append([vertex.getPoint(), vertex.getNormal()])
                self.__properties['normalsFloor'] = normals
            return self.__properties['normalsFloor']
        except:
            traceback.print_exc()

    def getNormalsSides(self):
        """
        [[(3D point),...][[(3 number normal),...]] getNormalsSides()
        Returns the point normals for each of the floor 3D points
        in a list of paired points and normals.
        """
        try:
            if not self.__properties['normalsSides']:
                sideVertices = self.getVerticesSides()
                normals = []
                for side in sideVertices:
                    sidNormals = []
                    for vertex in side:
                        sidNormals.append([vertex.getPoint(), vertex.getNormal()])
                    normals.append(sidNormals)
                self.__properties['normalsSides'] = normals
            return self.__properties['normalsSides']
        except:
            traceback.print_exc()

    def getOrigin(self):
        """
        (float, float, float) getOrigin()
        Returns the first 2D point in the sequence
        defining the current perimeter.
        """
        try:
            if not self.__properties['origin']:
                self.__properties['origin'] = self.getPointsFloor()[0]
            return self.__properties['origin']
        except:
            traceback.print_exc()

    def getPointsCeiling(self, points2D = False):
        """
        [(3D point,...)] getPointsCeiling()
        By default returns a list of 3D points describing the ceiling perimeter.
        2D points are returned if points2D = True.
        """
        try:
            if not self.__properties['pointsCeiling']:
                self.__properties['pointsCeiling2D'] = \
                list(self.__properties['boundaryShape'].exterior.coords)[:-1]
                level = self.getLevel() + self.getHeight()
                self.__properties['pointsCeiling'] = \
                    list(map(lambda pnt: (pnt[0], pnt[1], level),
                             self.__properties['pointsCeiling2D']))
            if points2D:
                return self.__properties['pointsCeiling2D']
            return self.__properties['pointsCeiling']
        except:
            traceback.print_exc()

    def getPointsExterior(self):
        """
        {[(3D point),], [(3D point),], [(3D point),]} getPointsExterior()
        Returns a dictionary of all the points describing the shell.
        """
        try:
            return \
            {
                'floor' : self.getPointsFloor(),
                'ceiling' : self.getPointsCeiling(),
                'sides' : self.getPointsSides()
            }
        except:
            traceback.print_exc()

    def getPointsFloor(self, points2D = False):
        """
        [(2D or 3D point,...)] getPointsFloor()
        By default returns a list of 3D points describing the floor perimeter.
        2D points are returned if points2D = True.
        """
        try:
            if not self.__properties['pointsFloor']:
                self.__properties['pointsFloor2D'] = \
                list(self.__properties['boundaryShape'].exterior.coords)[:-1]
                level = self.getLevel()
                self.__properties['pointsFloor'] = \
                    list(map(lambda pnt: (pnt[0], pnt[1], level),
                             self.__properties['pointsFloor2D']))
            if points2D:
                return self.__properties['pointsFloor2D']
            return self.__properties['pointsFloor']
        except:
            traceback.print_exc()

    def getPointsSides(self, points2D=False):
        """
        [(3D point,...)] getPointsSides()
        By default returns a list of lists of 3D points describing the side perimeters.
        2D points are returned if points2D = True.
        """
        try:
            if not self.__properties['pointsSides']:
                clgPoints = self.getPointsCeiling()
                flrPoints = self.getPointsFloor()
                length = len(clgPoints)
                index = 0
                sides = []
                while index < length:
                    side = []
                    side.append(flrPoints[index])
                    side.append(flrPoints[(index + 1) % length])
                    side.append(clgPoints[(index + 1) % length])
                    side.append(clgPoints[index])
                    sides.append(side)
                    index += 1
                self.__properties['pointsSides'] = sides
            if points2D:
                return self.__properties['pointsSides2D']
            return self.__properties['pointsSides']
        except:
            traceback.print_exc()

    def getTransparency(self):
        """
        float getTransparency()
        Returns the Transparency as a percentage between 0 and 1.
        """
        try:
            return self.__properties['transparency']
        except:
            traceback.print_exc()

    def getVerticesCeiling(self):
        """
        [aecVertex,...] getVerticesCeiling()
        Returns the list of aecVertex instances describing the ceiling perimeter.
        """
        try:
            if not self.__properties['verticesCeiling']:
                clgPoints = self.getPointsCeiling()
                flrPoints = self.getPointsFloor()
                vertices = []
                index = 0
                length = len(flrPoints)
                while index < length:
                    vertices.append(aecVertex(clgPoints, index, flrPoints[index]))
                    index += 1
                self.__properties['verticesCeiling'] = vertices
            return self.__properties['verticesCeiling']
        except:
            traceback.print_exc()

    def getVerticesExterior(self):
        """
        {[aecVertex,], [aecVertex,], [aecVertex,]} getVerticesExterior()
        Returns a dictionary of all the points describing the shell.
        """
        try:
            return \
            {
                'floor' : self.getVerticesFloor(),
                'ceiling': self.getVerticesCeiling(),
                'sides' : self.getVerticesSides()
            }
        except:
            traceback.print_exc()

    def getVerticesFloor(self):
        """
        [aecVertex,] getVerticesFloor()
        Returns the list of aecVertex objects describing the floor perimeter.
        """
        try:
            if not self.__properties['verticesFloor']:
                clgPoints = self.getPointsCeiling()
                flrPoints = self.getPointsFloor()
                vertices = []
                index = 0
                length = len(flrPoints)
                while index < length:
                    vertices.append(aecVertex(flrPoints, index, clgPoints[index]))
                    index += 1
                self.__properties['verticesFloor'] = vertices
            return self.__properties['verticesFloor']
        except:
            traceback.print_exc()

    def getVerticesSides(self):
        """
        [[aecVertex, x 4],] getVerticesFloor()
        Returns the list of lists of aecVertex objects
        describing the perimeter of each side.
        """
        try:
            if not self.__properties['verticesSides']:
                clgVertices = self.getVerticesCeiling()
                flrVertices = self.getVerticesFloor()
                index = 0
                length = len(flrVertices)
                sides = []
                while index < length:
                    side = []
                    side.append(flrVertices[index])
                    side.append(flrVertices[(index + 1) % length])
                    side.append(clgVertices[(index + 1) % length])
                    side.append(clgVertices[index])
                    sides.append(side)
                    index += 1
                self.__properties['verticesSides'] = sides
            return self.__properties['verticesSides']
        except:
            traceback.print_exc()

    def getVolume(self):
        """
        float getVolume()
        Returns the volume calculated from the
        floor area multiplied by the height.
        """
        try:
            if not self.__properties['volume']:
                self.__properties['volume'] = self.getArea() * self.getHeight()
            return self.__properties['volume']
        except:
            traceback.print_exc()

    def getXsize(self):
        """
        float getBoxXsize()
        Returns the 2D x-axis distance between the
        first two points of the aecSpace bounding box.
        """
        try:
            if not self.__properties['xSize']:
                self.__setBoundingBox()
            return self.__properties['xSize']
        except:
            traceback.print_exc()

    def getYsize(self):
        """
        float getBoxYsize()
        Returns the 2D y-axis distance between the first and
        third points of the aecSpace bounding box.
        """
        try:
            if not self.__properties['ySize']:
                self.__setBoundingBox()
            return self.__properties['ySize']
        except:
            traceback.print_exc()

    def setBoundary(self, points=[(0, 0), (1, 0), (1, 1), (0, 1)]):
        """
        bool setPerimeter((2D point), (2D point), (2D point)...)
        Creates a new perimeter from the delivered 2D points.
        Colinear points are removed.
        Returns True if successful.
        """
        try:
            points = self.__properties['aecGeomCalc'].rmvColinear(points)
            if len(points) < 3:
                return False
            self.__initialize()
            self.__properties['boundaryShape'] = shape.polygon.orient(shape.Polygon(points))           
            return True
        except:
            traceback.print_exc()

    def setColor(self, newColor=None):
        """
        bool setColor (integers [0 - 255], [0 - 255], [0 - 255])
        Sets the Color[R G B] values or without argument randomizes the color.
        Returns True if successful.
        """
        try:
            if newColor:
                newColor = list(map(int, list(newColor)))
                self.__properties['colorR'] = newColor[0]
                self.__properties['colorG'] = newColor[1]
                self.__properties['colorB'] = newColor[2]
            else:
                self.__properties['colorR'] = random.randint(0, 255)
                self.__properties['colorG'] = random.randint(0, 255)
                self.__properties['colorB'] = random.randint(0, 255)
            return True
        except:
            traceback.print_exc()

    def setHeight(self, newHeight = 1):
        """
        bool setHeight(number | string)
        Sets the Height as a float.
        Returns True if successful.
        """
        try:
            self.__properties['height'] = float(abs(newHeight))
            return True
        except:
            traceback.print_exc()

    def setLevel(self, newLevel = 0):
        """
        bool setLevel(number | string)
        Sets the Level as a float.
        Returns True if successful.
        """
        try:
            self.__properties['level'] = float(newLevel)
            return True
        except:
            traceback.print_exc()

    def setName(self, newName = ""):
        """
        bool setName(string)
        Sets the Name as a string.
        Returns True if successful.
        """
        try:
            self.__properties['name'] = str(newName)
            return True
        except:
            traceback.print_exc()

    def setTransparency(self, newTrans = 0):
        """
        bool setTransparency(number | string)
        Sets the Transparent percentage or without argument sets Transparency to 0.
        Converts inputs to a range from 0 to 1.
        Returns True if successful.
        """
        try:
            newTrans = self.__properties['aecErrorCheck'].makePercentage(newTrans)
            self.__properties['transparency'] = newTrans
            return True
        except:
            traceback.print_exc()

    def addBoundary(self, points, restart = False):
        """
        bool addBoundary((number, number, number),..., bool)
        If restart is True, constructs a new boundary from the listof delivered points.
        If restart is false, combines the current boundary with boundaries defined by 
        the delivered points.
        """
        try:
            if restart:
                boundaries = []
            else:
                boundaries = [self.__properties['boundaryShape']]
            self.setBoundary(points)
            boundaries.append(self.__properties['boundaryShape'])
            boundaries = shape.MultiPolygon(boundaries)
            boundary = shapeOps.unary_union(boundaries)
            self.__properties['boundaryShape'] = boundary
            self.setBoundary(self.getPointsFloor(points2D = True))
            return True
        except:
            traceback.print_exc()

    def contains(self, point = (0, 0, 0)):
        """
        bool contains((3D Point))
        Returns True if the delivered point is within the 2D boundary of
        the aecSpace, regardless of their relative z-axis positions.
        """
        try:
            point = shape.Point(point[0], point[1])
            return self.__properties['boundaryShape'].contains(point)
        except:
            traceback.print_exc()

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
            return contain and pointZ >= self.getLevel() and pointZ <= self.getHeight()
        except:
            traceback.print_exc()

    def makeBox(self, origin = (0, 0, 0), vector = (1, 1, 1)):
        """
        bool makeBox((3 numbers]), (3 numbers), float)
        Creates a rectangular aecSpace constructed from an origin point
        and a 3D vector describing length, width, and height.
        Returns True if successful.
        """
        try:
            points = self.__properties['aecGeomCalc'].getBoxPoints2D(origin, vector)
            self.setLevel(origin[2])
            self.setHeight(vector[2])
            self.setBoundary(points)
            return True
        except:
            traceback.print_exc()

    def makeBoxes(self, boxes = [[(0, 0, 0), (1, 1, 1)]]):
        """
        bool makeBoxes([[(3 numbers), (3 numbers)],...]
        Attempts to construct a new perimeter from a list of orthogonal
        rectangles described by paired origins and vectors.
        """
        try:
            self.makeBox(boxes[0][0], boxes[0][1])
            for box in boxes[1:]:
                self.addBoundary(self.__properties['aecGeomCalc'].getBoxPoints2D(box[0], box[1]))
            return True
        except:
            traceback.print_exc()

    def makeCircle(self, origin = (0, 0, 0), radius = 1):

        """
        bool makeCircle((3 numbers), number)
        Contructs the perimeter as an approximate circle, setting
        a ratio from radius to the number of sides.
        """
        try:
            if radius < 3:
                sides = 3
            else:
                sides = radius
            return self.makePolygon(origin, radius, sides)
        except:
            traceback.print_exc()

    def makePolygon(self, origin = (0, 0, 0), radius=1, sides=3):
        """
        bool makePolygon((3 numbers), number, integer)
        Constructs the perimeter as a regular polygon centered on the delivered
        origin point with the first vertex at the maximum y-coordinate.
        """
        try:
            radius = abs(radius)
            if radius == 0:
                return False
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
            traceback.print_exc()

    def mirror(self, mPoints = None):
        """
        bool mirror([(float, float), (float, float)])
        Mirrors the aecSpace orthogonally around the  specified line as defined
        by two points, or by default around the major orthogonal axis.
        Returns True if successful.
        """
        try:
            if not mPoints:
                mPoints = self.getAxisMajor(points2D=True)
            mPnt1 = mPoints[0]
            mPnt2 = mPoints[1]
            if mPnt1[0] == mPnt2[0]: # vertical mirror
                self.scale([-1, 1, 1], mPnt1)
                return True
            if mPnt1[1] == mPnt2[1]: # horizonal mirror
                self.scale([1, -1, 1], mPnt1)
                return True
            newPoints = \
            self.__properties['aecGeomCalc'].mirrorPoints2D(
                self.getPointsFloor(points2D=True), mPoints)
            self.setBoundary(newPoints)
            return True
        except:
            traceback.print_exc()

    def move (self, moveBy = (0, 0, 0)):
        """
        bool move((3 numbers))
        Moves the origin point accoding to the delivered vector and reconstructs the perimeter.
        Returns True if successful.
        """
        try:
            self.__properties['boundaryShape'] = \
                    affinity.translate(
                        self.__properties['boundaryShape'],
                        float(moveBy[0]),
                        float(moveBy[1]),
                        0)
            newLevel = self.getLevel() + float(moveBy[2])
            self.setLevel(newLevel)
            self.setBoundary(list(self.__properties['boundaryShape'].exterior.coords)[:-1])
            return True
        except:
            traceback.print_exc()

    def rotate(self, angle = 180, pivot = None):
        """
        bool rotate (float, (2D point))
        Rotates the aecSpace counterclockwise around the 2D pivot point by the delivered
        rotation in degrees.
        If no pivot point is provided, the aecSpace will rotate around its centroid.
        Return True if successful.
        """
        try:
            angle = int(angle)
            if not pivot:
                pivot = self.getCentroid()
            self.__properties['boundaryShape'] = \
                affinity.rotate(self.__properties['boundaryShape'], angle, pivot)
            self.setBoundary(list(self.__properties['boundaryShape'].exterior.coords)[:-1])
            return True
        except:
            traceback.print_exc()

    def scale(self, scaleBy = (1, 1, 1), scalePoint = None):
        """
        bool scale ((3 numbers]), (3 numbers]))
        Scales the aecSpace by a vector from the delivered point.
        If no scale point is provided, the aecSpace will scale from its centroid.
        Return True if successful.
        """
        try:
            if not scalePoint:
                scalePoint = self.getCentroid()
            self.__properties['boundaryShape'] = \
                affinity.scale(
                    self.__properties['boundaryShape'],
                    scaleBy[0],
                    scaleBy[1],
                    1,
                    scalePoint)
            self.__properties['height'] *= scaleBy[2]
            self.setBoundary(list(self.__properties['boundaryShape'].exterior.coords[:-1]))
            return True
        except:
            traceback.print_exc()

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
            traceback.print_exc()

# end class
