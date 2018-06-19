import traceback
import typing
import uuid

\from aecGeomCalc import aecGeomCalc
from aecSpace import aecSpace
from aecSpacer import aecSpacer



class aecSpaceGrid():
    
    # utility objects and data shared by all instances.
    
    __aecErrorCheck = aecErrorCheck() # An instance of aecErrorCheck.
    __aecGeomCalc = aecGeomCalc()     # An instance of aecGeometryCalc
    __aecSpacer = aecSpacer()         # An instance of aecSpacer        
    __type = 'aecSpaceGrid'                # Type identifier of object instances
    
    #__retain is a shared list of self.__property keys of
    # values to be retained through a call to __initialize.

    __retain = \
    ( 
        'ID',
        'name',
    )    
    
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

            'cells' : {},           # A dictionary of cells managed by this instance. 
            'extents' : (0, 0, 0),  # Dimensions of the cell grid.
            'ID' : None,            # A UUID
            'name' : "",            # A custom string designation.     

            # The following properties are reset by __initialize()

            'area' : None,    # Aggregate area of all cells                                
            'volume' : None,  # Aggregate volume of all cells

        } # end dictionary

        self.__properties['ID'] = uuid.uuid4()
    
    def __initialize(self):
        """
        INTERNAL
        __initialize()
        Resets specific internal variables to NONE to 
        ensure on-demand recompute of dependent values.
        Returns True on success.
        Returns False on failure.
        """
        try:
            for key in self.__properties.keys():
                if not key in self.__retain:
                    self.__properties[key] = None
            self.__properties['cells'] = {}
            self.__properties['extents'] = (0, 0, 0)
            return True
        except Exception:
            traceback.print_exc()
            return False
        
    def deleteCell(self, address):
        """
        bool deleteCell((int, int, int))
        Deletes the cell at the specified address.
        """
        try:
            address = self.__aecErrorCheck.checkAddress(address)
            if not address: return False
            self.__properties['cells'][address] = None
            return True
        except Exception:
            traceback.print_exc()
            return False
        
    def deleteCells(self, addresses):
        """
        [(int, int, int),] deleteCell([(int, int, int),])
        Deletes the cells at the specified list of addresses.
        Returns list of cells successfully deleted.
        Returns False on failure.
        """
        try:
            report = []
            for address in addresses:
                if self.deleteCell(address): 
                    report.append(address)
            return report
        except Exception:
            traceback.print_exc()
            return report

    def getAddresses(self):
        """
        [(int, int, int),] getAddresses()
        Returns the list of all cell addresses in the grid.
        Returns None on failure.
        """
        try:
            addresses = []
            for key in self.__properties['cells'].keys():
                addresses.append(key)
            return addresses
        except Exception:
            traceback.print_exc()
            return None                 
    
    def getCell(self, address):
        """
        aecSpace getCell((int, int, int))
        Returns the cell at the specified address as an aecSpace.
        Returns the last cell if the address is out of range. 
        Returns None if the cell at the address has been deleted.
        Returns None on Failure.
        """
        try:
            address = self.__aecErrorCheck.checkAddress(address, self.__properties['extents'])
            if not address: return None
            return self.__properties['cells'][address]
        except Exception:
            traceback.print_exc()
            return None 

    def getCells(self, addresses = None):
        """
        [aecSpace,] getCells([(int, int, int),])
        Returns the cells at the specified addresess as a list of aecSpaces.
        Returns the last cell if a specified address is out of range. 
        Returns an entry of None for every requested cell that has been deleted.
        Returns None on Failure.
        """
        try:
            cells = []            
            if not addresses: addresses = self.getAddresses()            
            for address in addresses:
                address = self.__aecErrorCheck.checkAddress(address, self.__properties['extents'])
                if not address: continue
                cells.append(self.__properties['cells'][address])
            return cells
        except Exception:
            traceback.print_exc()
            return None                     

    def getExtents(self):
        """
        (int, int, int) getExtents()
        Returns the extents of grid as a 3-digit tuple.
        Returns None on Failure.
        """
        try:
            return self.__properties['extents']
        except Exception:
            traceback.print_exc()
            return None 

    def getProperties(self):
        """
        dictionary getProperties()
        Retrieves the properties dictionary of all internal values.
        Intended for use by other components of the aecSpace toolkit.
        Returns None on failure.
        """
        try:
            return self.__properties
        except Exception:
            traceback.print_exc()
            return None        

    def getProperty(self, prpName: str):
        """
        value getProperty(string)
        Directly retrieves a property by its string key, bypassing all error checking.
        Intended for use by other components of the aecSpace toolkit.
        Returns None on failure.
        """
        try:
            return self.__properties[prpName]
        except Exception:
            traceback.print_exc()
            return None

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

    def makeCells(self, origin: tuple = (0, 0, 0), \
                        cellSize: tuple = (1, 1, 1), \
                        extents: tuple = (1, 1, 1)):
        """
        bool makeCells((3D point), number, (int, int, int))
        Creates a grid in the positive xyz directions from the specified origin.
        Each cell will be an aecSpace cube of diameter cellSize.
        The overall dimensions of the grid are extents[0] x-axis cells
        by extents[1] y-axis cells by extents[2] z-axis cells.
        Returns True on success.
        Returns False on failure.
        """
        try:

            origin = self.__aecErrorCheck.checkPoint(origin)
            if not origin: return False
            self.__initialize()
            cell = aecSpace()
            cell.makeBox(origin, cellSize)
            xKey = yKey = zKey = (0, 0, 0)
            extents = [int(x - 1) for x in list(extents)]
            xRow = [cell] + self.__aecSpacer.row(cell, extents[0])
            for xCell in xRow:
                if not xCell: continue
                xCell.setAddress(xKey)
                self.__properties['cells'][xKey] = xCell
                yRow = self.__aecSpacer.row(xCell, extents[1], xAxis = False)
                for yCell in yRow:
                    yKey = (yKey[0], yKey[1] + 1, yKey[2])
                    yCell.setAddress(yKey)
                    self.__properties['cells'][yKey] = yCell
                xKey = yKey = (xKey[0] + 1, xKey[1], xKey[2]) 
            zCells = []
            for key in self.__properties['cells'].keys():
                zStack = self.__aecSpacer.stack(self.__properties['cells'][key], extents[2])
                for zCell in zStack:
                    zKey = (key[0], key[1], zKey[2] + 1)
                    zCell.setAddress(zKey)
                    zCells.append((zKey, zCell))
                zKey = (key[0], key[1], key[2])
            for zCell in zCells:
                self.__properties['cells'][zCell[0]] = zCell[1]
            self.__properties['extents'] = tuple(extents)
            return True
        except Exception:
            traceback.print_exc()
            return False

    def setColor(self, newColor = None, addresses = None):
        """
        [(int, int, int),] setColor (int range 0 - 255, int range 0 - 255, int range 0 - 255), [(int, int, int),])
        Sets the color[R G B] values of each cell listed by address in addresses,
        or without argument randomizes the color.
        Affects all cells if no indices are delivered.        
        Returns a list of cell addresses whose color has been changed.
        Returns n
        Returns False on failure.
        """
        try:
            if not addresses: addresses = self.getAddresses()
            report = []
            for address in addresses:
                address = self.__aecErrorCheck.checkAddresses(address)
                if not address: continue
                cell = self.getCell(address)
                if not cell: continue
                cell.setColor(newColor)
                report.append(address)
            return report
        except Exception:
            traceback.print_exc()
            return report

    def setTransparency(self, newTrans = 0, addresses = None):
        """
        [(int, int, int),] setTransparency(number | string, [(int, int, int),])
        Sets the transparency as a percentage or without argument sets transparency to 0.
        Converts newTrans input to a range from 0 to 1.
        Returns True if successful.
        Returns False on failure.
        """
        try:
            newTrans = self.__aecErrorCheck.checkPercentage(newTrans)
            if not newTrans: return False
            if not addresses: addresses = self.getAddresses()
            report = []            
            for address in addresses:
                address = self.__aecErrorCheck.checkAddresses(address)
                if not address: continue
                cell = self.getCell(address)
                if not cell: continue
                cell.setTransparency(newTrans) 
                report.append(address)
            return True
        except Exception:
            traceback.print_exc()
            return report
           