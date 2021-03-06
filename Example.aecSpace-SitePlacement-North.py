import random

from aecSpace.aecColor import aecColor
from aecSpace.aecGeometry import aecGeometry
from aecSpace.aecPoint import aecPoint
from aecSpace.aecShaper import aecShaper
from aecSpace.aecSpace import aecSpace
from aecSpace.aecSpacer import aecSpacer
from aecSpace.aecSpaceGroup import aecSpaceGroup
from aecSpace.aecSpaceDrawOCC import aecSpaceDrawOCC

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
        'area' : 100000,
        'color' : aecColor.blue,
        'diameter' : (150, 250),
        'height' : 20,
        'level' : 0,
        'name' : 'Headquarters',
    }
]

def placeBuilding():
    spacer = aecSpacer()  
    shaper = aecShaper()      
    site = aecSpace()
    sitePoints = siteBoundary["coordinates"]
    sitePoints = [aecPoint(pnt[0], pnt[1], 0) for pnt in sitePoints]
    site.boundary = sitePoints
    site.color = aecColor.green
    site.height = 0.1
    site.level = -0.1
    spaces = [site]
    building = buildings[0]
    xWidth = building['diameter'][random.randint(0, 1)]
    yDepth = xWidth * 1.618
    space = aecSpace()
    space.boundary = shaper.makeCross(origin = aecPoint(0, 0, 0), 
                                      xSize = xWidth, 
                                      ySize = yDepth)
    space.rotate(random.uniform(0, 270))
    orientation = [
                       aecGeometry.NW,
                       aecGeometry.NNW,
                       aecGeometry.NW,
                       aecGeometry.N,
                       aecGeometry.NNE,
                       aecGeometry.NE,
                  ]
    if spacer.placeOnLine(space, site, orientation):
        space.height = building['height']
        space.level= building['level']
        space.color = building['color']
        spaces += [space]
        space2 = spacer.stackToArea(space, building['area'])
        spaces += space2
    return spaces

x = 0
y = 0
spaces = []
displace = -1500
vector = (displace, 0, 0)
while y < 7:
    while x < 7:
        spcGroup = aecSpaceGroup()
        spcGroup.add(placeBuilding())
        if spcGroup.count == 1: continue
        vector = (vector[0] + abs(displace), vector[1], 0)        
        spcGroup.moveBy(vector[0], vector[1], vector[2])
        spaces += spcGroup.spaces
        x += 1
    vector = (-1500, vector[1] + abs(displace), 0)    
    x = 0
    y += 1     
spaceDrawer = aecSpaceDrawOCC()
spaceDrawer.draw3D(spaces, displaySize = (1600, 900), update = True)
# update = True animates the example by updating the display after every space placement.
# About 60x slower to completion, but more interesting to watch.




