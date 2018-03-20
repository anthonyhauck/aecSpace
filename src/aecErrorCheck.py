import traceback

class aecErrorCheck:

    """
    aecErrorCheck contains both validating functions
    and an error message builder for debugging.
    """
    
    def __init__(self):
        """
        aecErrorCheck Constructor
        Passes for now, no setup required.
        """
        pass

    def errorMessage(self, className = "", tracer = None):
        """
        bool errorMessage(string, traceback)
        Builds an error message from the delivered traceback
        and prints the error message identifying the triggering
        line and the governing class.
        """
        className = "\nClass | " + className 
        traceError = tracer.format_exc()
        traceError = "\n" + traceError.split("\n")[-2]
        stack = tracer.extract_stack()
        message = tracer.format_list(stack)[-3].strip()    
        messageList = message.split("\n")
        fileList = messageList[0].split(" ")
        fileName = fileList[1].split(",")[0]
        fileName = "\n" + fileName[1:-1]
        fileLine = fileList[2] + " " + fileList[3]
        fileLine = fileLine.split(",")[0] + ": "
        message = "\n" + fileLine.capitalize() + messageList[1].strip()
        message = traceError + fileName + message + className
        print(message)
        return False     

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
            return self.errorMessage(self.__class__.__name__, traceback)
    
    def isPoint(self, coords = [0, 0]):
        """
        [number, number,] isPoint([number | string, number| string,...])
        Constructs a 2D or 3D point from a valid alphanumeric list or
        returns False if unable to.
        """
        newCoords = []
        try:
            if len(coords) < 2:
                return False
            newCoords.append(float(coords[0]))
            newCoords.append(float(coords[1]))
            if len(coords) > 2:  
                newCoords.append(float(coords[2]))
        except:
            return self.errorMessage(self.__class__.__name__, traceback)
        return newCoords
    
# end class    
