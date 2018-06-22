from random import randint, uniform

from aecSpace.aecColor import aecColor
from aecSpace.aecPoint import aecPoint
from aecSpace.aecShaper import aecShaper
from aecSpace.aecSpace import aecSpace
from aecSpace.aecSpacer import aecSpacer
from aecSpace.aecSpaceGroup import aecSpaceGroup
from aecSpace.aecSpaceDrawOCC import aecSpaceDrawOCC

# from hypar import glTF

def makeTower():
    
    def randomFloor(point):
        try:
            floor = aecSpace()
            shaper = aecShaper()
            floorSizeX = uniform(60, 100)
            floorSizeY = uniform(60, 100)
            floorHeight = uniform(10, 20)
            floorType = randint(1, 11)
            width = uniform(33, 45)
            depth = uniform(33, 45)
            xOffset = uniform(10, 90)
            yOffset = uniform(10, 90)
            if floorType == 1:
                floor.boundary = shaper.makeBox(point, floorSizeX, floorSizeY)
                floor.rotate(uniform(0, 360))
                x = 0
                boundaries = uniform(1, 5)
                tempFloor = aecSpace()
                while x < boundaries:
                    tempFloor.boundary = shaper.makeBox(origin = point, 
                                                        xSize = uniform(65, 100), 
                                                        ySize = uniform(65, 100))
                    tempFloor.rotate(uniform(0, 360))
                    floor.add(tempFloor.points_floor)
                    x += 1
            if floorType == 2:
                floor.boundary = shaper.makeCylinder(aecPoint(point.x + (floorSizeX * 0.5),
                                                              point.y + (floorSizeY * 0.5)),
                                                              (floorSizeX * 0.5))
            if floorType > 2 and floorType < 9:
                floor.boundary = shaper.makePolygon(aecPoint(point.x + (floorSizeX * 0.5), 
                                                             point.y + (floorSizeY * 0.5)),
                                                             (floorSizeX * 0.5), floorType)
            if floorType == 9:
                floor.boundary = shaper.makeCross(point, 
                                                  xSize = floorSizeX, 
                                                  ySize = floorSizeY,
                                                  xAxis = xOffset,
                                                  yAxis = yOffset)                                             
            if floorType == 10:
                floor.boundary = shaper.makeH(point, 
                                              xSize = floorSizeX, 
                                              ySize = floorSizeY,
                                              xWidth1 = width, 
                                              xWidth2 = depth,
                                              yDepth = depth)
            if floorType == 11:
                floor.boundary = shaper.makeU(point, 
                                              xSize = floorSizeX, 
                                              ySize = floorSizeY,
                                              xWidth1 = width, 
                                              xWidth2 = depth, 
                                              yDepth = depth)
            floor.rotate(uniform(0, 360))
            floor.height = floorHeight
            return floor
        except:
            return False
              
    def stackTower():
        spacer = aecSpacer()
        levels = randint(5, 70)
        floor = randomFloor(aecPoint(0, 0, 0))
        if not floor: return
        height = floor.height
        floors = [floor] + spacer.stack(floor, levels - 1)
        if uniform(1, 3) == 1:
            plinth = aecSpace()
            plinthLevels = randint(1, 3)
            plinthHeight = height * plinthLevels
            plinth.wrap(floor.points_floor)
            plinth.height = plinthHeight       
            pScale = uniform(1, 2)
            plinth.scale(pScale, pScale, 1)
            floors = floors[plinthLevels:]
            floors = [plinth] + floors
        colors = [aecColor.blue, aecColor.green]
        tower = aecSpaceGroup()
        tower.spaces = floors
        tower.setColor(colors[randint(0, 1)])
        tower.rotate(uniform(0, 360))
        if levels >= 10:
            index = 10
            while index < levels:
                tower.scale(0.8, 0.8, 1, index = index)
                index += 1
        if levels >= 30:
            index = 30
            while index < levels:
                tower.scale(0.8, 0.8, 1, index = index)
                index += 1                
        return tower.spaces
    
    return stackTower()

# end aecSpaceRandomTower

  
spaces = makeTower()
spaceDrawer = aecSpaceDrawOCC()
print(spaceDrawer.draw3D(spaces, displaySize = (1600, 900), update = False))
# update = True animates the example by updating the display after every space placement.
# About 60x slower to completion, but more interesting to watch.


