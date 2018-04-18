import traceback

class aecErrorCheck:

    """
    aecErrorCheck contains data validating functions.
    """
    
    def __init__(self):
        """
        aecErrorCheck Constructor
        """
        pass

    def checkIndices(self, indices = None, limit = None):
        """
        [int,] checkIndices([number,])
        Attempts to return a list of well-formed integer indices.
        If no indices are delivered, returns a range of integers from zero to limit.
        Absent any arguments, returns [0]
        Returns None on failure.
        """
        try:
            if not indices and not limit:
                return []
            if not indices and limit:
                return list(range(0, limit))
            if type(indices) != list:
                indices = [indices]
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
    
# end class    
