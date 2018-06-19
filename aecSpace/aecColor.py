import traceback

from typing import Tuple

"""
aecColor instantiates a set of color constants and 
variables as RGB tuples and an alpha component.
"""

class aecColor:
 
    aqua = (77, 184, 100)
    beige = (255, 250, 200)
    black = (0, 0, 0)
    blue = (0, 100, 255)
    brown = (170, 110, 40)
    coral = (255, 215, 180)
    cyan = (70, 240, 240)
    darkgray = (64, 64, 64)
    green = (60, 180, 75)
    granite = (60, 60, 60)
    gray = (128, 128, 128)
    lavender = (230, 190, 255)
    lime = (210, 245, 60)
    magenta = (240, 50, 230)
    maroon = (128, 0, 0)
    mint = (170, 255, 195)
    navy = (0, 0, 128)
    olive = (128, 128, 0)
    orange = (255, 115, 15) 
    pink = (255, 66, 138)
    purple = (191, 2, 255)
    red = (255, 0, 0)
    sand = (255, 215, 96)
    stone = (20, 20, 20)
    teal = (0, 128, 128)
    white = (255, 255, 255)
    yellow = (255, 239, 17)
       
    __slots__ = ['__red', '__green', '__blue', '__alpha']
        
    def __init__(self):
        """
        Constructor sets color to white and alpha to opaque.
        """
        self.__red = 255
        self.__green = 255
        self.__blue = 255
        self.__alpha = 0

    @property
    def alpha(self) -> int:
        """
        Returns the color's alpha component.
        """
        try:
            return self.__alpha 
        except Exception:
            traceback.print_exc()
            return None

    @alpha.setter
    def alpha(self, value: int = 0):
        """
        Sets the color's alpha component.
        """
        try:
            self.__alpha = (int(abs(value))) % 256
        except Exception:
            traceback.print_exc()
 
    @property
    def alpha_01(self) -> int:
        """
        Returns the color's alpha component as a value between 0 and 1.
        """
        try:
            return self.__alpha / 255
        except Exception:
            traceback.print_exc()
            return None       

    @property
    def color(self) -> Tuple[int, int, int]:
        """
        Returns the current color as integer RGB values from 0 to 255.
        """
        try:
            return (self.__red, self.__green, self.__blue)
        except Exception:
            traceback.print_exc()
            return None
 
    @color.setter
    def color(self, value: Tuple[int, int, int]):
        """
        Sets the current color with a tuple.
        """
        try:
            if len(value) != 3: return
            value = [(int(abs(val))) % 256 for val in list(value)]
            self.__red = value[0]
            self.__green = value[1]
            self.__blue = value[2]
        except Exception:
            traceback.print_exc()

    @property
    def color_01(self) -> Tuple[float, float, float]:
        """
        Returns the current color as float RGB values from 0 to 1.
        """
        try:
            return (self.__red / 255, 
                    self.__green / 255,
                    self.__blue / 255)
        except Exception:
            traceback.print_exc()
            return None        
        


 
        

    