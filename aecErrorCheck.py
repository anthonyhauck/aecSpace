import traceback

class aecErrorCheck:

# -------------------------------------------------------------------------    
# aecErrorCheck Constructor
# -------------------------------------------------------------------------    
    
    def __init__(self):
        pass
    # end constructor    

# -------------------------------------------------------------------------    
# errorMessage(string, string) 
# Prints an error message specific to the calling function.
# -------------------------------------------------------------------------
    
    def errorMessage(self, className = "", tracer = None):
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

# -------------------------------------------------------------------------    
# [number, number,] inRange([number, number], [number, number,]) 
# Forces the delivered numbers into the range described by the list.
# -------------------------------------------------------------------------

    def inRange(self, ranger = [0, 1], numbers = [0]):
        newNumbers = []
        try:         
            for number in numbers:
                number = float(number)
                if number < ranger[0]:
                    number = ranger[0]
                elif number > ranger[1]:
                    number = ranger[1]
                newNumbers.append(number)
            return newNumbers
        except:
            return self.errorMessage(self.__class__.__name__, traceback)
    
# -------------------------------------------------------------------------    
# [number, number,] isPoint([number, number,], bool) 
# Detects whether a list is 2 or 3 numbers and
# corrects constructs the specified 2D or 3D point.
# -------------------------------------------------------------------------

    def isPoint(self, coords = [0, 0]):
        newCoords = []
        try:
            if len(coords) > 1:        
                newCoords.append(float(coords[0]))
                newCoords.append(float(coords[1]))
            if len(coords) > 2:  
                newCoords.append(float(coords[2]))
        except:
            return self.errorMessage(self.__class__.__name__, traceback)
        return newCoords
    
# end class    
