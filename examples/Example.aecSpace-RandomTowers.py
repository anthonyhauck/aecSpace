"""
aecSpaceExample-RandomTowers

Assuming you've downloaded this source to your desktop, these instructions
should work.

These classes and this example were developed using the Anaconda development
environment, relevant due to the need for the pythonOCC toolkit, a Python
wrapper around the open source openCascade geometry kernel. The conda package
manager makes it easy to install pythonOCC.

To install Anaconda, visit https://www.anaconda.com/download/

To install pythonOCC, open the Anaconda prompt (not the OS command prompt!)
that you should find installed as a separate application from Anaconda 
Navigator, and paste in this line from http://www.pythonocc.org/download/

conda install -c conda-forge -c dlr-sc -c pythonocc -c oce pythonocc-core==0.18.1

aecSpace uses the shapely, sympy, numpy, and scipy libraries for geometric 
operations, so you'll need those as well:
    
conda install -c conda-forge shapely
conda install -c conda-forge sympy
conda install -c conda-forge scipy

numpy should already be installed with Anaconda.

After this you theoretically have everything you need to run this example.
Make sure your IDE can find the folder where you've stored these *.py files.
All the code outside of any aecSpaceExample-*.py file has been encapsulated 
as discrete objects.

Please leave questions and comments at the github repo where you found this.

Have fun!
Anthony Hauck | Black Arts Consulting
anthony@blackarts.co
"""

import random

from aecColors import aecColors
from aecSpace import aecSpace
from aecSpacer import aecSpacer
from aecSpaceGroup import aecSpaceGroup
from aecSpaceDrawOCC import aecSpaceDrawOCC

def aecSpaceRandomTowers():
    """
    Constructs a series of tower space distibution examples from a 
    combination of fixed and randomly set values and floor divisions.
    """
    origin = (0, 0, 0)
    displace = 300    
    
    def randomFloor(point):
        try:
            floor = aecSpace()
            floorSizeX = random.randint(60, 100)
            floorSizeY = random.randint(60, 100)
            floorHeight = random.randint(8, 10)
            floorType = random.randint(1, 11)
            width = random.randint(33, 45) * 0.01
            depth = random.randint(33, 45) * 0.01
            xOffset = random.randint(10, 90) * 0.01
            yOffset = random.randint(10, 90) * 0.01
            if floorType == 1:
                floor.makeBox(point, (floorSizeX, floorSizeY, 0))
                floor.rotate(random.randint(0, 360))
                x = 0
                boundaries = random.randint(1, 5)
                tempFloor = aecSpace()
                while x < boundaries:
                    tempFloor.makeBox(point, 
                                          (random.randint(65, 100), 
                                           random.randint(65, 100), 0))
                    tempFloor.rotate(random.randint(0, 360))
                    floor.addBoundary(tempFloor.getPointsFloor(points2D = True))
                    x += 1
            if floorType == 2:
                floor.makeCylinder((point[0] + (floorSizeX * 0.5),
                                  point[1] + (floorSizeY * 0.5), 0),
                                  (floorSizeX * 0.5))
            if floorType > 2 and floorType < 9:
                floor.makePolygon((point[0] + (floorSizeX * 0.5),
                                   point[1] + (floorSizeY * 0.5), 0),
                                   (floorSizeX * 0.5), floorType)
            if floorType == 9:
                floor.makeCross(point, (floorSizeX, floorSizeY, floorHeight),
                                                 xWidth = width, yDepth = depth,
                                                 xAxis = xOffset, yAxis = yOffset)                                             
            if floorType == 10:
                floor.makeH(point, (floorSizeX, floorSizeY, floorHeight),
                                             xWidth1 = width, xWidth2 = depth, 
                                             yDepth = depth)
            if floorType == 11:
                floor.makeU(point, (floorSizeX, floorSizeY, floorHeight),
                                             xWidth1 = width, xWidth2 = depth, 
                                             yDepth = depth)
                
            floor.rotate(random.randint(0, 360))
            floor.setHeight(floorHeight)
            return floor
        except:
            return False       
    
    def makeTower(point):
        spacer = aecSpacer()
        levels = random.randint(5, 70)
        floor = randomFloor(point)
        if not floor:
            return
        height = floor.getHeight()
        floors = [floor] + spacer.stack(floor, levels - 1)
        hasPlinth = random.randint(1, 3)
        if hasPlinth == 1:
            hasPlinth = True
            plinth = aecSpace()
            plinthLevels = random.randint(1, 3)
            plinthHeight = height * plinthLevels
            plinth.wrap(floor.getPointsFloor(points2D = True))
            plinth.setHeight(plinthHeight)        
            pScale = random.randint(20, 25) * 0.1
            plinth.scale((pScale, pScale, 1))
            floors = floors[plinthLevels:]
            floors = [plinth] + floors
        colors = [aecColors.blue, aecColors.green, aecColors.white]
        function = random.randint(0, 2)
        tower = aecSpaceGroup()
        tower.addSpaces(floors)
        tower.setColor(colors[function])
        tower.rotate(random.randint(0, 360))
        if levels >= 10:
            tower.scale((0.8, 0.8, 1), indices = list(range(10, levels)))
        if levels >= 30:
           tower.scale((0.8, 0.8, 1), indices = list(range(30, levels)))
        return tower
        
    def makeTowerRow(point, columns, displacement):
        towerRow = aecSpaceGroup()
        tower = makeTower(point)
        towerRow.addSpaces(tower.getSpaces())
        x = 0
        while x < columns:
            point = (point[0] + displacement, point[1], point[2])
            tower = makeTower(point)
            towerRow.addSpaces(tower.getSpaces())
            x += 1
        return towerRow
    
    def makeTowerRows(point, displacement, columns, rows):
        towerRows = aecSpaceGroup()
        x = 0
        while x < rows:
            towerRow = makeTowerRow(point, columns, displacement)
            towerRows.addSpaces(towerRow.getSpaces())
            point = (point[0], point[1] + displacement, point[2])
            x += 1
        return towerRows      
    return makeTowerRows(origin, displace, 5, 5)

# end aecSpaceERandomTowers

  
spaces = aecSpaceRandomTowers()
spaceDrawer = aecSpaceDrawOCC()
spaceDrawer.draw3D(spaces)



