"""
aecSpaceExample-Mirror

Please leave questions and comments at the github repo where you found this.

Have fun!
Anthony Hauck | Black Arts Consulting
anthony@blackarts.co
"""

# Import the classes we'll need.

from aecSpace.aecColor import aecColor
from aecSpace.aecPoint import aecPoint
from aecSpace.aecSpace import aecSpace
from aecSpace.aecSpacer import aecSpacer
from aecSpace.aecSpaceDrawOCC import aecSpaceDrawOCC

# Create class instances.

colors = aecColor()
space = aecSpace()
spacer = aecSpacer()
spaceDrawer = aecSpaceDrawOCC()

# Create a five-sided aecSpace at the origin.

space.points_floor = [aecPoint(0, 0), 
                      aecPoint(20, 0), 
                      aecPoint(30, 30), 
                      aecPoint(20, 50), 
                      aecPoint(0, 50)]
space.height = 15
newSpace = spacer.copy(space, 0, 0, 20)
newSpace.mirror()
spaces = [space, newSpace]
     
spaceDrawer.draw3D(spaces, displaySize = (1600, 900), update = True)
