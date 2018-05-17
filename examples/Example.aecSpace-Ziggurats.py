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

def aecSpaceZiggurats():
    """
    Constructs a series of tower space distibution examples from a 
    combination of fixed and randomly set values and floor divisions.
    """
    origin = (0, 0, 0)
    displace = 300    
    
    def randomFloor(point):
        try:
            floor = aecSpace()
            floorSize = 200
            floorHeight = 7
            floor.makeBox(point, (floorSize, floorSize, floorHeight))
            floor.setHeight(floorHeight)
            return floor
        except:
            return False       
    
    def makeTower(point):
        spacer = aecSpacer()
        levels = 10
        floor = randomFloor(point)
        floors = [floor] + spacer.stack(floor, levels - 1)
        colors = [aecColors.purple, aecColors.aqua, aecColors.yellow, aecColors.red, aecColors.red, aecColors.white]
        tower = aecSpaceGroup()
        tower.addSpaces(floors)
        function = random.randint(0, 5)
        tower.setColor(colors[function])
        scale = 0.85
        x = 1
        while x < levels:
            tower.scale((scale, scale, 1), indices = [x])
            scale -= 0.05
            x += 1
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

# end aecSpaceZiggurats

  
spaces = aecSpaceZiggurats()
spaceDrawer = aecSpaceDrawOCC()
spaceDrawer.draw3D(spaces, displaySize = (1600, 900), update = False)
# update = True will animate the example by updating the display after every space placement.
# About 60x slower to completion, but more interesting to watch.


