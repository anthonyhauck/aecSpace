import traceback

class aecValid:

    """
    aecErrorCheck contains data validating functions.
    """
        
    def __init__(self):
        """
        aecErrorCheck Constructor
        """
        pass

    def address(self, address = (0, 0, 0), bounds = None):
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
    
    def angle(self, angle):
        """
        float checkAngle(number)
        Attempts to return a well-formed float angle between 0 and 360.
        Returns None on failure.
        """
        try:
            if type(angle) != int and \
               type(angle) != float and \
               type(angle) != str: return None
            if type(angle) == str: angle = float(angle)
            return abs(angle % 360)
        except:
            traceback.print_exc()
            return None
    
    def color(self, color):
        """
        (int, int, int) checkColor(int, int, int)
        Attempts to return a well-formed tuple of 3 ints representing RGB values from 0 to 255.
        Returns None if unable to form a color as specified.
        """
        try:
            if type(color) != list and type(color) != tuple: return None
            if len(color) < 2: return None
            color = [int(x % 255) for x in list(color)]
            return color
        except:
            traceback.print_exc()
            return None

    def indices(self, indices = None, limit = None):
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
    
    def percent(self, number: float = 0.0):
        """
        float 0 - 1 makePercentage(number)
        Forces a number into the range of 0 to 1 by taking the absolute
        value and dividing a larger number successively by 10.
        Returns None on failure.
        """
        try:         
            number = abs(float(number))
            if number >= 0 and number <= 1: return number
            while number > 1: number *= 0.1
            return number 
        except:
            traceback.print_exc()
            return None
    
# end class    
