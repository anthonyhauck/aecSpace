import traceback
from aecSpace import aecSpace
from aecErrorCheck import aecErrorCheck

"""
class aecSpacer 
Provides calculation, positioning, and deployment 
functions for multiple aecSpace objects.
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

    def copy(self, space, moveBy = (0, 0, 0)):
        """
        aecSpace copy(aecSpace)
        Returns a new aecSpace that is a copy of the delivered aecSpace.     
        """
        try:
            newSpace = aecSpace()
            newSpace.setColor(space.getColor256())
            newSpace.setHeight(space.getHeight())
            newSpace.setLevel(space.getLevel())
            newSpace.setBoundary(space.getPointsExterior2D())
            newSpace.setTransparency(space.getTransparency())
            newSpace.move(moveBy)
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)            
        return newSpace   
    
    def place(self, space, places = 1, moveBy = (0, 0, 0)):
        """
        [aecSpace,...] place(aecSpace, int, (number, number, number))
        Creates and returns a list of aecSpaces placed along a vector 
        from the delivered aecSpace by the moveBy vector.
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
        [aecSpace,...] row(aecSpace, number, number, bool)
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
        [aecSpace,...] stacker(aecSpace, int, number)
        Creates and returns a list of aecSpaces stacked upward from the 
        delivered aecSpace by the height of the aecSpace plus additional
        elevation added by the plenum parameter.
        """
        try:
            stackBy = space.getLevel() + space.getHeight() + plenum
            spaces = self.place(space, levels, [0, 0, stackBy])
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)                  
        return spaces

# end class
    
