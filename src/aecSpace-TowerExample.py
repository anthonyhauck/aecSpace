"""
aecSpace Tower Example

Assuming you've downloaded this source to s your desktop, these instrictions
should work.

These classes and this example were developed using the Anaconda development
environment, relevant due to the need for the pythonOCC toolkit, a Python
wrapper around the open source openCascade geometry kernel. The conda package
manager makes it easy to install pythonOCC.

To install Anaconda, visit https://www.anaconda.com/download/

To install pythonOCC, open the Anaconda prompt (not the OS command prompt!)
that you should find installed as a separate aplication from Anaconda 
Navigator, and paste in this line from http://www.pythonocc.org/download/

conda install -c conda-forge -c dlr-sc -c pythonocc -c oce pythonocc-core==0.18.1

After this you theoretically have everything you need to run this example.
Make sure your IDE can find the folder where you've stored these *.py files.
All the code outside of this example file has been encapsulated as discrete objects.

Please leave questions and comments at the github repo where you found this.

Have fun!
Anthony Hauck | Black Arts Consulting
anthony@blackarts.co

"""

# aecSpaceDrawOCC imports all the rest of the pythonOCC components necessary.
# Here we just import enough to initalize the display. All other classes are 
# abstract geometry and have no dependency on the pythonOCC toolkit.

from OCC.Display.SimpleGui import init_display

# Import the classes we'll need.

from aecColors import aecColors
from aecSpace import aecSpace
from aecSpacer import aecSpacer
from aecSpaceDrawOCC import aecSpaceDrawOCC

# Create class instances.

colors = aecColors()
space = aecSpace()
spacer = aecSpacer()
spaceDrawer = aecSpaceDrawOCC()

# Hard code footprint coordinates for the three major elements
# of the model: the site, core, plinth, and tower.
# TODO: make this variable without editing code.

siteCoord = [[-30, -30], [50, -30], [60, 60], [50, 80], [-30, 80]]
plinthCoord = [[-20, -20], [40, -20], [50, 50], [40, 70], [-20, 70]]
towerCoord = [[0, 0], [20, 0], [30, 30], [20, 50], [0, 50]]

# Set the perimeter of the tower so we can use its polygon to find
# the tower centroid. We'll base the offset core's position on the 
# discovered coordinate.

space.setPerimeter(towerCoord)
spaceCentroid = space.getCentroid2D()

# Offset the core footprint corner origin from the tower centroid.
# TODO: make this variable without editing code.

originX = spaceCentroid[0] - 20
originY = spaceCentroid[1] - 10

# Create the core as an aecSpace and set its perimeter.
# TODO: make this variable without editing code.

core = aecSpace()
core.setPerimeter(
    [
         [originX, originY], 
         [originX + 20, originY], 
         [originX + 20, originY + 10], 
         [originX, originY + 10]
    ])

# Create the site as an aecSpace and set its perimeter
# TODO: make this variable without editing code.

site = aecSpace()
site.setPerimeter(siteCoord)

# Set heights of everything we've created so far.
# TODO: make this variable without editing code.

space.setHeight(7)
core.setHeight(7.75 * 21)
site.setHeight(0.01)

# Create copies of the initial aecSpace and stack them vertcally.
# The first numeric argument is the quantity of copies to stack
# sequentially above the delivered aecSpace.
# The second numeric argument indicates the amoount of offset to
# add the space's height, leaving a plenum between stackd spaces
# if greater than 0.
# TODO: make these variable without editing code.

spaces = spacer.stacker(space, 19, 1)

# Since we stacked the aecSpaces upward, the first two aecSpaces
# in the spaces list will be the first and second floors of our
# building, whose perimeters we'll expand to become our retail plinth.
# For the sake of some efficiency in code, since we need to iterate over
# this list anyway, we'll also set the color and transparency of the 
# aecSpaces at the same time.
# TODO: make these variable without editing code.

plinth = spaces[0 : 2]

for floor in plinth:
    floor.setPerimeter(plinthCoord)
    floor.setColor(colors.green)
    floor.setTransparency(0.5)
    
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
    rotate += 0.5
    
# Set all the tower floors to the same transparency as the plinth.
# TODO: make this variable without editing code.

for floor in tower:
    floor.setTransparency(0.5)
    
# Set colors for different tower functions.
    
for floor in towerCommercial:
    floor.setColor(colors.blue)
    
for floor in towerHospitality:
    floor.setColor(colors.purple)   
    
for floor in towerResidential:
    floor.setColor(colors.yellow)
    
# Set the colors of our core and site.
# TODO: make this variable without editing code.

core.setColor(colors.gray)
site.setColor(colors.granite)

# The following code adds shells around the plinth and the tower.
# If you're happy with the spaces representing your tower, you can
# comment out this section.
# TODO: make this variable without editing code.

# First gather up all the 2D points of the aecSpace perimeters
# as projected onto the zero plane.

floorPoints = []
for floor in tower:
    floorPoints += floor.getPoints2D()
    
# Now ask the aecSpacer to find the outermost of all those points.    

towerPoints = spacer.wrapper(floorPoints)

# Copy the lowest floor of the tower to start constructing our tower shell.

towerShell = spacer.copy(tower[0])

# Set the new aecSpace perimeter to the calculated outermost points

towerShell.setPerimeter(towerPoints)

# Scale the new aecSpace slightly outward and upward
# to fully enclose the tower floors.

towerShell.scale([1.02, 1.02, 1.02])

# Set the shell height, color, and  higher transparency.

towerShell.setHeight(7 * 20.8)
towerShell.setColor(colors.blue)
towerShell.setTransparency(0.9)

# Copy the lowest floor of the plinth to start constructing our plinth shell.

plinthShell = spacer.copy(plinth[0])

# Scale the new aecSpace slightly outward and upward
# to fully enclose the plinth floors.

plinthShell.scale([1.1, 1.1, 1])

# Set the shell height, color, and  higher transparency.

plinthShell.setHeight(7 * 2.2)
plinthShell.setColor(colors.blue)
plinthShell.setTransparency(0.9)

# Add the new aecSpace objects to the total list of spaces for
# delivery to the pythonOCC visualization environment.

spaces.append(site)
spaces.append(core)
spaces.append(plinthShell)
spaces.append(towerShell)

# Initialize the pythonOCC display.

display, start_display, add_menu, add_function_to_menu = init_display()

# Call the instance of aecSpaceDrawOCC to draw 
# the aecSpaces in the pythonOCC environment.

spaceDrawer.Draw3D(display, spaces)

# Start the pythonOCC display.

start_display()