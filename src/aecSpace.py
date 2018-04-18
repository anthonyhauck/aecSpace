import math
import numpy
import random
import traceback
import uuid

from shapely import affinity as affine
from shapely import geometry as shapely
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
        'verticesCeiling',
        'verticesFloor',
        'verticesSides'
    )

    #__retain is a shared list of self.__property keys of
    # values to be retained through a call to __initialize

    __retain = \
    (
        'colorR',
        'colorG',
        'colorB',
        'height',
        'ID',
        'level',
        'name',
        'transparency'
    )
    
    # utility objects and data shared by all instances of aecSpace
    
    __aecErrorCheck = aecErrorCheck()   # An instance of aecErrorCheck.
    __aecGeomCalc = aecGeomCalc()       # An instance of aecGeometryCalc
    __type = 'aecSpace'                 # Type identifier of object instances
    
    def __init__(self):
        """
        INTERNAL
        aecSpace Constructor
        Creates the dictionary of all internal keys and values.
        Sets the dimensions to a unit cube with a corner at (0, 0, 0).
        Sets the color to random RGB values.
        Sets the ID to a new UUID.

        """
        
        #__properties is a dictionary of all aecSpace instance variables
        
        self.__properties = \
        {
            # The following property values are preserved through a call to __initialize

            'colorR' : 0,              # Red component of the RGB color
            'colorG' : 0,              # Green component of the RGB color
            'colorB' : 0,              # Blue component of the RGB color
            'height' : 0,              # Height of the ceiling above the floor at level.
            'ID' : None,               # A UUID
            'level' : 0,               # The position of the floor above the zero plane.
            'name' : "",             # A custom string designation.
            'transparency' : 0,        # Percentage of transparency for rendering from 0 to 1

            # The following properties are reset by __invalidate()

            'area' : None,             # Floor area
            'boundaryShape' : None,    # A 2D Shapely polygon of the floor
            'boundingBox' : None,      # Coordinates of the floor bounding box
            'centroid' : None,         # 3D point floor centroid
            'centroid2D' : None,       # 2D point floor centroid
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
        self.setColor()
        self.makeBox()

    def __initialize(self):
        """
        INTERNAL
        __initialize()
        Resets specific internal variables to NONE to ensure
        on-demand recompute if the space boundary changes.
        """
        for key in self.__properties:
            if not key in self.__retain:
                self.__properties[key] = None

    def __setBoundingBox(self):
        """
        INTERNAL
        bool __setBoundingBox()
        Sets the bounding box and orthogonal sizes and axes.
        """
        try:
            if not self.__properties['boundaryShape']:
                return False
            bounds = self.__properties['boundaryShape'].bounds
            box = self.__properties['boundingBox'] = \
            [
                (bounds[0], bounds[1]),
                (bounds[2], bounds[1]),
                (bounds[2], bounds[3]),
                (bounds[0], bounds[3])
            ]
            self.__properties['xSize'] = shapely.Point(box[0]).distance(shapely.Point(box[1]))
            self.__properties['ySize'] = shapely.Point(box[0]).distance(shapely.Point(box[3]))
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
        except Exception:
            traceback.print_exc()
            return False

    def addBoundary(self, points, restart = False):
        """
        bool addBoundary([(2D or 3D point),], bool)
        If restart is True, constructs a new boundary from the delivered list of points.
        If restart is False, combines the current boundary with boundaries defined by
        the delivered points.
        Returns False if the delivered points do not resolve to a single non-crossing
        polygon and leaves the current boundary unchanged.
        Returns True if successful.
        """
        try:
            if restart or not self.__properties['boundaryShape']:
                boundaries = []
            else:
                boundaries = [self.__properties['boundaryShape']]
            if self.setBoundary(points):
                boundaries.append(self.__properties['boundaryShape'])
                boundaries = shapely.MultiPolygon(boundaries)
                boundary = shapeOps.unary_union(boundaries)
                if type(boundary) != shapely.polygon.Polygon:
                    return False
                self.setBoundary(list(boundary.exterior.coords)[:-1])
                return True
            return False
        except Exception:
            traceback.print_exc()
            return False

    def enclosesPoint(self, point):
        """
        bool encloses((3D point))
        Returns True if the delivered point falls within the 3D aecSpace,
        respecting the boundary, level, and height of the space relative
        to the point's position, returning False if the point is outside
        the space.
        Returns None on failure.
        """
        try:
            contain = self.__aecGeomCalc.containsPoint(self.getPointsFloor(points2D = True), point)
            pointZ = point[2]
            return contain and pointZ >= self.getLevel() and pointZ <= self.getHeight()
        except Exception:
            traceback.print_exc()
            return None

    def fitWithin(self, boundary):
        """
        bool fitWithin([(2D or 3D point),*3+])
        If the aecSpace boundary is not wholly within the delivered perimeter as
        described in a list of points, the aecSpace will reconfigure its perimeter
        to fit within the delivered perimeter.
        Returns True if successful, otherwise returning None.
        """
        try:
            shape = self.getPointsFloor()
            if shape:
                intersect = self.__aecGeomCalc.getIntersection(boundary, shape)
                if intersect:
                    self.setBoundary(intersect)
                    return True
            return None
        except Exception:
            traceback.print_exc()
            return None            
    
    def getAngles(self, degrees = False):
        """
        [[(3D point), interior angle float, exterior angle float],] getAngles(bool)
        Returns the interior and exterior horizontal angles at each point
        defining the floor and ceiling, in radians by default, or in
        degrees if degrees = True.
        Return None on failure.
        """
        try:
            angles = []
            for vertex in self.getVerticesFloor() + self.getVerticesCeiling():
                angles.append([vertex.getPoint(),
                               vertex.getAngle(exterior = False, degrees = degrees),
                               vertex.getAngle(exterior = True, degrees = degrees)])
            return angles
        except Exception:
            traceback.print_exc()
            return None

    def getArea(self):
        """
        float getArea()
        Returns the area of the boundary at the level.
        Returns None if there is no current boundary or on other failure.
        """
        try:
            if not self.__properties['boundaryShape']:
                return None
            if not self.__properties['area']:
                self.__properties['area'] = \
                self.__properties['boundaryShape'].area
            return self.__properties['area']
        except Exception:
            traceback.print_exc()
            return None

    def getAxisX(self, points2D = False):
        """
        [(3D point),] getAxisX()
        By default returns the two 3D x-axis endpoints of the bounding box at level.
        If points2D = True returns 2D endpoints.
        Returns None if there is no current boundary or on other failure.
        """
        try:
            if not self.__properties['boundaryShape']:
                return None            
            if not self.__properties['xAxis']:
                self.__setBoundingBox()
            if points2D:
                return self.__properties['xAxis2D']
            return self.__properties['xAxis']
        except Exception:
            traceback.print_exc()
            return None

    def getAxisY(self, points2D = False):
        """
        [(3D point),] getAxisX()
        By default returns the two 3D y-axis endpoints of the bounding box at level.
        If points2D = True returns 2D endpoints.
        Returns None if there is no current boundary or on other failure.
        """
        try:
            if not self.__properties['boundaryShape']:
                return None            
            if not self.__properties['yAxis']:
                self.__setBoundingBox()
            if points2D:
                return self.__properties['yAxis2D']
            return self.__properties['yAxis']
        except Exception:
            traceback.print_exc()
            return None

    def getAxisMajor(self, points2D = False):
        """
        [(3D point),] getAxisMajor(bool)
        By default returns the two 3D endpoints of the longer bounding box 
        axis at the level or the x-axis if both axes are of equal length.
        If points2D = True returns 2D endpoints.
        Returns None if there is no current boundary or on other failure.
        """
        try:
            if not self.__properties['boundaryShape']:
                return None            
            if not self.__properties['xAxis']:
                self.__setBoundingBox()
            if self.getXsize() >= self.getYsize():
                return self.getAxisX(points2D)
            return self.getAxisY(points2D)
        except Exception:
            traceback.print_exc()
            return None

    def getAxisMinor(self, points2D = False):
        """
        [(3D point),] getAxisMinor(bool)
        By default returns the two 3D endpoints of the shorter bounding box 
        axis at the level or the y-axis if both axes are of equal length.
        If points2D = True returns 2D endpoints.
        Returns None if there is no current boundary or on other failure.
        """
        try:
            if not self.__properties['boundaryShape']:
                return None            
            if not self.__properties['yAxis']:
                self.__setBoundingBox()
            if self.getXsize() < self.getYsize():
                return self.getAxisX(points2D)
            return self.getAxisY(points2D)
        except Exception:
            traceback.print_exc()
            return None

    def getBoundingBox(self):
        """
        [(2D point),] getBoundingBox()
        Returns the bounding box as four 2D points in counter-clockwise
        order from the minimum vertex in the coordinate plane.
        Returns None if there is no current boundary or on other failure.
        """
        try:
            if not self.__properties['boundaryShape']:
                return None
            if not self.__properties['boundingBox']:
                self.__setBoundingBox()
            return self.__properties['boundingBox']
        except Exception:
            traceback.print_exc()
            return None

    def getBoundingBoxCeiling(self):
        """
        [(3D point),] getBoundingBoxCeiling()
        Returns the bounding box at the level + the height as four 3D points in
        counter-clockwise order from the minimum vertex in the coordinate plane.
        Returns None if there is no current boundary or on other failure.
        """
        try:
            if not self.__properties['boundaryShape']:
                return None
            level = self.getLevel() + self.getHeight()
            bounds = self.getBoundingBox()
            return list(map(lambda x: tuple([x[0], x[1], level]), bounds))
        except Exception:
            traceback.print_exc()
            return None

    def getBoundingBoxFloor(self):
        """
        [(3D point),] getBoundingBoxFloor()
        Returns the bounding box at the level as four 3D points in counter-clockwise
        order from the minimum vertex in the coordinate plane.
        Returns None if there is no current boundary or on other failure.
        """
        try:
            if not self.__properties['boundaryShape']:
                return None            
            level = self.getLevel()
            bounds = self.getBoundingBox()
            return list(map(lambda x: tuple([x[0], x[1], level]), bounds))
        except Exception:
            traceback.print_exc()
            return None

    def getCentroid(self, point2D = False):
        """
        (3D point) getCentroid(bool)
        By default returns the centroid as a 3D point at the level.
        If points2D = True returns a 2D point.
        Returns None if there is no current boundary or on other failure.
        """
        try:
            if not self.__properties['boundaryShape']:
                return None            
            if not self.__properties['centroid']:
                centroid2D = self.__properties['boundaryShape'].centroid.bounds[:2]
                self.__properties['centroid2D'] = (centroid2D[0], centroid2D[1])
                self.__properties['centroid'] = (centroid2D[0], centroid2D[1], self.getLevel())
            if point2D:
                return self.__properties['centroid2D']
            return self.__properties['centroid']
        except Exception:
            traceback.print_exc()
            return None

    def getCircumference(self):
        """
        float getCircumference()
        Returns the length of the polygon perimeter at the level.
        Returns None if there is no current boundary or on other failure.
        """
        try:
            if not self.__properties['boundaryShape']:
                return None            
            if not self.__properties['circumference']:
                self.__properties['circumference'] = \
                self.__properties['boundaryShape'].length
            return self.__properties['circumference']
        except Exception:
            traceback.print_exc()
            return None

    def getColor01(self):
        """
        (3 floats) getColor01()
        Returns the color as an RGB tuple with three values in the 0 - 1 range.
        Returns None on failure.
        """
        try:
            return \
            (
                (self.__properties['colorR'] / 255),
                (self.__properties['colorG'] / 255),
                (self.__properties['colorB'] / 255)
            )
        except Exception:
            traceback.print_exc()
            return None

    def getColor256(self):
        """
        (3 ints) getColor256()
        Returns the color as an RGB tuple with three values in the 0 - 255 range.
        Returns None on failure.
        """
        try:
            return \
            (
                int(self.__properties['colorR']),
                int(self.__properties['colorG']),
                int(self.__properties['colorB'])
            )
        except Exception:
            traceback.print_exc()
            return None

    def getHeight(self):
        """
        float getHeight()
        Returns the space height.
        Returns None on failure.
        """
        try:
            return self.__properties['height']
        except Exception:
            traceback.print_exc()
            return None

    def getID(self):
        """
        string getID()
        Returns the unique ID automatically generated when 
        an aecSpace instance is created.
        Returns None on failure.
        """
        try:
            return self.__properties['ID']
        except Exception:
            traceback.print_exc()
            return None

    def getLevel(self):
        """
        float getLevel()
        Returns the space level.
        Returns None on failure.
        """
        try:
            return float(self.__properties['level'])
        except Exception:
            traceback.print_exc()
            return None

    def getMeshCeiling(self):
        """
        [[(3D point),], [(3 indices),], (3D surface normal)] getMeshCeiling()
        Returns a mesh representation of the ceiling including points, triangles
        in the form of indices into the point list, and a surface normal.
        Returns None if there is no current boundary or on other failure.
        """
        try:
            if not self.__properties['boundaryShape']:
                return None            
            if not self.__properties['meshCeiling']:
                points, indices = \
                self.__aecGeomCalc.getMesh2D(self.getPointsCeiling(points2D=True))
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
        except Exception:
            traceback.print_exc()
            return None

    def getMeshFloor(self):
        """
        [[(3D point),], [(3 indices),], (3D surface normal)] getMeshFloor()
        Returns a mesh representation of the floor including points, triangles
        in the form of indices into the point list, and a surface normal.
        Returns None if there is no current boundary or on other failure.
        """
        try:
            if not self.__properties['boundaryShape']:
                return None            
            if not self.__properties['meshFloor']:
                points, indices = \
                self.__aecGeomCalc.getMesh2D(self.getPointsFloor(points2D=True))
                level = self.getLevel()
                points = list(map(lambda x: (x[0], x[1], level), points))
                normal = self.getNormalFloor()
                self.__properties['meshFloor'] = [points, indices, normal]
            return self.__properties['meshFloor']
        except Exception:
            traceback.print_exc()
            return None

    def getMeshSides(self):
        """
        [[(3D point),], (3D surface normal)], [(3 indices),] getMeshSides()
        Returns a mesh representation of the sides including points and surface
        normals for each side, and triangles in the form of indices into the point list.
        Returns None if there is no current boundary or on other failure.
        """
        try:
            if not self.__properties['boundaryShape']:
                return None            
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
        except Exception:
            traceback.print_exc()
            return None

    def getMeshGeometric(self):
        """
        ([[[(3D point),] (3D normal)]],[(3 int index),]] getMeshGeometric()
        Returns a simple mesh representation of the space including points, 
        point normals, and triangle indices into the point list.
        Returns None if there is no current boundary or on other failure.
        """
        try:
            if not self.__properties['boundaryShape']:
                return None            
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
        except Exception:
            traceback.print_exc()
            return None

    def getMeshGraphic(self):
        """
        {'points' : [float,], 'indices' : [int,], 'normals' : [int,]} getMeshGraphic()
        Returns points, triangle indices into the points list, and surface normals
        as three flat dictionary entry lists of floats for rendering compatibility
        with graphic display systems.
        Returns None if there is no current boundary or on other failure.
        """
        try:
            if not self.__properties['boundaryShape']:
                return None            
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
        except Exception:
            traceback.print_exc()
            return None

    def getName(self):
        """
        string getName()
        Returns the custom string designation.
        Returns None on failure.
        """
        try:
            return self.__properties['name']
        except Exception:
            traceback.print_exc()
            return None

    def getNormalCeiling(self):
        """
        (3D vector) getNormalCeiling()
        Returns the ceiling surface normal.
        RReturns None if there is no current boundary or on other failure.
        """
        try:
            if not self.__properties['boundaryShape']:
                return None            
            if not self.__properties['normalCeiling']:
                normals = self.getNormalsCeiling()
                srfNormal = normals[0][1]
                for normal in normals[1:]:
                    srfNormal = numpy.add(srfNormal, numpy.array(normal[1]))
                srfNormal = tuple(numpy.divide(srfNormal, len(normals)))
                self.__properties['normalCeiling'] = srfNormal
            return self.__properties['normalCeiling']
        except Exception:
            traceback.print_exc()
            return None

    def getNormalFloor(self):
        """
        (3D vector) getNormalFloor()
        Returns the floor surface normal.
        Returns None if there is no current boundary or on other failure.
        """
        try:
            if not self.__properties['boundaryShape']:
                return None            
            if not self.__properties['normalFloor']:
                normals = self.getNormalsFloor()
                srfNormal = normals[0][1]
                for normal in normals[1:]:
                    srfNormal = numpy.add(srfNormal, numpy.array(normal[1]))
                srfNormal = tuple(numpy.divide(srfNormal, len(normals)))
                self.__properties['normalFloor'] = srfNormal
            return self.__properties['normalFloor']
        except Exception:
            traceback.print_exc()
            return None

    def getNormalSides(self):
        """
        [[(3D point),], (3D vector)],] getNormalSides()
        Returns a list pairing sets of points defining a single side with their surface normal.
        Returns None if there is no current boundary or on other failure.
        """
        try:
            if not self.__properties['boundaryShape']:
                return None            
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
        except Exception:
            traceback.print_exc()
            return None

    def getNormalsCeiling(self):
        """
        [[(3D point), (3D vector)],] getNormalsCeiling()
        Returns the point normals for each of the ceiling 
        3D points in a list of paired points and normals.
        Returns None if there is no current boundary or on other failure.
        """
        try:    
            if not self.__properties['boundaryShape']:
                return None
            if not self.__properties['normalsCeiling']:
                normals = []
                vertices = self.getVerticesCeiling()
                for vertex in vertices:
                    normals.append([vertex.getPoint(), vertex.getNormal()])
                self.__properties['normalsCeiling'] = normals
            return self.__properties['normalsCeiling']
        except Exception:
            traceback.print_exc()

    def getNormalsFloor(self):
        """
        [[(3D point), (3D vector)],] getNormalsFloor()
        Returns the point normals for each of the floor 
        3D points in a list of paired points and normals.
        Returns None if there is no current boundary or on other failure.
        """
        try:
            if not self.__properties['boundaryShape']:
                return None            
            if not self.__properties['normalsFloor']:
                normals = []
                vertices = self.getVerticesFloor()
                for vertex in vertices:
                    normals.append([vertex.getPoint(), vertex.getNormal()])
                self.__properties['normalsFloor'] = normals
            return self.__properties['normalsFloor']
        except Exception:
            traceback.print_exc()
            return None

    def getNormalsSides(self):
        """
        [[[(3D point), (3D vector)],],] getNormalsSides()
        Returns the point normals for each of the sides 3D points
        in a list of paired points and normals grouped by each side.
        Returns None if there is no current boundary or on other failure.        
        """
        try:
            if not self.__properties['boundaryShape']:
                return None            
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
        except Exception:
            traceback.print_exc()
            return None

    def getOrigin(self):
        """
        (3D point) getOrigin()
        Returns the first 3D point in the sequence defining the current perimeter.
        Returns None if there is no current boundary or on other failure.
        """
        try:
            if not self.__properties['boundaryShape']:
                return None            
            if not self.__properties['origin']:
                self.__properties['origin'] = self.getPointsFloor()[0]
            return self.__properties['origin']
        except Exception:
            traceback.print_exc()
            return None

    def getPointsCeiling(self, points2D = False):
        """
        [(3D point),] getPointsCeiling()
        By default returns a list of 3D points describing the ceiling perimeter.
        2D points are returned if points2D = True.
        Returns None if there is no current boundary or on other failure.
        """
        try:
            if not self.__properties['boundaryShape']:
                return None            
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
        except Exception:
            traceback.print_exc()
            return None

    def getPointsExterior(self):
        """
        {'floor' : [(3D point),], 'ceiling' : [(3D point),], 'sides' : [[(3D point),], ]} 
        getPointsExterior()
        Returns a dictionary of all the points describing the space.
        Returns None if there is no current boundary or on other failure.
        """
        try:
            if not self.__properties['boundaryShape']:
                return None            
            return \
            {
                'floor' : self.getPointsFloor(),
                'ceiling' : self.getPointsCeiling(),
                'sides' : self.getPointsSides()
            }
        except Exception:
            traceback.print_exc()
            return None

    def getPointsFloor(self, points2D = False):
        """
        [(2D or 3D point,...)] getPointsFloor()
        By default returns a list of 3D points describing the floor perimeter.
        2D points are returned if points2D = True.
        Returns None if there is no current boundary or on other failure.
        """
        try:
            if not self.__properties['boundaryShape']:
                return None            
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
        except Exception:
            traceback.print_exc()
            return None

    def getPointsSides(self, points2D = False):
        """
        [[(3D point),],] getPointsSides()
        By default returns a list of lists of 3D points describing the side perimeters.
        2D points are returned if points2D = True.
        Returns None if there is no current boundary or on other failure.
        """
        try:
            if not self.__properties['boundaryShape']:
                return None            
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
        except Exception:
            traceback.print_exc()
            return None

    def getProperties(self):
        """
        dictionary getProperties()
        Retrieves the properties dictionary of all internal values of the space.
        Intended for use by other components of the aecSpace toolkit.
        Returns None on failure.
        """
        try:
            return self.__properties
        except Exception:
            traceback.print_exc()
            return None        

    def getProperty(self, prpName):
        """
        value getProperty(string)
        Directly retrieves a property by its string key, bypassing all error checking.
        Intended for use by other components of the aecSpace toolkit.
        Returns None on failure.
        """
        try:
            return self.__properties[prpName]
        except Exception:
            traceback.print_exc()
            return None        

    def getTransparency(self):
        """
        float getTransparency()
        Returns the Transparency as a percentage between 0 and 1.
        Returns None on failure.
        """
        try:
            return self.__properties['transparency']
        except Exception:
            traceback.print_exc()
            return None

    def getType(self):
        """
        string getType()
        Returns the constant 'aecSpace' to identify the object type.
        Returns None on failure.
        """
        try:
            return self.__type
        except Exception:
            traceback.print_exc()
            return None           
    
    def getVerticesCeiling(self):
        """
        [aecVertex,] getVerticesCeiling()
        Returns the list of aecVertex instances describing the ceiling perimeter.
        Returns None if there is no current boundary or on other failure.
        """
        try:
            if not self.__properties['boundaryShape']:
                return None            
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
        except Exception:
            traceback.print_exc()
            return None

    def getVerticesExterior(self):
        """
        {'floor' : [aecVertex,], 'ceiling' : [aecVertex,], 'sides' : [aecVertex,]} 
        getVerticesExterior()
        Returns a dictionary of all the aecVertex instances describing the space.
        Returns None if there is no current boundary or on other failure.
        """
        try:
            if not self.__properties['boundaryShape']:
                return None            
            return \
            {
                'floor' : self.getVerticesFloor(),
                'ceiling': self.getVerticesCeiling(),
                'sides' : self.getVerticesSides()
            }
        except Exception:
            traceback.print_exc()
            return None

    def getVerticesFloor(self):
        """
        [aecVertex,] getVerticesFloor()
        Returns the list of aecVertex instances describing the floor perimeter.
        Returns None if there is no current boundary or on other failure.
        """
        try:
            if not self.__properties['boundaryShape']:
                return None            
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
        except Exception:
            traceback.print_exc()
            return None

    def getVerticesSides(self):
        """
        [[aecVertex,],] getVerticesFloor()
        Returns the list of lists of aecVertex instances describing the perimeter of each side.
        Returns None if there is no current boundary or on other failure.
        """
        try:
            if not self.__properties['boundaryShape']:
                return None            
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
        except Exception:
            traceback.print_exc()
            return None

    def getVolume(self):
        """
        float getVolume()
        Returns the volume calculated from the boundary area multiplied by the height.
        Returns None if there is no current boundary or on other failure.
        """
        try:
            if not self.__properties['boundaryShape']:
                return None            
            if not self.__properties['volume']:
                self.__properties['volume'] = self.getArea() * self.getHeight()
            return self.__properties['volume']
        except Exception:
            traceback.print_exc()
            return None

    def getXsize(self):
        """
        float getBoxXsize()
        Returns the 2D x-axis length of the space bounding box.
        Returns None if there is no current boundary or on other failure.
        """
        try:
            if not self.__properties['boundaryShape']:
                return None            
            if not self.__properties['xSize']:
                self.__setBoundingBox()
            return self.__properties['xSize']
        except Exception:
            traceback.print_exc()
            return None

    def getYsize(self):
        """
        float getBoxYsize()
        Returns the 2D y-axis length of the space bounding box.
        Returns None if there is no current boundary or on other failure.
        """
        try:
            if not self.__properties['boundaryShape']:
                return None            
            if not self.__properties['ySize']:
                self.__setBoundingBox()
            return self.__properties['ySize']
        except Exception:
            traceback.print_exc()
            return None

    def makeBox(self, origin = (0, 0, 0), vector = (1, 1, 1)):
        """
        bool makeBox((3D point), (3D vector))
        Creates a rectangular space constructed from an origin point
        and a 3D vector describing length, width, and height.
        Returns True on success.
        Returns False on failure.
        """
        try:
            points = self.__aecGeomCalc.getBoxPoints2D(origin, vector)
            self.setLevel(origin[2])
            self.setHeight(vector[2])
            self.setBoundary(points)
            return True
        except Exception:
            traceback.print_exc()
            return False

    def makeBoxes(self, boxes = [[(0, 0, 0), (1, 1, 1)]]):
        """
        bool makeBoxes([[(3D Point), (3D vector)],])
        Attempts to construct a new perimeter from a list of orthogonal
        rectangles described by paired origins and vectors.
        Returns True if successful.
        """
        try:
            self.makeBox(boxes[0][0], boxes[0][1])
            for box in boxes[1:]:
                self.addBoundary(self.__aecGeomCalc.getBoxPoints2D(box[0], box[1]))
            return True
        except Exception:
            traceback.print_exc()
            return False

    def makeCross(self, origin = (0, 0, 0), vector = (1, 1, 1),
                        xWidth = 0.33333333, yDepth = 0.33333333,
                        xAxis = 0.5, yAxis = 0.5):
        """
        bool makeCross((3D point), (3D vector), percent, percent, percent, percent)
        Constructs a cross-shaped space within the box defined by point and vector.
        xWidth and yDepth are percentages of overall x-axis and y-axis distances that
        determine the width of each cross arm.
        xAxis and yAxis are percentages of overall x-axis and y-axis distances that
        determine the centerline of each cross arm.
        Returns True on success.
        Returns False on failure.
        """
        try:
            xWidth = self.__aecErrorCheck.checkPercentage(xWidth) * vector[0]
            yDepth = self.__aecErrorCheck.checkPercentage(yDepth) * vector[1]
            xAxis = self.__aecErrorCheck.checkPercentage(xAxis) * vector[0]
            yAxis = self.__aecErrorCheck.checkPercentage(yAxis) * vector[1]
            xPoint = (origin[0] + (yAxis - (xWidth * 0.5)), origin[1], origin[2])
            yPoint = (origin[0], origin[1] + (xAxis - (yDepth * 0.5)), origin[2])
            points = self.__aecGeomCalc.getBoxPoints2D(xPoint, (xWidth, vector[1], 0))
            self.addBoundary(points, True)
            points = self.__aecGeomCalc.getBoxPoints2D(yPoint, (vector[0], yDepth, 0))
            self.addBoundary(points)
            self.setHeight(vector[2])
            return True
        except Exception:
            traceback.print_exc()
            return False
    
    def makeCylinder(self, origin = (0, 0, 0), radius = 1, height = 0):

        """
        bool makeCylinder((3D point), number, number)
        Contructs the perimeter as an approximate circle, setting a ratio from
        the delivered  radius to the number of sides and setting the space height.
        Returns True on success.
        Returns False on failure.
        """
        try:
            if radius < 3:
                sides = 3
            else:
                sides = radius
            return self.makePolygon(origin, radius, sides, height)
        except Exception:
            traceback.print_exc()
            return False
        
    def makeH(self, origin = (0, 0, 0), vector = (1, 1, 1),
                    xWidth1 = 0.33333333, xWidth2= 0.33333333, yDepth = 0.33333333):
        """
        bool makeH((3D point), (3D vector), percent, percent, percent)
        Constructs an H-shaped boundary within the box defined by point and vector.
        xWidth1, xWidth2, and yDepth are percentages of overall x-axis and y-axis distances that
        determine the width of each vertical and cross bar, respectively.
        Returns True on success.
        Returns False on failure.        
        """
        try:
            if self.makeCross(origin, vector, xWidth1, yDepth, yAxis = (xWidth1 * 0.5)):
                xPoint = (origin[0] + (vector[0] - xWidth2), origin[1], origin[2])
                points = self.__aecGeomCalc.getBoxPoints2D(xPoint, (xWidth2 * vector[0], vector[1], origin[2]))
                self.addBoundary(points)
                return True
            return False
        except Exception:
            traceback.print_exc()
            return False

    def makeL(self, origin = (0, 0, 0), vector = (1, 1, 1),
                    xWidth = 0.33333333, yDepth = 0.33333333):
        """
        bool makeL((3D point), (3D vector), percent, percent)
        Constructs a L-shaped boundary within the box defined by point and vector.
        xWidth and yDepth are percentages of overall x-axis and y-axis distances 
        that determine the width of each bar.
        Returns True on success.
        Returns False on failure.  
        """
        try:
            return self.makeCross(origin, vector, xWidth, yDepth, xWidth * 0.5, yDepth * 0.5)
        except Exception:
            traceback.print_exc()
            return False

    def makePolygon(self, origin = (0, 0, 0), radius = 1, sides = 3, height = 0):
        """
        bool makePolygon((3D point), number, integer, number)
        Constructs the perimeter as a regular polygon centered on the delivered
        origin point with the first vertex at the maximum y-coordinate. 
        Sets the height of the space.
        Returns True on success.
        Returns False on failure.          
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
            self.setHeight(height)
            return True
        except Exception:
            traceback.print_exc()
            return False

    def makeT(self, origin = (0, 0, 0), vector = (1, 1, 1),
                    xWidth = 0.33333333, yDepth = 0.33333333):
        """
        bool makeT((3D point), (3D vector), percent, percent)
        Constructs a T-shaped boundary within the box defined by point and vector.
        xWidth and yDepth are percentages of overall x-axis and y-axis distances that
        determine the width of the vertical and horizonatl bars, respectively.
        Returns True on success.
        Returns False on failure.
        """
        try:
            return self.makeCross(origin, vector, xWidth, yDepth, xAxis = (1 - (yDepth * 0.5)))
        except Exception:
            traceback.print_exc()
            return False

    def makeU(self, origin = (0, 0, 0), vector = (1, 1, 1),
                    xWidth1 = 0.33333333, xWidth2= 0.33333333, yDepth = 0.33333333):
        """
        bool makeU((3D point), (3D vector), percent, percent, percent)
        xWidth1, xWidth2, and yDepth are percentages of overall x-axis and y-axis distances 
        that determine the width of each vertical and cross bar, respectively.
        Returns True on success.
        Returns False on failure.    
        """
        try:
            if self.makeL(origin, vector, xWidth1, yDepth):
                xWidth = xWidth2 * vector[0]
                xPoint = (origin[0] + (vector[0] - xWidth), origin[1], origin[2])
                points = self.__aecGeomCalc.getBoxPoints2D(xPoint, (xWidth, vector[1], origin[2]))
                self.addBoundary(points)
                return True
            return False
        except Exception:
            traceback.print_exc()
            return False

    def mirror(self, mPoints = None):
        """
        bool mirror([(3D point), (3D point)])
        Mirrors the space orthogonally around the specified line as defined
        by two points, or by default around the major orthogonal axis.
        Returns True on success.
        Returns False on failure.
        """
        try:
            if not self.__properties['boundaryShape']:
                return False            
            if not mPoints:
                mPoints = self.getAxisMajor(points2D = True)
            newPoints = \
            self.__aecGeomCalc.mirrorPoints2D(
                self.getPointsFloor(points2D = True), mPoints)
            self.setBoundary(newPoints)
            return True
        except Exception:
            traceback.print_exc()
            return False

    def move(self, moveBy = (0, 0, 0)):
        """
        bool move((3D vector))
        Moves the space according to the delivered vector.
        Returns True on success.
        Returns False on failure.
        """
        try:
            if not self.__properties['boundaryShape']:
                return False
            boundary = \
                    affine.translate(
                        self.__properties['boundaryShape'],
                        float(moveBy[0]),
                        float(moveBy[1]),
                        0)
            if type(boundary) != shapely.polygon.Polygon:
                return False
            newLevel = self.getLevel() + float(moveBy[2])
            self.setLevel(newLevel)
            self.setBoundary(list(boundary.exterior.coords)[:-1])
            return True
        except Exception:
            traceback.print_exc()
            return False

    def rotate(self, angle = 180, pivot = None):
        """
        bool rotate (float, (2D point))
        Rotates the space counterclockwise around the 2D pivot point 
        by the delivered rotation in degrees.
        If no pivot point is provided, the space will rotate around its centroid.
        Returns True on success.
        Returns False on failure.
        """
        try:
            if not self.__properties['boundaryShape']: return False
            angle = int(angle)
            if not pivot: pivot = self.getCentroid()
            boundary = affine.rotate(self.__properties['boundaryShape'], angle, pivot)
            if type(boundary) != shapely.polygon.Polygon: return False
            return self.setBoundary(boundary.exterior.coords[:-1])
        except Exception:
            traceback.print_exc()
            return False

    def scale(self, scaleBy = (1, 1, 1), scalePoint = None):
        """
        bool scale (3 numbers), (3D point))
        Scales the space by a vector from the delivered point.
        If no point is provided, the space will scale from its centroid.
        Returns True on success.
        Returns False on failure.
        """
        try:
            if not self.__properties['boundaryShape']:  return False                   
            if not scalePoint: scalePoint = self.getCentroid()
            boundary = \
                affine.scale(
                    self.__properties['boundaryShape'],
                    scaleBy[0],
                    scaleBy[1],
                    1,
                    scalePoint)
            if type(boundary) != shapely.polygon.Polygon: return False
            if not self.setBoundary(list(boundary.exterior.coords[:-1])): return False
            self.__properties['height'] *= scaleBy[2]
            return True
        except Exception:
            traceback.print_exc()
            return False

    def setBoundary(self, points = [(0, 0), (1, 0), (1, 1), (0, 1)]):
        """
        bool setPerimeter([(2D point),])
        Creates a new perimeter from the delivered 2D points.
        Colinear points are removed. Fails if a single 
        non-crossing polygon cannot be contructed.
        Returns True on success.
        Returns False on failure.
        """
        try:
            points = self.__aecGeomCalc.rmvColinear(points)
            if len(points) < 3:
                return False            
            boundary = shapely.polygon.orient(shapely.Polygon(points))
            if type(boundary) != shapely.polygon.Polygon:
                return False
            self.__initialize()
            self.__properties['boundaryShape'] = boundary
            return True
        except Exception:
            traceback.print_exc()
            return False

    def setColor(self, newColor = None):
        """
        bool setColor ((int range 0 - 255, int range 0 - 255, int range 0 - 255)
        Sets the Color[R G B] values or without argument randomizes the color.
        Returns True if successful.
        Returns False on failure.        
        """
        try:
            if newColor:
                newColor = list(map(lambda color: int(color) % 256, list(newColor)))
                self.__properties['colorR'] = newColor[0]
                self.__properties['colorG'] = newColor[1]
                self.__properties['colorB'] = newColor[2]
            else:
                self.__properties['colorR'] = random.randint(0, 255)
                self.__properties['colorG'] = random.randint(0, 255)
                self.__properties['colorB'] = random.randint(0, 255)
            return True
        except Exception:
            traceback.print_exc()
            return False

    def setHeight(self, newHeight = 1):
        """
        bool setHeight(number | string)
        Sets the height as a float.
        Returns True if successful.
        Returns False on failure.        
        """
        try:
            self.__properties['height'] = float(newHeight)
            return True
        except Exception:
            traceback.print_exc()
            return False

    def setLevel(self, newLevel = 0):
        """
        bool setLevel(number | string)
        Sets the level as a float.
        Returns True if successful.
        Returns False on failure.
        """
        try:
            self.__properties['level'] = float(newLevel)
            return True
        except Exception:
            traceback.print_exc()
            return False

    def setName(self, newName = ""):
        """
        bool setName(string)
        Sets the Name as a string.
        Returns True if successful.
        Returns False on failure.
        """
        try:
            self.__properties['name'] = str(newName)
            return True
        except Exception:
            traceback.print_exc()
            return False

    def setProperty(self, prpName, value):
        """
        bool setProperty(string, value)
        Directly sets a property its key, bypassing all error checking.
        Intended for use by other components of the aecSpace toolkit.
        Returns True if successful.
        Returns False on failure. 
        """
        try:
            self.__properties[prpName] = value
            return True
        except Exception:
            traceback.print_exc()
            return False        
    
    def setTransparency(self, newTrans = 0):
        """
        bool setTransparency(number | string)
        Sets the transparency as a percentage or without argument sets transparency to 0.
        Converts inputs to a range from 0 to 1.
        Returns True if successful.
        Returns False on failure.
        """
        try:
            newTrans = self.__aecErrorCheck.checkPercentage(newTrans)
            self.__properties['transparency'] = newTrans
            return True
        except Exception:
            traceback.print_exc()
            return False

    def wrap(self, points):
        """
        bool wrap ([(3D point),])
        Sets the boundary of the space to a convex hull 
        derived from the delivered list of points.
        Returns True if successful.
        Returns False on failure.
        """
        try:
            conHull = self.__aecGeomCalc.convexHull(points)
            if conHull:
                self.setBoundary(conHull)
                return True
            return False
        except Exception:
            traceback.print_exc()
            return False

# end class
