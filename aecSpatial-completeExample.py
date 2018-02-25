from OCC.Display.SimpleGui import init_display
from aecSpace import aecSpace
from aecSpacer import aecSpacer
from aecSpaceDrawOCC import aecSpaceDrawOCC

commercial = [50, 166, 255]
hospitality = [216, 91, 255]
residential = [255, 239, 17]
retail = [76, 205, 0]


towerCoord = [[0, 0], [20, 0], [30, 30], [20, 50], [0, 50]]
plinthCoord = [[-10, -10], [30, -10], [40, 40], [30, 60], [-10, 60]]
siteCoord = [[-20, -20], [40, -20], [50, 50], [40, 70], [-20, 70]]

display, start_display, add_menu, add_function_to_menu = init_display()
spaceDrawer = aecSpaceDrawOCC()
spacer = aecSpacer()
space = aecSpace()
space.setPerimeter(towerCoord)
space.setHeight(7)
space.setColor(residential)
spaceCentroid = space.getCentroid2D()


originX = spaceCentroid[0] - 20
originY = spaceCentroid[1] - 10
core = aecSpace()
core.setPerimeter(
    [
         [originX, originY], 
         [originX + 20, originY], 
         [originX + 20, originY + 10], 
         [originX, originY + 10]
    ])
core.setHeight(7.75 * 21)
core.setColor([64, 64, 64])


spaces = spacer.stacker(space, 19, 1)


site = aecSpace()
site.setPerimeter(siteCoord)
site.setHeight(0.01)
site.setColor([60, 60, 60])

towerShell = spacer.copy(spaces[1])
towerShell.scale([1.1, 1.1, 1.1])
towerShell.move([0, 0, 7.5])
towerShell.setHeight(7 * 20.8)
towerShell.setColor(retail)
towerShell.setTransparency(0.9)

rotate = 0

for floor in spaces:
    floor.setTransparency(0.5)
    floor.rotate(rotate)
    rotate += 0.5

spaces[0].setPerimeter(plinthCoord)

plinthShell = spacer.copy(spaces[0])
plinthShell.scale([1.1, 1.1, 1])
plinthShell.setHeight(7 * 2.2)
plinthShell.setColor(retail)
plinthShell.setTransparency(0.9)


spaces[1].setPerimeter(plinthCoord)
spaces[0].setColor(retail)
spaces[1].setColor(retail)
spaces[2].setColor(commercial)
spaces[3].setColor(commercial)
spaces[4].setColor(commercial)
spaces[5].setColor(commercial)
spaces[6].setColor(hospitality)
spaces[7].setColor(hospitality)
spaces[8].setColor(hospitality)
spaces[9].setColor(hospitality)
spaces[10].setColor(hospitality)
spaces[11].setColor(hospitality)

totalRentableArea = 0
for floor in spaces:
    totalRentableArea += floor.getArea()
# end for

spaces.append(site)
spaces.append(core)
spaces.append(plinthShell)
spaces.append(towerShell)

print("\n\n\n\nSPACE ALLOCATION REPORT")
print("\n\nTotal Residential Area: " + str(spaces[2].getArea() * 7) + " Square Meters")
print("\n\nTotal Hospitality Area: " + str(spaces[2].getArea() * 6) + " Square Meters")
print("\n\nTotal Commercial Area: " + str(spaces[2].getArea() * 4) + " Square Meters")
print("\n\nStreet Retail Area: " + str(space.getArea()) + " Square Meters")
print("\n\nTotal Retail Area: " + str(space.getArea() * 2) + " Square Meters")
print("\n\nTotal Rentable Area: " + str(totalRentableArea) + " Square Meters")

spaceDrawer.Draw3D(display, spaces)
start_display()