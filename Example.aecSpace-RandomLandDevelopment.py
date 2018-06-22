from random import randint, uniform
import traceback

from aecSpace.aecColor import aecColor
from aecSpace.aecPoint import aecPoint
from aecSpace.aecShaper import aecShaper
from aecSpace.aecSpace import aecSpace
from aecSpace.aecSpacer import aecSpacer
from aecSpace.aecSpaceGroup import aecSpaceGroup
from aecSpace.aecSpaceDrawOCC import aecSpaceDrawOCC

siteWest = \
[
    aecPoint(1335.5515, 2415.9574),
    aecPoint(1263.2383, 2389.3717),
    aecPoint(1398.0416, 2022.7068),
    aecPoint(1551.4579, 1522.2420),
    aecPoint(1696.0947, 1356.2240),
    aecPoint(1900.4278, 2314.2330),
    aecPoint(1900.2106, 2351.8979),
]

siteEast = \
[
    aecPoint(2000.1994, 2289.2733),
    aecPoint(2700.4829, 2289.2733),
    aecPoint(2700.4829, 1737.8546),
    aecPoint(2108.5229, 1263.0727),
    aecPoint(1792.2478, 1263.0727),
    aecPoint(1771.8803, 1282.6400)
]

buildings = \
[
    {
        'area' : (200000, 300000),
        'color' : aecColor.aqua,
        'diameter' : (300, 500),
        'height' : 25,
        'level' : 0,
        'name' : 'venue',
        'plan' : (1, 9)
    },
    
    {
        'area' : (100000, 200000),
        'color' : aecColor.yellow,
        'diameter' : (500, 1000),
        'height' : 15,
        'level' : 0,
        'name' : 'conference',
        'plan' : (1, 13)
    },
    
    {
        'area' : (10000, 50000),
        'color' : aecColor.orange,
        'diameter' : (200, 500),
        'height' : 20,
        'level' : 0,
        'name' : 'event',
        'plan' : (1, 13)        
    },   
    
    {
        'area' : (350000, 500000),
        'color' : aecColor.purple,
        'diameter' : (100, 300),
        'height' : 15,
        'level' : 0,
        'name' : 'hotelluxury',
        'plan' : (1, 13)
    },
    
    {
        'area' : (100000, 150000),
        'color' : aecColor.purple,
        'diameter' : (100, 300),
        'height' : 12,
        'level' : 0,
        'name' : 'hotelbusiness',
        'plan' : (1, 13)
    },
    
    {
        'area' : (20000, 200000),
        'color' : aecColor.blue,
        'diameter' : (100, 300),
        'height' : 15,
        'level' : 0,
        'name' : 'office',
        'plan' : (1, 13)
    },
    
    {
        'area' : (500000, 700000),
        'color' : aecColor.granite,
        'diameter' : (500, 700),
        'height' : -20,
        'level' : 0,
        'name' : 'parking',
        'plan' : (2, 8)
    },
    
    {
        'area' : (250000, 500000),
        'color' : aecColor.green,
        'diameter' : (200, 500),       
        'height' : 20,
        'level' : 0,
        'name' : 'retail',
        'plan' : (1, 13)        
    },
    
    {
        'area' : (20000, 50000),
        'color' : aecColor.white,
        'diameter' : (100, 200),
        'height' : 15,
        'level' : 0,
        'name' : 'administration',
        'plan' : (1, 9)   
    }
]

def makeSpace(building, point, xSize, ySize):
    try:
        spcType = randint(building['plan'][0], building['plan'][1])
        space = aecSpace()
        shaper = aecShaper()
        if spcType == 1:
            space.boundary = shaper.makeBox(point, xSize, ySize)
            space.rotate(randint(0, 360))
            x = 0
            boundaries = randint(1, 5)
            tempFloor = aecSpace()
            while x < boundaries:
                if xSize <= ySize:
                    tempFloor.boundary = \
                    shaper.makeBox(point, uniform(xSize, ySize), uniform(xSize, ySize))
                else:
                    tempFloor.boundary = \
                    shaper.makeBox(point, uniform(ySize, xSize), uniform(ySize, xSize))                   
                tempFloor.rotate(uniform(0, 360))
                space.add(tempFloor.points_floor)
                x += 1  
        if spcType == 2:  space.boundary = shaper.makeCylinder(point, (xSize * 0.5))
        if spcType > 2 and spcType < 9: 
                          space.boundary = shaper.makePolygon(point, (xSize * 0.5), spcType) 
        if spcType == 9:  space.boundary = shaper.makeCross(point, xSize, ySize)     
        if spcType == 10: space.boundary = shaper.makeH(point, xSize, ySize) 
        if spcType == 11: space.boundary = shaper.makeL(point, xSize, ySize) 
        if spcType == 12: space.boundary = shaper.makeT(point, xSize, ySize) 
        if spcType == 13: space.boundary = shaper.makeU(point, xSize, ySize)
        return space
    except Exception:
        traceback.print_exc()
        return None

def develop():
    spacer = aecSpacer()        
    sitWest = aecSpace()
    sitEast = aecSpace()    
    sitWest.boundary = siteWest
    sitEast.boundary = siteEast
    sitWest.color = aecColor.sand
    sitEast.color = aecColor.sand
    spaces = [sitWest, sitEast]
    spcGroup = aecSpaceGroup()
    for building in buildings:
        if randint(0, 1) == 0 : site = sitWest
        else: site = sitEast
        boundary = site.points_floor
        point = site.point_ceiling
        xWidth = randint(building['diameter'][0], building['diameter'][1])
        yDepth = randint(building['diameter'][0], building['diameter'][1])
        space = None
        while not space:
            space = makeSpace(building, point, xWidth, yDepth)
            if not space.fitWithin(boundary): 
                point = site.point_ceiling
                space = None
        space.height = building['height']
        space.level = building['level']
        space.color = building['color']
        area = randint(building['area'][0], building['area'][1])    
        if building['name'] == 'parking': build = [space] + spacer.stackToArea(space, area)
        else: build = [space] + spacer.stackToArea(space, area)
        spcGroup.clear()
        spcGroup.add(build)
        levels = spcGroup.count
        if building['name'] != 'parking':
            if levels >= 10:
                index = 10
                while index < levels:
                    spcGroup.scale(0.8, 0.8, 1, index = index)
                    index += 1
            if levels >= 20:
                index = 20
                while index < levels:
                    spcGroup.scale(0.8, 0.8, 1, index = index)
                    index += 1                   
            if levels >= 30:
                index = 30
                while index < levels:
                    spcGroup.scale(0.8, 0.8, 1, index = index)
                    index += 1           
        build = spcGroup.spaces
        spaces += build
    return spaces

x = 0
y = 0
spaces = []
vector = (-2000, 0, 0)
while y < 4:
    while x < 4:
        spcGroup = aecSpaceGroup()
        spcGroup.add(develop())
        vector = (vector[0] + 2000, vector[1], 0)        
        spcGroup.moveBy(vector[0], vector[1], vector[2])
        spaces += spcGroup.spaces               
        x += 1
    vector = (-2000, vector[1] + 2000, 0)    
    x = 0
    y += 1     
spaceDrawer = aecSpaceDrawOCC()
spaceDrawer.draw3D(spaces, displaySize = (1600, 900), update = True)
# update = True animates the example by updating the display after every space placement.
# About 60x slower to completion, but more interesting to watch.




