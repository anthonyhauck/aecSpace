import random

from aecColors import aecColors
from aecSpace import aecSpace
from aecSpacer import aecSpacer
from aecSpaceGroup import aecSpaceGroup
from aecSpaceDrawOCC import aecSpaceDrawOCC

siteBoundary = \
{
     "type": "Polygon",
     "coordinates": \
     [
        [2000.1994, 2289.2733],
        [2700.4829, 2289.2733],
        [2700.4829, 1737.8546],
        [2108.5229, 1263.0727],
        [1792.2478, 1263.0727],
        [1771.8803, 1282.6400]          
     ]
}

siteBound = \
[
    (2000.1994, 2289.2733),
    (2700.4829, 2289.2733),
    (2700.4829, 1737.8546),
    (2108.5229, 1263.0727),
    (1792.2478, 1263.0727),
    (1771.8803, 1282.6400)
]

buildings = \
[
    {
        'area' : 180000,
        'color' : aecColors.blue,
        'diameter' : (150, 200),
        'height' : 40,
        'level' : 0,
        'name' : 'Headquarters',
    }
]

def placeBuilding():
    spacer = aecSpacer()        
    site = aecSpace()
    sitePoints = siteBoundary["coordinates"]
    site.setBoundary(sitePoints)
    site.setColor(aecColors.green)
    site.setHeight(-0.1)
    spaces = [site]
    building = buildings[0]
    xWidth = building['diameter'][random.randint(0, 1)]
    yDepth = xWidth * 1.618
    space = aecSpace()
    space.makeCross((0, 0, 0), (xWidth, yDepth, 0))
    space.rotate(random.randint(0, 360))
    orientation = random.randint(1, 4)
    if spacer.placeWithinLine(space, site, orientation):
        space.setHeight(building['height'])
        space.setLevel(building['level'])
        space.setColor(building['color'])
        spaces += [space]
        space2 = spacer.stackToArea(space, building['area'])
        spaces += space2          
    return spaces

x = 0
y = 0
spaces = []
displace = -1500
vector = (displace, 0, 0)
compass = 0
while y < 7:
    while x < 7:
        spcGroup = aecSpaceGroup()
        spcGroup.addSpaces(placeBuilding())
        vector = (vector[0] + abs(displace), vector[1], 0)        
        spcGroup.move(vector)
        spaces += spcGroup.getSpaces()
        compass += 1             
        x += 1
    vector = (-1500, vector[1] + abs(displace), 0)    
    x = 0
    y += 1     
spaceDrawer = aecSpaceDrawOCC()
spaceDrawer.draw3D(spaces, displaySize = (1600, 900), update = False)
# update = True animates the example by updating the display after every space placement.
# About 60x slower to completion, but more interesting to watch.




