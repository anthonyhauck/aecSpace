import traceback
import uuid

from aecErrorCheck import aecErrorCheck
from aecGeomCalc import aecGeomCalc

class aecGeomCalc:
    
    # utility objects and data shared by all instances.
    
    __aecErrorCheck = aecErrorCheck()   # An instance of aecErrorCheck.
    __aecGeomCalc = aecGeomCalc()       # An instance of aecGeometryCalc
    __type = 'aecGrid'                  # Type identifier of object instances
    
    def __init__(self):
        """
        INTERNAL
        Constructor
        Creates the dictionary of all internal keys and values.
        Sets the ID to a new UUID.
        """
        
        # __properties is a dictionary of all internal variables
        
        self.__properties = \
        {
 
            # The following property values are preserved through a call to __initialize.

            'ID' : None,      # A UUID
            'name' : "",      # A custom string designation.     

            # The following properties are reset by __invalidate()

            'area' : None,    # Aggregate area of all cells
            'volume' : None,  # Aggregate volume of all cells
            'cells' : [],     # List of cells managed by this instance.            

        } # end dictionary

        self.__properties['ID'] = uuid.uuid4()
    
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