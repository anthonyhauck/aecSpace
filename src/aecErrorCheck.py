import traceback

class aecErrorCheck:

    """
    aecErrorCheck contains data validating functions.
    """
    
    __type = 'aecErrorCheck' # Type identifier of object instances
    
    def __init__(self):
        """
        aecErrorCheck Constructor
        """
        pass

    def checkAddress(self, address = (0, 0, 0), bounds = None):
        """
        (int, int, int) checkAddress((int, int, int), (int, int, int))
        Attempts to return a plausible 3 digit address for an item
        with a 3-dimensional matrix. 
        If bounds are supplied as a tuple or list of 3 integers comparisons
        to the corresponding address coordinate are made to ensure the
        address is within or equal to the asserted bounds.
        Returns None on failure.
        """
        try:
            if type(address) != list and type(address) != tuple: return None
            if len(address) < 3: return None 
            address = ([abs(int(x)) for x in list(address)[:3]])
            if not bounds: return tuple(address)
            if type(bounds) != list and type(bounds) != tuple: return None
            if len(bounds) < 3: return None 
            bounds = ([abs(int(x)) for x in list(bounds)[:3]])
            if address[0] > bounds[0]: address[0] = bounds[0]
            if address[1] > bounds[1]: address[1] = bounds[1]
            if address[2] > bounds[2]: address[2] = bounds[2]
            return tuple(address)
        except:
            traceback.print_exc()
            return None        
    
    def checkIndices(self, indices = None, limit = None):
        """
        [int,] checkIndices([number,])
        Attempts to return a list of well-formed integer indices.
        If no indices are delivered, returns a range of integers from zero to limit.
        Absent any arguments, returns [0]
        Returns None on failure.
        """
        try:
            if not indices and not limit: return []
            if not indices and limit: return list(range(0, limit))
            if type(indices) != list: indices = [indices]
            if len(indices) == 0: return None
            indices = [int(index) for index in indices]
            indices.sort()          
            if limit and limit > 0:
                indices.reverse()
                while len(indices) > 0 and indices[0] > limit - 1:
                    indices = indices[1:]
                indices.sort()
            return indices
        except:
            traceback.print_exc()
            return None   
    
    def checkPercentage(self, number = 0):
        """
        float 0 - 1 makePercentage(number)
        Forces a number into the range of 0 to 1 by taking the absolute
        value and dividing a larger number successively by 10.
        Returns None on failure.
        """
        try:         
            number = abs(float(number))
            if number >= 0 and number <= 1:
                return number
            while number > 1:
                number *= 0.1
            return number 
        except:
            traceback.print_exc()
            return None

    def checkPoint(self, testPoint, point2D = False):
        """
        (2D or 3D point) checkPoint((2D or 3D point), bool)
        Returns a well-formed 2D or 3D point from the delivered argument if possible.
        Returns None if unable to form a point as specified.
        """
        try:
            if type(testPoint) != list and type(testPoint) != tuple: return None
            if len(testPoint) < 2: return None
            point = []           
            point.append(float(testPoint[0]))
            point.append(float(testPoint[1]))
            if point2D: return tuple(point)
            if len(testPoint) < 3: return None
            point.append(float(testPoint[2]))
            return tuple(point)
        except:
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
    
# end class    
