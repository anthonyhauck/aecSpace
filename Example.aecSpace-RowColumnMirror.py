"""
aecSpaceExample-RowColumnMirror

Please leave questions and comments at the github repo where you found this.

Have fun!
Anthony Hauck | Black Arts Consulting
anthony@blackarts.co
"""

from random import randint

from aecSpace.aecColor import aecColor
from aecSpace.aecPoint import aecPoint
from aecSpace.aecSpace import aecSpace
from aecSpace.aecSpacer import aecSpacer
from aecSpace.aecSpaceDrawOCC import aecSpaceDrawOCC

# Create class instances.

colors = aecColor()
space = aecSpace()
spacer = aecSpacer()


# Create an aecSpace at the origin.

space.boundary = ([aecPoint(0, 0), 
                   aecPoint(20, 0), 
                   aecPoint(30, 30), 
                   aecPoint(20, 50), 
                   aecPoint(0, 50)])
space.height = 10

# Create copies of the initial aecSpace and arrange them in a row.

firstTower = spacer.stack(space, 12, 1)
rowTowers = []
for floor in firstTower:
    rowTowers += spacer.row(floor, 5, 70)

columnTowers = []
for floor in rowTowers:
    columnTowers += spacer.row(floor, 5, 70, xAxis = False)
    
spaces = firstTower + rowTowers + columnTowers
    
for floor in spaces:
    floor.color = \
        (randint(0, 255), 
         randint(0, 255),
         randint(0, 255))
    if floor.color.color[0] > 100:
        if floor.color.color[1] < 100:
            floor.mirror()
            floor.rotate(randint(0, 90))
        else:
            floor.mirror()
            floor.rotate(randint(90, 270))
     
spaceDrawer = aecSpaceDrawOCC()
spaceDrawer.draw3D(spaces, displaySize = (1600, 900), update = False)
# update = True animates the example by updating the display after every space placement.
# About 60x slower to completion, but more interesting to watch.