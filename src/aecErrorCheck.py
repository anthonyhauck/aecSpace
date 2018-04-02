import traceback

class aecErrorCheck:

    """
    aecErrorCheck contains data validating functions.
    """
    
    def __init__(self):
        """
        aecErrorCheck Constructor
        Passes for now, no setup required.
        """
        pass

    def checkPoint(self, testPoint, point3D = True):
        """
        checkPoint confirms that the delivered variable is a valid 
        2D or 3D point, and attempts to convert alternate types to
        create a well-formed point.
        """
        try:
            point = []
            point.append(float(testPoint[0]))
            point.append(float(testPoint[1]))
            if point3D:
                point.append(float(testPoint[2]))
            return tuple(point)
        except:
            traceback.print_exc()                

    def makePercentage(self, number = 0):
        """
        float 0 - 1 makePercentage(number)
        Forces a number into the range of 0 to 1 by taking the absolute
        value and dividing a larger number successively by 10.
        """
        try:         
            number = abs(number)
            if number >= 0 and number <= 1:
                return number
            while number > 1:
                number *= 0.1
            return number 
        except:
            traceback.print_exc() 
    
# end class    
