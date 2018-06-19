import traceback

from random import uniform
from shapely import geometry as shapely
from typing import List

from .aecGeometry import aecGeometry
from .aecPoint import aecPoint
from .aecSpace import aecSpace

"""
class aecSpacer
Provides calculation, positioning, and deployment
functions for multiple aecSpace objects.
"""
class aecSpacer:

    __aecGeometry = aecGeometry()

    def __init__(self):
        """
        aecSpacer Constructor
        """
        pass

    def copy(self, space: aecSpace, x: float = 0, y: float = 0, z: float = 0) -> aecSpace:
        """
        Returns a new aecSpace that is a copy of the delivered aecSpace.
        The copy will be moved by the delivered x, y, and z displacements.
        Returns None on failure.
        """
        try:
            spcProps = space.copy_properties
            newSpace = aecSpace()
            newSpace.boundary = spcProps['boundary']            
            newSpace.color = spcProps['color']
            newSpace.height = spcProps['height']
            newSpace.level = spcProps['level']
            newSpace.name = spcProps['name']
            newSpace.moveBy(x, y, z)
            return newSpace
        except Exception:
            traceback.print_exc() 
            return None

    def place(self, space: aecSpace, copies: int = 1, 
                    x: float = 0, y: float = 0, z: float = 0) -> bool:
        """
        Creates and returns a list of aecSpaces placed along the delivered xyz displacements.
        Returned list does not include the delivered aecSpace.
        Returns None on failure.
        """
        try:
            spaces = []
            index = 0
            while index < copies:
                newSpace = self.copy(space, x, y, z)
                spaces += [newSpace]
                space = newSpace
                index += 1
            return spaces
        except Exception:
            traceback.print_exc()
            return None

    def placeOnLine(self, shape: aecSpace, border: aecSpace, orient: List[int]):
        """
        Attempts to place one aecSpace (shape) withn the boundary of
        another (border) at a random interior point along a specified line
        from the center of the boundary to the specified compass point on
        the boundary.
        Returns True on success.
        Returns False on failure.        
        """
        try:
            if shape.area > border.area: return False
            tstShape = self.copy(shape)
            for direction in orient:
                comLine = border.compassLine(direction)
                level = border.level
                within = False
                x = 0
                while not within and x < 100:
                    vector = shapely.LineString([comLine[0].xy, comLine[1].xy])
                    posit = uniform(0, 100)
                    point = vector.interpolate(posit, normalized = True)
                    point = aecPoint(point.x, point.y, level)
                    tstShape.moveTo(tstShape.centroid_floor, point)
                    within = border.containsShape(tstShape.points_floor)
                    x += 1
                if within: 
                    shape.moveTo(shape.centroid_floor, point)
                    return True
            return False
        except Exception:
            traceback.print_exc()
            return False        

    def placeWithin(self, shape: aecSpace, border: aecSpace) -> bool:
        """
        Attempts to place one aecSpace (shape) within the boundary 
        of another (border) at a random interior point.
        Returns True on success.
        Returns False on failure.
        """
        try:
            if shape.area > border.area: return False
            level = border.level
            xAxis = border.axis_x
            yAxis = border.axis_y        
            lowX = xAxis[0].x
            topX = xAxis[1].x
            lowY = yAxis[0].y
            topY = yAxis[1].y
            within = False
            x = 0
            tstShape = self.copy(shape)
            while not within and x < 100:
                xCoord = uniform(lowX, topX)
                yCoord = uniform(lowY, topY)
                bndPnt = aecPoint(xCoord, yCoord, level)
                tstShape.moveTo(tstShape.centroid_floor, bndPnt)
                within = border.boundary.contains(tstShape.boundary)
                x += 1
            if not within: return False
            shape.moveTo(shape.centroid_floor, bndPnt)
            return True
        except Exception:
            traceback.print_exc()
            return False

    def row(self, space: aecSpace, copies: int = 1, 
                  gap: float = 0, xAxis: bool = True) -> List[aecSpace]:
        """
        Creates and returns a list of aecSpaces placed along the x-axis from the delivered
        aecSpace by the bounding box width plus the distance added by the gap parameter.
        By default places new spaces along the positive x-axis from the position of the
        delivered aecSpace, or if xAxis is false, along the positive y-axis.
        Returned list does not include the delivered aecSpace.
        Returns None on failure.
        """
        try:
            if xAxis: return self.place(space, copies, x = space.size_x + gap)
            return self.place(space, copies, y = space.size_y + gap)
        except Exception:
            traceback.print_exc()
            return None

    def stack(self, space: aecSpace, copies: int = 1, plenum: float = 0) -> List[aecSpace]:
        """
        Creates and returns a list of aecSpaces stacked upward from the
        delivered aecSpace by the height of the aecSpace plus additional
        elevation added by the plenum parameter.
        Returned list does not include the delivered aecSpace.
        Returns None on failure.
        """
        try:
            return self.place(space, copies, z = space.height + plenum)
        except Exception:
            traceback.print_exc()
            return None

    def stackToArea(self, space, area, plenum = 0):
        """
        [aecSpace,] buildToArea(aecSpace, number, number)
        Compares the area of the delivered aecSpace to the target area and stacks
        identical spaces from the original space until the target area is met or
        exceeded, returning a list of resulting aecSpaces.
        Returned list does not include the delivered aecSpace.
        Returns None on failure.
        """
        try:
            spcArea = space.area
            if spcArea >= area: return []
            copies = int(area / spcArea)
            return self.stack(space, copies, plenum)
        except Exception:
            traceback.print_exc()
            return None
