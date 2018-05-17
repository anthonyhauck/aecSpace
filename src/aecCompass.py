import traceback

"""
aecColors instantiates a set of color constants in the form of RGB tuples.
"""

class aecCompass:
    
    C = 0
    N = 1
    NNE = 2
    NE = 3
    ENE = 4
    E = 5
    ESE = 6
    SE = 7
    SSE = 8
    S = 9
    SSW = 10
    SW = 11
    WSW = 12
    W = 13
    WNW = 14
    NW = 15
    NNW = 16
    
    
    __type = 'aecCompass' # Type identifier of object instances
    
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
    