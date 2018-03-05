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
        
    def column(self, space, places = 1, gap = 0, plus = True):
        """
        [aecSpace,...] column(aecSpace, int, float, bool)
        Creates and returns a list of aecSpaces placed along the Y-axis 
        from the delivered aecSpace by the bounding box depth plus the
        distance added by the gap parameter. Defaults to placement along
        the positive axis from the position of the delivered aecSpace,
        or negative if the plus boolean is False.
        """
        try:
            posBy = space.getBoxYsize() + gap
            if not plus:
                posBy = posBy - (posBy * 2)
            moveBy = [0, posBy, 0]
            return self.place(space, places, moveBy)           
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)

    def copy(self, space, moveBy = [0, 0, 0]):
        """
        aecSpace copy(aecSpace)
        Returns a new aecSpace that is a copy of the delivered aecSpace.     
        """
        try:
            newSpace = aecSpace()
            newSpace.setColor(space.getColor256())
            newSpace.setHeight(space.getHeight())
            newSpace.setLevel(space.getLevel())
            newSpace.setBoundary(space.getPoints2D())
            newSpace.setTransparency(space.getTransparency())
            newSpace.move(moveBy)
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)            
        return newSpace
       
    def place(self, space, places = 1, moveBy = [0, 0, 0]):
        """
        [aecSpace,...] place(aecSpace, int, [float, float, float])
        Creates and returns a list of Spaces placed along a vector 
        from the delivered aecSpace by.
        """
        spaces = [space]
        try:
            x = 0
            while x < places:
                newSpace = self.copy(space, moveBy)
                spaces.append(newSpace)
                space = newSpace
                x += 1            
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)                  
        return spaces            

    def row(self, space, places = 1, gap = 0, plus = True):
        """
        [aecSpace,...] row(aecSpace, int, float, bool)
        Creates and returns a list of aecSpaces placed along the X-axis 
        from the delivered aecSpace by the bounding box width plus the
        distance added by the gap parameter. Defaults to placement along
        the positive axis from the position of the delivered aecSpace,
        or negative if plus boolean is False.
        """
        try:
            posBy = space.getBoxXsize() + gap
            if not plus:
                posBy = posBy - (posBy * 2)
            moveBy = [posBy, 0, 0]
            return self.place(space, places, moveBy)           
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)
    
    def stack(self, space, levels = 1, plenum = 0):
        """
        [aecSpace,...] stacker(aecSpace, int, float)
        Creates and returns a list of aecSpaces stacked upward from the 
        delivered aecSpace by the height of the Space plus additional
        elevation added by the plenum parameter.
        """
        try:
            stackBy = space.getLevel() + space.getHeight() + plenum
            spaces = self.place(space, levels, [0, 0, stackBy])
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)                  
        return spaces
    
    def wrap(self, points):
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
    
