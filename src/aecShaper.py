import traceback

from aecGeomCalc import aecGeomCalc
from aecSpace import aecSpace
from aecErrorCheck import aecErrorCheck

"""
class aecShaper
Provides a number of utility functions for creating an aecSpace
of a specific topology, using the English alphabet to denote various plan
shapes of the final space.
"""


class aecShaper:
    
    """
    __aecErrorCheck is an instance of aecErrorCheck.
    """
    __aecErrorCheck = None
    __aecGeomCalc = None
       
    def __init__(self):
        """
        aecSpacer Constructor
        Creates a new aecErrorCheck object.
        """
        self.__aecErrorCheck = aecErrorCheck()
        self.__aecGeomCalc = aecGeomCalc()
        
    def makeCross(self, origin = (0, 0, 0), vector = (1, 1, 1), 
                        xWidth = 0.33333333, yDepth = 0.33333333,
                        xAxis = 0.5, yAxis = 0.5):         
        """
        aecSpace makecross((3 numbers), (3 numbers), (2 numbers), percent, percent)
        Constructs a cross-shaped aecSpace within the box defined by point and vector.
        xWidth and yWidth are understood as percentages of overall x-axis and 
        y-axis distances.
        xAxis and yAxis are understood as percentages of overall x-axis and 
        y-axis distances treated as offsets from the x- and y- origin axes.
        
        """
        try:
            xWidth = self.__aecErrorCheck.makePercentage(xWidth) * vector[0]
            yDepth = self.__aecErrorCheck.makePercentage(yDepth) * vector[1]
            xAxis = self.__aecErrorCheck.makePercentage(xAxis) * vector[0]
            yAxis = self.__aecErrorCheck.makePercentage(yAxis) * vector[1]
            xPoint = (origin[0] + (yAxis - (xWidth * 0.5)), origin[1], origin[2])
            yPoint = (origin[0], origin[1] + (xAxis - (yDepth * 0.5)), origin[2])
            space = aecSpace()
            points = self.__aecGeomCalc.getBoxPoints2D(xPoint, (xWidth, vector[1], 0))
            space.addBoundary(points, True)
            points = self.__aecGeomCalc.getBoxPoints2D(yPoint, (vector[0], yDepth, 0))
            space.addBoundary(points)
            return space
        except:
            traceback.print_exc() 
            
    def makeH(self, origin = (0, 0, 0), vector = (1, 1, 1), 
                    xWidth1 = 0.33333333, xWidth2= 0.33333333, yDepth = 0.33333333):
        """
        aecSpace makeH((3 numbers), (3 numbers), (2 numbers), percent, percent, percent)
        Constructs an H-shaped aecSpace within the box defined 
        by point and vector.
        Vertical and horizontal widths are understood as percentages
        of overall x-axis and y-axis distances.        
        """
        try:
            space = self.makeCross(origin, vector, xWidth1, yDepth, yAxis = (xWidth1 * 0.5))
            xPoint = (origin[0] + (vector[0] - xWidth2), origin[1], origin[2])
            points = points = self.__aecGeomCalc.getBoxPoints2D(xPoint, (xWidth2 * vector[0], vector[1], origin[2]))
            space.addBoundary(points)
            return space
        except:
            traceback.print_exc() 
    
    def makeL(self, origin = (0, 0, 0), vector = (1, 1, 1), 
                    xWidth = 0.33333333, yDepth = 0.33333333):         
        """
        aecSpace makeL((3 numbers), (3 numbers), (2 numbers), percent, percent)
        Constructs a new left-handed L-shaped aecSpace within the box defined 
        by point and vector.
        Vertical and horizontal widths are understood as percentages
        of overall x-axis and y-axis distances.
        """
        try:
            return self.makeCross(origin, vector, xWidth, yDepth, xWidth * 0.5, yDepth * 0.5)
        except:
            traceback.print_exc() 
            
    def makeT(self, origin = (0, 0, 0), vector = (1, 1, 1), 
                    xWidth = 0.33333333, yDepth = 0.33333333):         
        """
        aecSpace makeL((3 numbers), (3 numbers), (2 numbers), percent, percent)
        Constructs a new left-handed L-shaped aecSpace within the box defined 
        by point and vector.
        Vertical and horizontal widths are understood as percentages
        of overall x-axis and y-axis distances.
        """
        try:
            return self.makeCross(origin, vector, xWidth, yDepth, xAxis = (1 - (yDepth * 0.5)))
        except:
            traceback.print_exc() 
            
    def makeU(self, origin = (0, 0, 0), vector = (1, 1, 1), 
                    xWidth1 = 0.33333333, xWidth2= 0.33333333, yDepth = 0.33333333):         
        """
        aecSpace makeL((3 numbers), (3 numbers), (2 numbers), percent, percent, percent)
        Constructs a U-shaped aecSpace within the box defined 
        by point and vector.
        Vertical and horizontal widths are understood as percentages
        of overall x-axis and y-axis distances.
        """
        try:
            space = self.makeL(origin, vector, xWidth1, yDepth)
            xWidth = xWidth2 * vector[0]
            xPoint = (origin[0] + (vector[0] - xWidth), origin[1], origin[2])
            points = points = self.__aecGeomCalc.getBoxPoints2D(xPoint, (xWidth, vector[1], origin[2]))
            space.addBoundary(points)
            return space
        except:
            traceback.print_exc() 
    
# end class
