import numpy
import traceback
from typing import List, Tuple
from uuid import uuid4

class aecPoint():
    """
    Represents 2D or 3D Cartesian coordinates as three float values.
    """
    
    __slots__ = ['__ID', '__x', '__y', '__z']
      
    def __init__(self, x:float = 0, y:float = 0, z:float = 0):
        """
        Constructor defaults to origin point coordinates.
        """
        self.__ID = str(uuid4())
        self.__x = float(x)
        self.__y = float(y)
        self.__z = float(z)

    @property
    def ID(self) -> str:
        """
        Property
        Returns the UUID.
        """            
        try:
            return self.__ID
        except Exception:
            traceback.print_exc()
            return None

    @property
    def x(self) -> float:
        """
        Property
        Returns the x coordinate.
        """          
        try:
            return self.__x
        except Exception:
            traceback.print_exc()
            return None    
    
    @x.setter
    def x(self, x: float = 0):
        """
        Property
        Sets the x coordinate.
        Restores previous value on failure.  
        """                  
        try:
            preX = self.__x
            self.__x = float(x)
        except Exception:
            self.__x = preX
            traceback.print_exc()
       
    @property
    def y(self) -> float:
        """
        Property
        Returns the y coordinate.
        """                 
        try:
            return self.__y
        except Exception:
            traceback.print_exc()
            return None    
    
    @y.setter
    def y(self, y: float = 0):
        """
        Property
        Sets the y coordinate.
        Restores previous value on failure.
        """              
        try:
            preY = self.__y
            self.__y = float(y)
        except Exception:
            self.__y = preY
            traceback.print_exc()
    
    @property
    def z(self) -> float:
        """
        Property
        Returns the z coordinate.
        """            
        try:
            return self.__z
        except Exception:
            traceback.print_exc()
            return None    
    
    @z.setter
    def z(self, z: float = 0):
        """
        Property
        Sets the z coordinate.
        Restores previous value on failure.
        """           
        try:
            preZ = self.__z
            self.__z = float(z)
        except Exception:
            self.__z = preZ
            traceback.print_exc()

    @property
    def xy(self) -> Tuple[float, float]:
        """
        Property
        Returns x and y coordinates as a (x, y) tuple.
        """
        try:
            return (self.x, self.y)
        except Exception:
            traceback.print_exc()
            return None  
        
    @xy.setter
    def xy(self, coord: Tuple[float, float]):
        """
        Property
        Sets the x and y coordinates with an (x, y) tuple.
        """
        try:
            preX = self.x
            preY = self.y
            self.x = coord[0]
            self.y = coord[1]
        except Exception:
            self.x = preX
            self.y = preY   
            traceback.print_exc()
            return None          

    @property
    def xy_array(self) -> numpy.array:
        """
        Property
        Returns x and y coordinates as a (x, y) numpy array.
        """
        try:
            return numpy.array(self.xyz)
        except Exception:
            traceback.print_exc()
            return None 

    @property
    def xy_list(self) -> List[float]:
        """
        Property
        Returns x and y coordinates as a (x, y) list.
        """
        try:
            return list(self.xyz)
        except Exception:
            traceback.print_exc()
            return None  
                 
    @property
    def xyz(self) -> Tuple[float, float, float]:
        """
        Property
        xyz returns the coordinate.
        Use .x, .y, and .z to access each value from the result.
        """
        try:
            return (self.x, self.y, self.z)
        except Exception:
            traceback.print_exc()
            return None           
    
    @xyz.setter
    def xyz(self, coord: Tuple[float, float, float]):
        """
        Property
        Sets the x, y, and z coordinates with an (x, y, z) tuple.
        Restores previous values on failure.    
        """
        try:
            preX = self.x
            preY = self.y
            preZ = self.z
            self.x = coord[0]
            self.y = coord[1]
            self.z = coord[1]
        except Exception:
            self.x = preX
            self.y = preY 
            self.z = preZ  
            traceback.print_exc()
            return None     

    @property
    def xyz_array(self) -> numpy.array:
        """
        Property
        Returns the 3D coordinates as a numpY array.
        """
        try:
            return numpy.array(self.xyz)
        except Exception:
            traceback.print_exc()
            return None    

    @property
    def xyz_list(self) -> List[float]:
        """
        Property
        Returns the 3D coordinates as a list.
        """
        try:
            return list(self.xyz)
        except Exception:
            traceback.print_exc()
            return None       
               
    def moveBy(self, x:float = 0, y:float = 0, z:float = 0) -> bool:
        """
        Changes each coordinate by the corresponding delivered value.
        Return True on success.
        Returns False on failure and reverts coordinate values.         
        """
        try:
            preX = self.x
            preY = self.y
            preZ = self.z                    
            self.x += x
            self.y += y
            self.z += z
            return True
        except Exception:
            self.x = preX
            self.y = preY             
            self.z = preZ             
            traceback.print_exc()
            return False