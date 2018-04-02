"""
aecSpaceExample-SpaceDistribution

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
from aecSpaceDrawOCC import aecSpaceDrawOCC

def aecSpaceRandomTowers():
    """
    Constructs a series of tower space distibution examples from a 
    combination of fixed and randomly set values and floor divisions.
    """

    origin = (0, 0, 0)
    displace = 300
    spacer = aecSpacer()
    colors = aecColors()
    
    def full(point, xWidth, yDepth, zHeight):
        floor = aecSpace()
        floor.makeBox(point, (xWidth, yDepth, zHeight))
        setColors([floor])
        return [floor]
    
    def halfDepth(point, xWidth, yDepth, zHeight):
        depth = yDepth * 0.5
        half1 = aecSpace()  
        half1.makeBox(point, (xWidth, depth, zHeight))
        halfSpaces = spacer.column(half1)
        setColors(halfSpaces)
        return halfSpaces
    
    def halfWidth(point, xWidth, yDepth, zHeight):
        width = xWidth * 0.5
        half1 = aecSpace()  
        half1.makeBox(point, (width, yDepth, zHeight))
        halfSpaces = spacer.row(half1)
        setColors(halfSpaces)
        return halfSpaces
    
    def quarterDepth(point, xWidth, yDepth, zHeight):
        if random.randint(0, 1) == 0:
            depth = yDepth * 0.25
            scale = 3
        else:
            depth = yDepth * 0.75
            scale = 0.333333333       
        half1 = aecSpace()  
        half1.makeBox(point, (xWidth, depth, zHeight))
        halfSpaces = spacer.column(half1)
        halfSpaces[1].scale([1, scale, 1], halfSpaces[1].getOrigin())
        setColors(halfSpaces)
        return halfSpaces
    
    def quarterWidth(point, xWidth, yDepth, zHeight):
        if random.randint(0, 1) == 0:
            width = xWidth * 0.25
            scale = 3
        else:
            width = xWidth * 0.75
            scale = 0.333333333       
        half1 = aecSpace()  
        half1.makeBox(point, (width, yDepth, zHeight))
        halfSpaces = spacer.row(half1)
        halfSpaces[1].scale([scale, 1, 1], halfSpaces[1].getOrigin())
        setColors(halfSpaces)
        return halfSpaces
    
    def setColors(halfSpaces):
        colors = [aecColors.blue, aecColors.orange, aecColors.purple, aecColors.yellow]
        colorPick = random.randint(0, 3)
        halfSpaces[0].setColor(colors[colorPick])
        if len(halfSpaces) == 1:
            return
        colors.reverse()
        halfSpaces[1].setColor(colors[colorPick])
    
    def makeFloor(point, xWidth, yDepth, zHeight):
        floorType = random.randint(0, 4)
        if floorType == 0:
            floorSpaces = full(point, xWidth, yDepth, zHeight)
        if floorType == 1:
            floorSpaces = halfDepth(point, xWidth, yDepth, zHeight)
        if floorType == 2:
            floorSpaces = halfWidth(point, xWidth, yDepth, zHeight)
        if floorType == 3:
            floorSpaces = quarterDepth(point, xWidth, yDepth, zHeight)
        if floorType == 4:
            floorSpaces = quarterWidth(point, xWidth, yDepth, zHeight)
        return floorSpaces
    
    def makeCore(point, xWidth, yDepth, zHeight): 
        xCoord = (point[0] - 5) + (xWidth * 0.5)
        yCoord = (point[1] + (yDepth * 0.5) + 10)
        point = (xCoord, yCoord, point[2])
        core = aecSpace()
        core.makeBox(point, (10, 20, zHeight))
        core.setColor(colors.gray)
        return [core]
    
    def makeTower(point):
        floors = []
        xWidth = 40 # random.randint(20, 60)
        yDepth = 40 # random.randint(20, 60)
        levels = 20 # random.randint(5, 50)
        zHeight = 10 # random.randint(3, 6)
        plinth = aecSpace()
        plinth.makeBox(point, (xWidth, yDepth, zHeight))
        plinthScaleX = 1.5 # (random.randint(10, 25)) * 0.1
        plinthScaleY = 1.5 # (random.randint(10, 25)) * 0.1
        plinth.scale([plinthScaleX, plinthScaleY, 2], plinth.getCentroid())
        plinth.setColor(colors.green)
        floors.append(plinth)
        floors = floors + makeCore(point, xWidth, yDepth, zHeight * (levels + 3))
        point = (point[0], point[1], point[2] + zHeight * 2)
        x = 0
        while x < levels:
            floors = floors + makeFloor(point, xWidth, yDepth, zHeight)
            point = (point[0], point[1], point[2] + zHeight)
            x += 1       
        return floors
        
    def makeTowerRow(point, columns, displacement):
        towers = []
        towers = towers + makeTower(point)
        x = 0
        while x < columns:
            point = (point[0] + displacement, point[1], point[2])
            towers = towers + makeTower(point)
            x += 1
        return towers
    
    def makeTowerRows(point, displacement, columns, rows):
        towers = []
        x = 0
        while x < rows:
            towers = towers + makeTowerRow(point, columns, displacement)
            point = (point[0], point[1] + displacement, point[2])
            x += 1
        return towers
        
    return makeTowerRows(origin, displace, 5, 5)

# end aecSpaceDistributionExample
  
spaces = aecSpaceRandomTowers()
spaceDrawer = aecSpaceDrawOCC()
spaceDrawer.draw3D(spaces)


