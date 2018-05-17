import random
import traceback

from aecColors import aecColors
from aecGeomCalc import aecGeomCalc
from aecSpace import aecSpace
from aecSpacer import aecSpacer
from aecSpaceGroup import aecSpaceGroup
from aecSpaceDrawOCC import aecSpaceDrawOCC



siteWest = \
[
    (1335.5515, 2415.9574),
    (1263.2383, 2389.3717),
    (1398.0416, 2022.7068),
    (1551.4579, 1522.2420),
    (1696.0947, 1356.2240),
    (1900.4278, 2314.2330),
    (1900.2106, 2351.8979),
]

siteEast = \
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
        'area' : (200000, 300000),
        'color' : aecColors.aqua,
        'diameter' : (300, 500),
        'height' : 25,
        'level' : 0,
        'name' : 'venue',
        'plan' : (1, 9)
    },
    
    {
        'area' : (100000, 200000),
        'color' : aecColors.yellow,
        'diameter' : (500, 1000),
        'height' : 15,
        'level' : 0,
        'name' : 'conference',
        'plan' : (1, 13)
    },
    
    {
        'area' : (10000, 50000),
        'color' : aecColors.orange,
        'diameter' : (200, 500),
        'height' : 20,
        'level' : 0,
        'name' : 'event',
        'plan' : (1, 13)        
    },   
    
    {
        'area' : (350000, 500000),
        'color' : aecColors.purple,
        'diameter' : (100, 300),
        'height' : 15,
        'level' : 0,
        'name' : 'hotelluxury',
        'plan' : (1, 13)
    },
    
    {
        'area' : (100000, 150000),
        'color' : aecColors.purple,
        'diameter' : (100, 300),
        'height' : 12,
        'level' : 0,
        'name' : 'hotelbusiness',
        'plan' : (1, 13)
    },
    
    {
        'area' : (20000, 200000),
        'color' : aecColors.blue,
        'diameter' : (100, 300),
        'height' : 15,
        'level' : 0,
        'name' : 'office',
        'plan' : (1, 13)
    },
    
    {
        'area' : (500000, 700000),
        'color' : aecColors.granite,
        'diameter' : (500, 700),
        'height' : -20,
        'level' : 0,
        'name' : 'parking',
        'plan' : (2, 8)
    },
    
    {
        'area' : (250000, 500000),
        'color' : aecColors.green,
        'diameter' : (200, 500),       
        'height' : 20,
        'level' : 0,
        'name' : 'retail',
        'plan' : (1, 13)        
    },
    
    {
        'area' : (20000, 50000),
        'color' : aecColors.white,
        'diameter' : (100, 200),
        'height' : 15,
        'level' : 0,
        'name' : 'administration',
        'plan' : (1, 9)   
    }
]



def makeSpace(building, point, xWidth, yDepth):
    try:
        spcType = random.randint(building['plan'][0], building['plan'][1])
        space = aecSpace()
        if spcType == 1:
            space.makeBox(point, (xWidth, yDepth, 0))
            space.rotate(random.randint(0, 360))
            x = 0
            boundaries = random.randint(1, 5)
            tempFloor = aecSpace()
            while x < boundaries:
                if xWidth <= yDepth:
                    tempFloor.makeBox(point, 
                                          (random.randint(xWidth, yDepth), 
                                           random.randint(xWidth, yDepth), 0))
                else:
                    tempFloor.makeBox(point, 
                                          (random.randint(yDepth, xWidth), 
                                           random.randint(yDepth, xWidth), 0))                    
                tempFloor.rotate(random.randint(0, 360))
                space.addBoundary(tempFloor.getPointsFloor(points2D = True))
                x += 1               
        if spcType == 2: space.makeCylinder(point, (xWidth * 0.5))
        if spcType > 2 and spcType < 9: space.makePolygon(point, (xWidth * 0.5), spcType) 
        if spcType == 9: space.makeCross(point, (xWidth, yDepth, 0))        
        if spcType == 10: space.makeH(point, (xWidth, yDepth, 0))
        if spcType == 11: space.makeL(point, (xWidth, yDepth, 0))
        if spcType == 12: space.makeT(point, (xWidth, yDepth, 0))
        if spcType == 13: space.makeU(point, (xWidth, yDepth, 0))
        return space
    except Exception:
        traceback.print_exc()
        return None



def develop():
    geom = aecGeomCalc()
    spacer = aecSpacer()        
    sitWest = aecSpace()
    sitEast = aecSpace()    
    sitWest.setBoundary(siteWest)
    sitEast.setBoundary(siteEast)
    sitWest.setColor(aecColors.sand)
    sitEast.setColor(aecColors.sand)
    spaces = [sitWest, sitEast]
    spcGroup = aecSpaceGroup()
    for building in buildings:
        if random.randint(0, 1) == 0 : site = sitWest
        else: site = sitEast
        boundary = site.getPointsFloor()
        point = geom.findPoint(boundary)
        if not point: continue
        point = (point[0], point[1], 0)
        xWidth = random.randint(building['diameter'][0], building['diameter'][1])
        yDepth = random.randint(building['diameter'][0], building['diameter'][1])
        space = None
        while not space:
            space = makeSpace(building, point, xWidth, yDepth)
            if space:
                if not space.fitWithin(boundary) or \
                       space.getArea() < building['diameter'][0]*20: 
                    space = None
        space.setHeight(building['height'])
        space.setLevel(building['level'])
        space.setColor(building['color'])
        area = random.randint(building['area'][0], building['area'][1])    
        if building['name'] == 'parking':
            build = [space] + spacer.stackToArea(space, area)
        else:
            build = [space] + spacer.stackToArea(space, area)
        spcGroup.clearSpaces()
        spcGroup.addSpaces(build)
        if spcGroup.getCount() - 1 >= 10:
            spcGroup.scale((0.8, 0.8, 1), scalePoint = None, indices = list(range(10, spcGroup.getCount()))) 
        if spcGroup.getCount() - 1 >= 20:
            spcGroup.scale((0.8, 0.8, 1), scalePoint = None, indices = list(range(20, spcGroup.getCount())))  
        if spcGroup.getCount() - 1 >= 30:
            spcGroup.scale((0.8, 0.8, 1), scalePoint = None, indices = list(range(30, spcGroup.getCount())))
        build = spcGroup.getSpaces()
        spaces += build
    return spaces

x = 0
y = 0
spaces = []
vector = (-2000, 0, 0)
while y < 5:
    while x < 5:
        spcGroup = aecSpaceGroup()
        spcGroup.addSpaces(develop())
        vector = (vector[0] + 2000, vector[1], 0)        
        spcGroup.move(vector)
        spaces += spcGroup.getSpaces()               
        x += 1
    vector = (-2000, vector[1] + 2000, 0)    
    x = 0
    y += 1     
spaceDrawer = aecSpaceDrawOCC()
spaceDrawer.draw3D(spaces, displaySize = (1600, 900), update = False)
# update = True animates the example by updating the display after every space placement.
# About 60x slower to completion, but more interesting to watch.




