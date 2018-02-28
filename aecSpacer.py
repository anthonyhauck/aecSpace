import traceback
from aecSpace import aecSpace
from aecErrorCheck import aecErrorCheck

"""
aecSpacer 
Provides calculation, positioning, and deployment functions for multiple
aecSpace objects.
"""
class aecSpacer:
    
    """
    __aecErrorCheck is an instance of aecErrorCheck.
    """
    __aecErrorCheck = None
       
    def __init__(self):
        """
        aecSpacer Constructor
        Creates a new aecErrorCheck object.
        """
        self.__aecErrorCheck = aecErrorCheck()

    def copy(self, space):
        """
        aecSpace copy(aecSpace)
        Returns a new aecSpace that is a copy of the delivered aecSpace.
        
        """
        newSpace = None
        try:
            newSpace = aecSpace()
            newSpace.setColor(space.getColor256())
            newSpace.setHeight(space.getHeight())
            newSpace.setLevel(space.getLevel())
            newSpace.setPerimeter(space.getPoints2D())
            newSpace.setTransparency(space.getTransparency())
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)            
        return newSpace

    def stacker(self, space, levels = 1, plenum = 0):
        """
        [aecSpaces] stacker(aecSpace, int, float)
        Creates and returns a list of int Spaces stacked upward from the 
        delivered aecSpace by the height of the Space plus additional
        elevation added by the plenum parameter.
        """
        spaces = [space]
        try:
            moveUp = space.getLevel() + space.getHeight() + plenum
            x = 0
            while x < levels:
                newSpace = self.copy(space)
                newSpace.move([0, 0, moveUp])
                spaces.append(newSpace)
                space = newSpace
                x += 1
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)                  
        return spaces
    
    def wrapper(self, points):
        """
        [[float, float],...] wrapper([[float, float],...])
        Computes the convex hull of a set of 2D points returning the list
        of outermost points in counter-clockwise order, starting from the
        vertex with the lexicographically smallest coordinates.
        Implements Andrew's monotone chain algorithm. O(n log n) complexity.
        """
        points = list(map(tuple, points))
        points = sorted(set(points))
        if len(points) <= 1:
            return points
        
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
        
        return lower[:-1] + upper[:-1]

# end class
    
