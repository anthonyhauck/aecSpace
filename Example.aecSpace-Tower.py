"""
aecSpaceExample-Tower

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

def makeTower():

    # Create class instances.
    
    space = aecSpace()
    spacer = aecSpacer()
    
    # Hard code footprint coordinates for the three major elements
    # of the model: the site, core, plinth, and tower.
    # TODO: make this variable without editing code.
    
    siteCoord = \
    [
        aecPoint(-30, -30), 
        aecPoint(50, -30), 
        aecPoint(60, 60), 
        aecPoint(50, 80), 
        aecPoint(-30, 80)
    ]
    plinthCoord = \
    [
        aecPoint(-20, -20), 
        aecPoint(40, -20), 
        aecPoint(50, 50), 
        aecPoint(40, 70), 
        aecPoint(-20, 70)
    ]
    towerCoord = \
    [
        aecPoint(0, 0), 
        aecPoint(20, 0), 
        aecPoint(30, 30, 0), 
        aecPoint(20, 50, 0), 
        aecPoint(0, 50, 0)
    ]
    
    # Set the perimeter of the tower so we can use its polygon to find
    # the tower centroid. We'll base the offset core's position on the 
    # discovered coordinate.
    
    space.boundary = towerCoord
    spaceCentroid = space.centroid_floor
    
    # Offset the core footprint corner origin from the tower centroid.
    # TODO: make this variable without editing code.
    
    originX = spaceCentroid.x - 20
    originY = spaceCentroid.y - 10
    
    # Create the core as an aecSpace and set its perimeter.
    # TODO: make this variable without editing code.
    
    core = aecSpace()
    core.boundary = \
    [
         aecPoint(originX, originY), 
         aecPoint(originX + 20, originY), 
         aecPoint(originX + 20, originY + 10), 
         aecPoint(originX, originY + 10)
    ]
    
    # Create the site as an aecSpace and set its perimeter
    # TODO: make this variable without editing code.
    
    site = aecSpace()
    site.boundary = siteCoord
    
    # Set heights of everything we've created so far.
    # TODO: make this variable without editing code.
    
    space.height = 7
    space.level = 0
    core.height = (7.75 * 21)
    site.height = 0.1
    site.level = -0.1
    
    # Create copies of the initial aecSpace and stack them vertically.
    # The first numeric argument is the quantity of copies to stack
    # sequentially above the delivered aecSpace.
    # The second numeric argument indicates the amoount of offset to
    # add the space's height, leaving a plenum between stackd spaces
    # if greater than 0.
    # TODO: make these variable without editing code.
    
    spaces = [space] + spacer.stack(space, 19, 1)
    
    # Since we stacked the aecSpaces upward, the first two aecSpaces
    # in the spaces list will be the first and second floors of our
    # building, whose perimeters we'll expand to become our retail plinth.
    # For the sake of some efficiency in code, since we need to iterate over
    # this list anyway, we'll also set the color and transparency of the 
    # aecSpaces at the same time.
    # TODO: make these variable without editing code.
    
    plinth = spaces[0 : 2]
    
    for floor in plinth:
        floor.boundary = plinthCoord
        floor.color = aecColor.green
        floor.color.alpha = 127
        
    # The remainder of the stacked aecSpaces will become our tower.
        
    tower = spaces[2:]
    
    # Set up functional sections of the tower.
    # TODO: make these variable without editing code.
    
    towerCommercial = tower[0: 5]
    towerHospitality = tower[5: 11]
    towerResidential = tower[11:]
    
    # Rotate each tower space around its centroid. 
    # Comment out this section if you'd like a straight tower.
    # TODO: make this variable without editing code.
    
    rotate = 0
    for floor in tower:
        floor.rotate(rotate)
        rotate += 10
        
    # Set all the tower floors to the same transparency as the plinth.
    # TODO: make this variable without editing code.
    
    for floor in tower:
        floor.color.alpha = 127
        
    # Set colors for different tower functions.
        
    for floor in towerCommercial:
        floor.color = aecColor.blue
        
    for floor in towerHospitality:
        floor.color = aecColor.purple
        
    for floor in towerResidential:
        floor.color = aecColor.yellow
        
    # Set the colors of our core and site.
    # TODO: make this variable without editing code.
    
    core.color = aecColor.gray
    site.color = aecColor.granite
    
    # The following code adds shells around the plinth and the tower.
    # If you're happy with the spaces representing your tower, you can
    # comment out this section.
    # TODO: make this variable without editing code.
    
    # First gather up all the 2D points of the aecSpace perimeters
    # as projected onto the zero plane.
    
    floorPoints = []
    for floor in tower:
        floorPoints += floor.points_floor
        
   
    # Construct the tower shell by setting the boundary to an outermost
    # wrap of all the collected exterior points.
    
    towerShell = aecSpace()
    towerShell.wrap(floorPoints)
       
    # Scale the new aecSpace slightly outward and upward
    # to fully enclose the tower floors.
    
    towerShell.scale(1.1, 1.1, 1.1)
    
    # Set the shell level, height, color, and  higher transparency.
    
    towerShell.level = (7 * 2.2)
    towerShell.height = (7 * 20.8)
    towerShell.color = aecColor.blue
    towerShell.color.alpha = 200
    
    # Copy the lowest floor of the plinth to start constructing our plinth shell.
    
    plinthShell = spacer.copy(plinth[0])
    
    # Scale the new aecSpace slightly outward and upward
    # to fully enclose the plinth floors.
    
    plinthShell.scale(1.1, 1.1, 1)
    
    # Set the shell height, color, and  higher transparency.
    
    plinthShell.height = (7 * 2.2)
    plinthShell.color = aecColor.blue
    plinthShell.color.alpha = 200
    
    # Add the new aecSpace objects to the total list of spaces for
    # delivery to the pythonOCC visualization environment.
    
    spaces.append(site)
    spaces.append(core)
    spaces.append(plinthShell)
    spaces.append(towerShell)
    return spaces

# end makeTower

spaces = makeTower()
spaceDrawer = aecSpaceDrawOCC()
spaceDrawer.draw3D(spaces, displaySize = (1600, 900), update = True)
# update = True animates the example by updating the display after every space placement.
# About 60x slower to completion, but more interesting to watch.
