import random

from aecSpace.aecColor import aecColor
from aecSpace.aecPoint import aecPoint
from aecSpace.aecShaper import aecShaper
from aecSpace.aecSpace import aecSpace
from aecSpace.aecSpacer import aecSpacer
from aecSpace.aecSpaceDrawOCC import aecSpaceDrawOCC

shaper = aecShaper()

def placeBath(space: aecSpace):
    origin = space.origin_floor
    point = aecPoint(origin.x + 1, origin.y + 2750)
    bath = aecSpace()
    bath.boundary = shaper.makeBox(point, 2750, 1380)
    bath.height = 2749
    bath.level = origin.z
    bath.color = aecColor.blue
    bath.color.alpha = 125
    point = aecPoint(point.x, point.y + 390)
    tank = aecSpace()
    tank.boundary = shaper.makeBox(point, 200, 600)
    tank.height = 330
    tank.level = origin.z + 400
    tank.color = aecColor.white
    point = aecPoint(point.x + 400, point.y + 300)
    bowl = aecSpace()
    bowl.boundary = shaper.makeCylinder(point, 270)
    bowl.height = 410
    bowl.level = origin.z
    bowl.color = aecColor.white 
    point = aecPoint(origin.x + 2270, origin.y + 2750)
    vanity = aecSpace()
    vanity.boundary = shaper.makeBox(point, 480, 1380)  
    vanity.height = 780
    vanity.level = origin.z
    vanity.color = aecColor.white
    return [bath, tank, bowl, vanity]

def placeBathFixtures(space: aecSpace):
    origin = space.origin_floor
    point = aecPoint(origin.x + 1, origin.y + 3129)
    tub = aecSpace()
    tub.boundary = shaper.makeBox(point, 2000, 1000)
    tub.height = 450
    tub.level = origin.z
    tub.color = aecColor.white
    point = aecPoint(origin.x + 1, origin.y + 150)
    tank = aecSpace()
    tank.boundary = shaper.makeBox(point, 200, 600)
    tank.height = 330
    tank.level = origin.z + 400
    tank.color = aecColor.white
    point = aecPoint(point.x + 400, point.y + 300)
    bowl = aecSpace()
    bowl.boundary = shaper.makeCylinder(point, 270)
    bowl.height = 410
    bowl.level = origin.z
    bowl.color = aecColor.white
    point = aecPoint(origin.x + 1, origin.y + 1000)
    vanity = aecSpace()
    vanity.boundary = shaper.makeBox(point, 480, 1500) 
    vanity.height = 780
    vanity.level = origin.z
    vanity.color = aecColor.white
    mirror = aecSpace()
    mirror.boundary = shaper.makeBox(point, 10, 1500)
    mirror.height = 1500
    mirror.level = point.z + 1000
    mirror.color = aecColor.white  
    return [tub, tank, bowl, vanity, mirror]

def placeBed(space):
    origin = space.origin_floor
    point = aecPoint(origin.x + 1500, origin.y + 1)
    bed = aecSpace()
    bed.boundary = shaper.makeBox(point, 1500, 2000)
    bed.height = 600
    bed.color = aecColor.white
    point = aecPoint(origin.x + 1600, origin.y + 20)
    pillows = aecSpace()
    pillows.boundary = shaper.makeBox(point, 1300, 400)
    pillows.height = 150
    pillows.level = origin.z + 600
    pillows.color = aecColor.white
    return [bed, pillows]

def placeCloset(space):
    origin = space.origin_floor
    point = aecPoint(origin.x + 1, origin.y + 1)
    closet = aecSpace()
    closet.boundary = shaper.makeBox(point, 700, 2750)
    closet.height = 2749
    closet.color = aecColor.orange
    return [closet]

def placeFurniture(space):
    origin = space.origin_floor
    point = aecPoint(origin.x + 1032.5, origin.y)
    couchSeat = aecSpace()
    couchSeat.boundary = shaper.makeBox(point, 2000, 800)
    couchSeat.height = 370
    couchSeat.color = aecColor.white
    couchBack = aecSpace()
    couchBack.boundary = shaper.makeBox(point, 2000, 200)
    couchBack.height = 330
    couchBack.level = origin.z + 380
    couchBack.color = aecColor.white
    point = aecPoint(point.x + 300, point.y + 1200)
    table = aecSpace()
    table.boundary = shaper.makeBox(point, 1400, 600)
    table.height = 370
    table.color = aecColor.white
    return [couchSeat, couchBack, table]

def placeKitchen(space):
    origin = space.origin_floor
    point = aecPoint(origin.x + 1, origin.y + 1)
    kitchen = aecSpace()
    kitchen.boundary = shaper.makeL(origin = point, xSize = 3097.5, ySize = 3097.5, xWidth = 750, yDepth = 750)
    kitchen.height = 1000
    kitchen.rotate(180, space.center_floor)
    kitchen.color = aecColor.white
    return [kitchen]

def makeHouse(point, module):    
    space = aecSpace()
    spacer = aecSpacer()
    space.boundary = shaper.makeBox(point, module, module)
    space.height = 2750
    baths = []
    beds = []
    closets = []
    fixtures = []
    furniture = []
    kitchens = []
    space.color.alpha = 125
    colors = \
    [
         aecColor.aqua,
         aecColor.blue, 
         aecColor.green, 
         aecColor.purple,
         aecColor.yellow
    ]
    rotations = [0, 90, 180]
    row = random.randint(1, 3)
    spaces = spacer.row(space, row)
    spaces += [space]
    extSpaces = []
    for unit in spaces:
        row = random.randint(0, 3)
        if row > 0: 
            extSpaces += spacer.row(unit, row, gap = 0, xAxis = False)
    spaces += extSpaces
    for unit in spaces:
        color = colors[random.randint(0, len(colors) - 1)]
        if color == aecColor.aqua:
            tmpFurn = placeFurniture(unit)
            rotation = rotations[random.randint(0, 2)]
            for furn in tmpFurn:
                furn.rotate(rotation, unit.center_floor)
            furniture += tmpFurn
            colors.remove(aecColor.aqua)  
        if color == aecColor.blue:
            tmpFurn = placeBathFixtures(unit)
            rotation = rotations[random.randint(0, 2)]
            for furn in tmpFurn:
                furn.rotate(rotation, unit.center_floor)
            fixtures += tmpFurn            
            colors.remove(aecColor.blue)  
        if color == aecColor.purple:
            tmpFurn = placeKitchen(unit)
            rotation = rotations[random.randint(0, 2)]
            for furn in tmpFurn:
                furn.rotate(rotation, unit.center_floor)
            kitchens += tmpFurn
            colors.remove(aecColor.purple) 
        if color == aecColor.green:
            tmpFurn = placeBed(unit)
            rotation = rotations[random.randint(0, 2)]
            for furn in tmpFurn:
                furn.rotate(rotation, unit.center_floor)
            beds += tmpFurn            
            if random.randint(0, 1) == 0:
                tmpFurn = placeCloset(unit)
                for furn in tmpFurn:
                    furn.rotate(rotation, unit.center_floor)                
                closets += tmpFurn
            if random.randint(0, 2) == 0:
                tmpFurn = placeBath(unit)
                for furn in tmpFurn:
                    furn.rotate(rotation, unit.center_floor)                    
                baths += tmpFurn
        if color == aecColor.yellow:
            colors.remove(aecColor.yellow)                  
        unit.color = color
        unit.color.alpha = 125
    return spaces + baths + beds + closets + fixtures + furniture + kitchens

spaces = []
x = 0
y = 0
point = aecPoint(-20000, 0, 0)
while y < 4:
    while x < 4:
        spaces += makeHouse(point, 4130)
        point.x += 20000
        x += 1
    point.x = -20000
    point.y += 20000
    x = 0
    y += 1
spaceDrawer = aecSpaceDrawOCC()
spaceDrawer.draw3D(spaces, displaySize = (1600, 900), update = True)
# update = True will animate the example by updating the display after every space placement.
# About 60x slower to completion, but more interesting to watch.