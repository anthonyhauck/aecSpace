import traceback
import uuid

from aecErrorCheck import aecErrorCheck
from aecGeomCalc import aecGeomCalc

class aecSpaceGroup:
    """
    class aecSpaceGroup
    Manages multiple aecSpace instances as a single object, 
    enabling collective editing and reporting.
    """
    #__retain is a shared list of self.__property keys of
    # values to be retained through a call to __initialize.

    __retain = \
    (
        'ID',
        'name',
        'spaces'
    )
    
    # utility objects shared by all instances of aecSpaceGroup
    
    __aecErrorCheck = aecErrorCheck()   # An instance of aecErrorCheck.
    __aecGeomCalc = aecGeomCalc()       # An instance of aecGeometryCalc    
   
    def __init__(self):
        """
        INTERNAL
        aecSpaceGroup Constructor
        Creates the dictionary of all internal keys and values.
        Sets the ID to a new UUID.
        """
        
        # __properties is a dictionary of all aecSpaceGroup variables
        
        self.__properties = \
        {
 
            # The following property values are preserved through a call to __initialize.

            'ID' : None,      # A UUID
            'name' : "",      # A custom string designation.
            'spaces' : [],    # List of the aecSpace instances managed by this instance.            

            # The following properties are reset by __invalidate()

            'area' : None,    # Aggregate area of all aecSpaces
            'volume' : None,  # Aggregate volume of all aecSpaces

        } # end dictionary

        self.__properties['ID'] = uuid.uuid4()
        
    def __initialize(self):
        """
        INTERNAL
        __initialize()
        Resets specific internal variables to NONE
        to ensure on-demand recompute.
        """
        for key in self.__properties:
            if not key in self.__retain:
                self.__properties[key] = None
    
    def __sortByLevel(self):
        """
        INTERNAL
        bool __sortByLevel()
        Sorts all aecSpaces by their level, lowest to highest.
        Returns True on success.
        Returns False on failure.
        """
        try:
            if self.__properties['spaces']:
                self.__properties['spaces'].sort(key = lambda x: x.getLevel())
        except Exception:
            traceback.print_exc()
            return False         
    
    def addSpaces(self, spaces):
        """
        bool addSpaces([aecSpace,])
        Appends a list of aecSpaces to the spaces list.
        Returns True on success.
        Returns False on failure.
        """
        try:
            if type(spaces) != list:
                spaces = [spaces]
            for space in spaces:
                if space.getType() != 'aecSpace': continue
                self.__properties['spaces'].append(space)
            self.__sortByLevel()
            self.__initialize()
            return True
        except Exception:
            traceback.print_exc()
            return False
        
    def clearSpaces(self):
        """
        bool clearSpaces()
        Resets the aecSpace list to an empty list and initializes the instance.
        Returns True on success.
        Returns False on failure.
        """
        try:
            self.__properties['spaces'] = []
            self.__initialize()
        except Exception:
            traceback.print_exc()
            return False

    def deleteSpaces(self, indices):
        """
        bool delSpaces([int,])
        Deletes the spaces at the specified indices of the current list of aecSpaces.
        Returns True on success.
        Returns False if the spaces list is empty or on other failure.
        """
        try:
            spaces = self.getSpaces()
            if len(spaces) == 0: return False
            indices = self.__aecErrorCheck.checkIndices(indices, len(spaces))            
            for index in indices:
                if spaces[index]:
                    spaces[index] = None
                    del spaces[index]
            self.__properties['spaces'] = spaces
            self.__sortByLevel()
            self.__initialize()
            return True
        except Exception:
            traceback.print_exc()
            return False
   
    def getArea(self):
        """
        float getArea()
        Returns the aggregate area of the floors of all aecSpaces.
        Returns None on failure.
        """
        try:
            if not self.__properties['area']:
                area = 0
                for space in self.__properties['spaces']:
                    area += space.getArea()                
                self.__properties['area'] = area
            return self.__properties['area']
        except Exception:
            traceback.print_exc()
            return None
        
    def getCount(self):
        """
        float getCount()
        Returns the quantity of spaces in the spaces list.
        Returns None on failure.
        """
        try:
            if type(self.__properties['spaces']) != list:
                self.__properties['spaces'] = []
            return len(self.__properties['spaces'])
        except Exception:
            traceback.print_exc()
            return None        
    
    def getProperties(self):
        """
        dictionary getProperties()
        Returns the properties dictionary.
        Intended for use by other components of the aecSpace toolkit.
        Returns None on failure.        
        """
        try:
            return self.__properties
        except Exception:
            traceback.print_exc()
            return None    
        
    def getSpaces(self):
        """
        [aecSpace,] getSpaces()
        Returns the list of aecSpaces.
        Returns None on failure.
        """
        try:
            if type(self.__properties['spaces']) != list:
                self.__properties['spaces'] = []            
            return self.__properties['spaces']
        except Exception:
            traceback.print_exc()
            return None 

    def getVolume(self):
        """
        float getVolume()
        Returns the aggregate volume of all aecSpaces.
        Returns None on failure.
        """
        try:
            if not self.__properties['volume']:
                volume = 0
                for space in self.__properties['spaces']:
                    volume += space.getVolume()                
                self.__properties['volume'] = volume
            return self.__properties['volume']
        except Exception:
            traceback.print_exc()
            return None             

    def move(self, moveBy = (1, 1, 1), indices = None):
        """
        bool scale (3D vector), (int,])
        Moves each aecSpace listed by index in indices by the delivered vector.
        Affects all aecSpaces if no indices are delivered.
        Returns True on success.
        Returns False if the spaces list is empty or on other failure.
        """
        try:
            spaces = self.getSpaces()
            if len(spaces) == 0: return False
            indices = self.__aecErrorCheck.checkIndices(indices, len(spaces))
            for index in indices:
                spaces[index].move(moveBy)
            return True
        except Exception:
            traceback.print_exc()
            return False

    def rotate(self, angle = 180, pivot = None, indices = None):
        """
        bool rotate (float, (2D point), (int,))
        Rotates each aecSpace listed by index in indices counterclockwise around the 
        2D pivot point by the delivered rotation in degrees.
        Affects all aecSpaces if no indices are delivered.
        If no pivot point is provided, each indicated 
        aecSpace will be rotated around its centroid.
        Returns True on success.
        Returns False if the spaces list is empty or on other failure.
        """
        try:
            spaces = self.getSpaces()
            if len(spaces) == 0: return False
            indices = self.__aecErrorCheck.checkIndices(indices, len(spaces))
            for index in indices:
                spaces[index].rotate(angle, pivot)
            return True
        except Exception:
            traceback.print_exc()
            return False

    def scale(self, scaleBy = (1, 1, 1), scalePoint = None, indices = None):
        """
        bool scale (3D vector), (3D point), (int,))
        Scales each aecSpace listed by index in indices by a vector from the delivered point.
        Affects all aecSpaces if no indices are delivered.
        If no pivot scale point is provided, each indicated  
        aecSpace will be scaled from its centroid.
        Returns True on success.
        Returns False if the spaces list is empty or on other failure.
        """
        try:
            spaces = self.getSpaces()
            if len(spaces) == 0: return False
            indices = self.__aecErrorCheck.checkIndices(indices, len(spaces))
            for index in indices:
                spaces[index].scale(scaleBy, scalePoint)
            return True
        except Exception:
            traceback.print_exc()
            return False
    
    def setColor(self, newColor = None, indices = None):
        """
        bool setColor (int range 0 - 255, int range 0 - 255, int range 0 - 255)
        Sets the color[R G B] values of each aecSpace listed by index in indices
        or without argument randomizes the color.
        Affects all aecSpaces if no indices are delivered.        
        Returns True on success.
        Returns False if the spaces list is empty or on other failure.
        """
        try:
            spaces = self.getSpaces()
            if len(spaces) == 0: return False
            indices = self.__aecErrorCheck.checkIndices(indices, len(spaces))
            for index in indices:
                spaces[index].setColor(newColor) 
            return True
        except Exception:
            traceback.print_exc()
            return False

    def setHeight(self, height = 1, indices = None):
        """
        bool setHeight(number | string, (int,))
        Sets the height as a float for each aecSpace listed by index in indices.
        Affects all aecSpaces if no indices are delivered.     
        Returns True on success.
        Returns False if the spaces list is empty or on other failure.
        """
        try:
            spaces = self.getSpaces()
            if len(spaces) == 0: return False
            indices = self.__aecErrorCheck.checkIndices(indices, len(spaces))
            for index in indices:
                spaces[index].setHeight(height)
            return True
        except Exception:
            traceback.print_exc()
            return False

    def setLevel(self, level = 0, indices = None):
        """
        bool setLevel(number | string)
        Sets the level as a float for each aecSpace listed by index in indices.
        Affects all aecSpaces if no indices are delivered.
        Returns True on success.
        Returns False if the spaces list is empty or on other failure.       
        """
        try:
            spaces = self.getSpaces()
            if len(spaces) == 0: return False            
            indices = self.__aecErrorCheck.checkIndices(indices, len(spaces))
            for index in indices:
                spaces[index].setLevel(level)
            return True
        except Exception:
            traceback.print_exc()
            return False

    def setName(self, newName = ""):
        """
        bool setName(string)
        Sets the Name of the aecGroup as a string.
        Returns True on success.
        Returns False if the spaces list is empty or on other failure.
        """
        try:
            self.__properties['name'] = str(newName)
            return True
        except Exception:
            traceback.print_exc()
            return False
        
    def setNames(self, newName = "", indices = None):
        """
        bool setName(string)
        Sets the name of each aecSpace listed by index in indices.
        Affects all aecSpaces if no indices are delivered.
        Returns True on success.
        Returns False if the spaces list is empty or on other failure.        
        """
        try:
            spaces = self.getSpaces()
            if len(spaces) == 0: return False
            indices = self.__aecErrorCheck.checkIndices(indices, len(spaces))
            for index in indices:
                spaces[index].setName(newName)
            return True
        except Exception:
            traceback.print_exc()
            return False        

    def setTransparency(self, transparency = 0, indices = []):
        """
        bool setTransparency(number | string)
        Sets the transparency percentage or without argument sets Transparency to 0 for
        each aecSpace listed by index in indices.
        Converts inputs to a range from 0 to 1.        
        Affects all aecSpaces if no indices are delivered.        
        Returns True on success.
        Returns False if the spaces list is empty or on other failure.       
        """
        try:
            spaces = self.getSpaces()
            if len(spaces) == 0: return False
            indices = self.__aecErrorCheck.checkIndices(indices, len(spaces))
            for index in indices:
                spaces[index].setTransparency(transparency)
            return True
        except Exception:
            traceback.print_exc()
            return False

    def wrap(self, points, indices = None):
        """
        bool wrap ([(3D point),*3+])
        Sets the boundary of each aecSpace listed by index in indices 
        to a convex hull derived from the delivered list of points.
        Affects all aecSpaces if no indices are delivered.        
        Returns True on success.
        Returns False if the spaces list is empty or on other failure.      
        """
        try:
            conHull = self.__aecGeomCalc.convexHull(points)
            if not conHull: return False
            spaces = self.getSpaces()
            if len(spaces) == 0: return False
            indices = self.__aecErrorCheck.checkIndices(indices, len(spaces))
            for index in indices:
                spaces[index].wrap(points)                        
            return True
        except Exception:
            traceback.print_exc()
            return False
        
# end class
    