"""
aecSpaceExample-RandomTower

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
from aecShaper import aecShaper
from aecSpaceDrawOCC import aecSpaceDrawOCC

def aecSpaceRandomTower():
    """
    Constructs a series of tower space distibution examples from a 
    combination of fixed and randomly set values and floor divisions.
    """   
    def randomFloor(point):
        try:
            floor = aecSpace()
            shaper = aecShaper()
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
                    floor.addBoundary(tempFloor.getPointsExterior2D())
                    x += 1
            if floorType == 2:
                floor.makeCircle((point[0] + (floorSizeX * 0.5),
                                  point[1] + (floorSizeY * 0.5), 0),
                                  (floorSizeX * 0.5))
            if floorType > 2 and floorType < 9:
                floor.makePolygon((point[0] + (floorSizeX * 0.5),
                                   point[1] + (floorSizeY * 0.5), 0),
                                   (floorSizeX * 0.5), floorType)
            if floorType == 9:
                floor = shaper.makeCross(point, (floorSizeX, floorSizeY, floorHeight),
                                                 xWidth = width, yDepth = depth,
                                                 xAxis = xOffset, yAxis = yOffset)                                             
            if floorType == 10:
                floor = shaper.makeH(point, (floorSizeX, floorSizeY, floorHeight),
                                             xWidth1 = width, xWidth2 = depth, 
                                             yDepth = depth)
            if floorType == 11:
                floor = shaper.makeU(point, (floorSizeX, floorSizeY, floorHeight),
                                             xWidth1 = width, xWidth2 = depth, 
                                             yDepth = depth)
                
            floor.rotate(random.randint(0, 360))
            floor.setHeight(floorHeight)
            return floor
        except:
            return False
        
    
    def makeTower(point):
        spacer = aecSpacer()
        levels = random.randint(5, 50)
        floor = randomFloor(point)
        if floor == False:
            return
        height = floor.getHeight()
        tower = spacer.stack(floor, levels)
        hasPlinth = random.randint(1, 3)
        if hasPlinth == 1:
            hasPlinth = True
            plinth = aecSpace()
            plinthLevels = random.randint(1, 3)
            plinthHeight = height * plinthLevels
            plinth.wrap(floor.getPointsExterior2D())
            plinth.setHeight(plinthHeight)        
            pScale = random.randint(20, 25) * 0.1
            plinth.scale((pScale, pScale, 1))
            tower = tower[plinthLevels:]
            tower = [plinth] + tower  
        colors = [aecColors.blue, aecColors.green]
        function = random.randint(0, 1)
        for floor in tower:
            floor.setColor(colors[function])        
        rotation = random.randint(0, 360)
        for floor in tower:
            floor.rotate(rotation)
        if levels >= 10:
           rotation = random.randint(0, 20)
           for floor in tower[10:]:
               floor.scale((0.8, 0.8, 1))
        if levels >= 30:
           for floor in tower[30:]:
               floor.scale((0.8, 0.8, 1))
        return tower
        
    return makeTower((0, 0, 0))

# end aecSpaceRandomTower

  
spaces = aecSpaceRandomTower()
spaceDrawer = aecSpaceDrawOCC()
spaceDrawer.Draw3D(spaces)



