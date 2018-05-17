import traceback

"""
aecColors instantiates a set of color constants in the form of RGB tuples.
"""

class aecColors:
    
    aqua = (77, 184, 100)
    blue = (50, 166, 255)
    stone = (20, 20, 20)
    gray = (64, 64, 64)
    granite = (60, 60, 60)
    green = (76, 205, 0)
    orange = (255, 115, 15) 
    purple = (191, 2, 255)
    pink = (255, 66, 138)
    red = (255, 0, 0)
    sand = (255, 215, 96)
    white = (255, 255, 255)
    yellow = (255, 239, 17)
    
    __type = 'aecColors' # Type identifier of object instances
    
    def __init__(self):
        """
        aecColors Constructor
        Passes for now, no setup required.
        """
        pass

    def getType(self):
        """
        string getType()
        Returns a string constant to identify the object type.
        Returns None on failure.
        """
        try:
            return self.__type
        except Exception:
            traceback.print_exc()
            return None    
    
    
# end class
    