import traceback

from typing import List, Tuple
from uuid import uuid4

from .aecColor import aecColor
from .aecGeometry import aecGeometry
from .aecPoint import aecPoint
from .aecSpace import aecSpace

class aecSpaceGroup:
    """
    Manages multiple aecSpace instances as a single object, 
    enabling collective editing and reporting.
    """

    __slots__ = ['__aecGeometry', '__ID', '__name', '__spaces']
      
    def __init__(self, x:float = 0, y:float = 0, z:float = 0):
        """
        Constructor defaults to origin point coordinates.
        """
        self.__aecGeometry = aecGeometry()
        self.__ID = str(uuid4())
        self.__name = ''
        self.__spaces = []
        
    @property
    def area(self) -> float:
        """
        Returns the total area of all spaces.
        Return None on failure.
        """
        try:
            space_area = 0
            for space in self.__spaces: space_area += space.area
            return space_area
        except Exception:
            traceback.print_exc()
            return None   
    
    @property
    def by_level(self) -> List[aecSpace]:
        """
        INTERNAL
        bool __sortByLevel()
        Returns a list of all spaces by their level, lowest to highest.
        """
        try:
            return self.__spaces.sort(key = lambda space: space.level)
        except Exception:
            traceback.print_exc()
            return False     

    @property
    def count(self) -> float:
        """
        Returns the count of spaces.
        Return None on failure.
        """
        try:
            return len(self.__spaces)
        except Exception:
            traceback.print_exc()
            return None   
        
    @property
    def indices(self) -> List[int]:
        """
        Returns a list of all indices.
        Returns None on failure.
        """
        try:
            return list(range(0, len(self.__spaces)))
        except Exception:
            traceback.print_exc()
            return None    

    @property
    def name(self) -> str:
        """
        Property
        Returns the name.
        Returns None on failure.
        """
        try:
            return self.__name
        except Exception:
            traceback.print_exc() 
            return None

    @name.setter
    def name(self, value: str):
        """
        Property
        Sets the name.
        """
        try:
            name = self.__name
            self.__name = str(value)
        except Exception:
            self.__name = name
            traceback.print_exc() 

    @property
    def spaces(self) -> List[aecSpace]:
        """
        Returns the list of aecSpaces.
        Returns None on failure.
        """
        try:
            return self.__spaces
        except Exception:
            traceback.print_exc()
            return None 
        
    @spaces.setter
    def spaces(self, value: List[aecSpace]):
        """
        Returns the list of aecSpaces.
        Returns None on failure.
        """
        try:
            preSpaces = self.__spaces
            self.__spaces = value
        except Exception:
            self.__spaces = preSpaces
            traceback.print_exc()
    
    @property
    def volume(self):
        """
        Returns the aggregate volume of all spaces.
        Returns None on failure.
        """
        try:
            space_volume = 0
            for space in self.__spaces: space_volume += space.volume
            return space_volume
        except Exception:
            traceback.print_exc()
            return None    
        
    def add(self, spaces: List[aecSpace]) -> bool:
        """
        Appends a list of aecSpaces to the spaces list.
        Returns True on success.
        Returns False on failure.
        """
        try:
            for space in spaces: self.__spaces.append(space)
            return True
        except Exception:
            traceback.print_exc()
            return False
        
    def clear(self) -> bool:
        """
        Sets the space list to an empty list.
        Returns True on success.
        Returns False on failure.
        """
        try:
            self.__spaces = []
            return True
        except Exception:
            traceback.print_exc()
            return False    
        
    def delete(self, index):
        """
        Deletes the space at the specified index of the current list of spaces.
        Returns True on success.
        Returns False if the spaces list is empty or on other failure.
        """
        try:
            index = int(index)
            spaces = self.spaces()
            if index > len(spaces) or index < 0 - 1: return False
            del spaces[index]
            self.__spaces = spaces
            return True
        except Exception:
            traceback.print_exc()
            return False
        
    def moveBy(self, x: float = 0, y: float = 0, z: float = 0, index: int = None) -> bool:
        """
        Moves the spaces by the delivered x, y, and z displacements.
        Returns True on success.
        Returns False on failure.
        """
        try:
            if index:
                index = int(index)
                spaces = self.spaces()
                if index > len(spaces) or index < 0 - 1: return False
                self.__spaces[index].moveBy(x, y, z)
            else:
                for space in self.__spaces: space.moveBy(x, y, z)
            return True
        except Exception:
            traceback.print_exc()
            return False  

    def moveTo(self, fromPnt: aecPoint, toPnt: aecPoint, index: int = None) -> bool:
        """
        Moves the spaces by constructing a vector between the "from" and "to" points.
        Returns True on success.
        Returns False on failure.
        """        
        try:
            if index:
                index = int(index)
                spaces = self.spaces()
                if index > len(spaces) or index < 0 - 1: return False
                self.__spaces[index].moveTo(fromPnt, toPnt)
            else:
                for space in self.__spaces: space.moveTo(fromPnt, toPnt)
            return True
        except Exception:
            traceback.print_exc()
            return False          

    def rotate(self, angle: float, point: aecPoint = None, index: int = None) -> bool:
        """
        Rotates the space by the delivered angle in degrees.
        If no point is provided, the space will scale from its centroid.
        Returns True on success.
        Returns False on failure.
        """     
        try:
            if index:
                index = int(index)
                spaces = self.spaces()
                if index > len(spaces) or index < 0 - 1: return False
                self.__spaces[index].rotate(angle, point)
            else:
                for space in self.__spaces: space.rotate(angle, point)
            return True
        except Exception:
            traceback.print_exc()
            return False                 

    def scale(self, x: float = 1, y: float = 1, z: float = 1, 
                    point: aecPoint = None, index: int = None) -> bool:
        """
        Scales the space by the delivered x, y, and z factors.
        If no point is provided, the space will scale from its centroid.
        Returns True on success.
        Returns False on failure.
        """
        try:
            if index:
                index = int(index)
                spaces = self.spaces
                if index > len(spaces) - 1 or index < 0: return False
                self.__spaces[index].scale(x, y, z, point)
            else:            
                for space in self.__spaces: space.scale(x, y, z, point)
            return True
        except Exception:
            traceback.print_exc()
            return False         
 
    def setAlpha(self, alpha: int = 255, index: int = None) -> bool:
        """
        Sets the alpha of the indicated or all spaces.
        Affects all spaces if no index is delivered.        
        Returns True on success.
        Returns False on failure.
        """
        try:
            if index:
                index = int(index)
                spaces = self.spaces()
                if index > len(spaces) or index < 0 - 1: return False
                self.__spaces[index].alpha = alpha
            else:            
                for space in self.__spaces: space.alpha = alpha
            return True
        except Exception:
            traceback.print_exc()
            return False    
    
    def setColor(self, color: Tuple[int, int, int], index: int = None) -> bool:
        """
        Sets the color of the indicated or all spaces.
        Affects all spaces if no index is delivered.        
        Returns True on success.
        Returns False on failure.
        """
        try:
            if index:
                index = int(index)
                spaces = self.spaces()
                if index > len(spaces) or index < 0 - 1: return False
                self.__spaces[index].color = color
            else:            
                for space in self.__spaces: space.color = color
            return True
        except Exception:
            traceback.print_exc()
            return False

    def setHeight(self, value: float = 1.0, index: int = None) -> bool:
        """
        Sets the height as a float for the indicated space.
        Affects all spaces if no index is delivered.     
        Returns True on success.
        Returns False on failure.
        """
        try:
            if index:
                index = int(index)
                spaces = self.spaces()
                if index > len(spaces) or index < 0 - 1: return False
                self.__spaces[index].height = value
            else:            
                for space in self.__spaces: space.height = value
            return True
        except Exception:
            traceback.print_exc()
            return False
        
    def setLevel(self, value: float = 1.0, index: int = None) -> bool:
        """
        Sets the level as a float for the indicated space.
        Affects all spaces if no index is delivered.     
        Returns True on success.
        Returns False on failure.
        """
        try:
            if index:
                index = int(index)
                spaces = self.spaces()
                if index > len(spaces) or index < 0 - 1: return False
                self.__spaces[index].level = value
            else:            
                for space in self.__spaces: space.level = value
            return True
        except Exception:
            traceback.print_exc()
            return False  
        
    def setName(self, value: str = "", index: int = None) -> bool:
        """
        Sets the name of the indicated space.
        Affects all spaces if no index is delivered.     
        Returns True on success.
        Returns False if the spaces list is empty or on other failure.
        """
        try:
            if index:
                index = int(index)
                spaces = self.spaces()
                if index > len(spaces) or index < 0 - 1: return False
                self.__spaces[index].name = value
            else:            
                for space in self.__spaces: space.name = value
            return True
        except Exception:
            traceback.print_exc()
            return False  
        
    def wrap(self, points: List[aecPoint], index: int = None) -> bool:
        """
        Wraps the indicated space around the delivered points as a convex hull.
        Affects all spaces if no index is delivered.    
        Returns True on success.
        Returns False on failure.
        """     
        try:
            if index:
                index = int(index)
                spaces = self.spaces()
                if index > len(spaces) or index < 0 - 1: return False
                self.__spaces[index].wrap(points)
            else:
                for space in self.__spaces: space.wrap(points)
            return True
        except Exception:
            traceback.print_exc()
            return False              