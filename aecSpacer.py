import traceback
from aecSpace import aecSpace
from aecErrorCheck import aecErrorCheck

# -------------------------------------------------------------------------   
# Spacer 
# Provides Space positioning and deployment utilities.
# -------------------------------------------------------------------------   


class aecSpacer:
    
    # __aecErrorCheck is an instance of aecErrorCheck
    
    __aecErrorCheck = None
    
# -------------------------------------------------------------------------    
# aecSpacer Constructor
# -------------------------------------------------------------------------    
    
    def __init__(self):
        self.__aecErrorCheck = aecErrorCheck()

# -------------------------------------------------------------------------
# copy(Space)
#
# Returns a new Space that is a copy of the delivered space.
# -------------------------------------------------------------------------
    
    def copy(self, space):
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

    
# -------------------------------------------------------------------------
# stacker(Space, int, float)
#
# Stacker creates returns a list of int Spaces stacked upward from the delivered Space
# by the height of the Space plus additional elevation added by the plenum parameter
# -------------------------------------------------------------------------   

    def stacker(self, space, levels = 1, plenum = 0):
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

# end class
    
