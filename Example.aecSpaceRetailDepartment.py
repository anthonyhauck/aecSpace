from random import randint, uniform

from aecSpace.aecColor import aecColor
from aecSpace.aecPoint import aecPoint
from aecSpace.aecShaper import aecShaper
from aecSpace.aecSpace import aecSpace
from aecSpace.aecSpaceGroup import aecSpaceGroup
from aecSpace.aecSpacer import aecSpacer
from aecSpace.aecSpaceDrawOCC import aecSpaceDrawOCC

# Create class instances.

spacer = aecSpacer()
shaper = aecShaper()
spaceDrawer = aecSpaceDrawOCC()

def makeCheckOut():
    components = aecSpaceGroup();
    base = aecSpace();
    base.boundary = shaper.makeBox(aecPoint(), 75, 150)
    base.height = 100
    top = aecSpace();
    top.boundary = shaper.makeU(aecPoint(), 
                                xSize = 170, 
                                ySize = 80, 
                                xWidth1 = 20, 
                                xWidth2 = 20, 
                                yDepth = 20)
    top.height = 30
    top.rotate(90)
    top.moveBy(-25, 50, 100)

    components.add([base, top])
    components.setColor(aecColor.sand)
    return components    

def makeRackCross():
    components = aecSpaceGroup();
    base = aecSpace();
    base.boundary = shaper.makeCylinder(aecPoint(), radius = 40)
    base.height = 5
    support = aecSpace()
    support.boundary = shaper.makeCylinder(aecPoint(), radius = 5)
    support.height = 157
    support.moveBy(0, 0, 5)
    top = aecSpace();
    top.boundary = shaper.makeCross(aecPoint(-50, -50), 100, 100, xWidth = 10 , yDepth = 10)
    top.height = 4
    top.moveBy(0, 0, 162)
    components.add([base, support, top])
    components.rotate(uniform(0, 360), base.center_floor)
    components.setColor(aecColor.sand)
    return components    

def makeRackRound():
    components = aecSpaceGroup();
    base = aecSpace();
    base.boundary = shaper.makeCylinder(radius = 40)
    base.height = 5
    support = aecSpace();
    support.boundary = shaper.makeCylinder(radius = 5)
    support.height = 125
    support.moveBy(0, 0, 5)
    top = aecSpace();
    top.boundary = shaper.makeCylinder(radius = 50)
    top.height = 3
    top.moveBy(0, 0, 130)
    components.add([base, support, top])
    components.setColor(aecColor.sand)
    return components    

def makeShelfSingle(length = 200):
    components = aecSpaceGroup();
    base = aecSpace();
    base.boundary = shaper.makeBox(aecPoint(), 50, length)
    base.height = 25
    divider = aecSpace()
    divider.boundary = shaper.makeBox(aecPoint(), 4, length - 10)
    divider.height = 125
    divider.moveTo(fromPnt = aecPoint(), toPnt = aecPoint(0, 5, 25))
    lowShelfFront = aecSpace()
    lowShelfFront.boundary = shaper.makeBox(aecPoint(), 43, length - 10)
    lowShelfFront.height = 2
    lowShelfFront.moveTo(fromPnt = aecPoint(), toPnt = aecPoint(4, 5, 65))
    highShelfFront = spacer.copy(lowShelfFront, 0, 0, 40)
    components.add([base, divider, lowShelfFront, highShelfFront])
    components.rotate(uniform(0, 360), base.center_floor)
    components.setColor(aecColor.sand)
    return components

def makeShelfDouble(length = 200):
    components = aecSpaceGroup();
    base = aecSpace();
    base.boundary = shaper.makeBox(aecPoint(), 100, length)
    base.height = 25
    divider = aecSpace();
    divider.boundary = shaper.makeBox(aecPoint(), 4, length - 10)
    divider.height = 125
    divider.moveTo(fromPnt = aecPoint(), toPnt = aecPoint(48, 5, 25))
    lowShelfFront = aecSpace();
    lowShelfFront.boundary = shaper.makeBox(aecPoint(), 43, length - 10)
    lowShelfFront.height = 2                     
    lowShelfFront.moveTo(fromPnt = aecPoint(), toPnt = aecPoint(52, 5, 65))
    lowShelfBack = spacer.copy(lowShelfFront)
    lowShelfBack.mirror([aecPoint(50, 0), aecPoint(50, 500)])
    highShelfFront = spacer.copy(lowShelfFront, z = 40)
    highShelfBack = spacer.copy(lowShelfBack, z = 40)
    components.add([base, divider, lowShelfFront, lowShelfBack, highShelfFront, highShelfBack])
    components.rotate(uniform(0, 360), base.center_floor)
    components.setColor(aecColor.sand)
    return components

def makeShelfTiered(length = 150):
    components = aecSpaceGroup();
    lowShelf = aecSpace();  
    lowShelf.boundary = shaper.makeBox(aecPoint(), 100, length)
    lowShelf.height = 3
    lowShelf.moveBy(z = 27)
    midShelf = spacer.copy(lowShelf, z = 30)
    midShelf.scale(0.75, 0.75, 1)
    topShelf = spacer.copy(midShelf, z = 30)
    topShelf.scale(0.75, 0.75, 1)   
    base = spacer.copy(lowShelf, z = -27)
    base.scale(0.75, 0.75, 9)
    support1 = spacer.copy(base, z = 30)
    support1.scale(0.25, 0.5, 1)
    support1.height = 27
    support2 = spacer.copy(support1, z = 30)
    components.add([base, lowShelf, midShelf, topShelf, support1, support2])
    components.rotate(uniform(0, 360), base.center_floor)
    components.setColor(aecColor.sand)
    return components

def makeDepartment():
    moveBy = [100, 100, 0]
    floor = aecSpace()
    floor.boundary = shaper.makeBox(aecPoint(), 1700, 2100)
    floor.level = -1
    floor.height = 1
    floor.color = aecColor.blue
    fixtures= [floor]
    checkout = makeCheckOut()
    checkout.moveBy(moveBy[0], moveBy[1], moveBy[2])
    fixtures += checkout.spaces
    x = 0
    displace = 350
    while x < 4:
        moveBy[0] += displace
        fixType = randint(0, 4)
        if fixType == 0: nxtFixture = makeRackCross()
        if fixType == 1: nxtFixture = makeRackRound()
        if fixType == 2: nxtFixture = makeShelfSingle()
        if fixType == 3: nxtFixture = makeShelfDouble()
        if fixType == 4: nxtFixture = makeShelfTiered()     
        nxtFixture.moveBy(moveBy[0], moveBy[1], moveBy[2])
        fixtures += nxtFixture.spaces
        x += 1   
    x = 0
    y = 0
    while y < 5:
        moveBy = [100, moveBy[1] + displace, 0]
        while x < 5:
            fixType = randint(0, 4)
            if fixType == 0: nxtFixture = makeRackCross()
            if fixType == 1: nxtFixture = makeRackRound()
            if fixType == 2: nxtFixture = makeShelfSingle()
            if fixType == 3: nxtFixture = makeShelfDouble()
            if fixType == 4: nxtFixture = makeShelfTiered()     
            nxtFixture.moveBy(moveBy[0], moveBy[1], moveBy[2])
            fixtures += nxtFixture.spaces         
            moveBy[0] = moveBy[0] + displace
            x += 1
        x = 0
        y += 1   
    return fixtures
    
x = 0
y = 0
displace = [-2000, -2400, 0]
spaces = []

while y < 1:
    displace[1] += 2400
    while x < 1:
        displace[0] += 2000
        department = makeDepartment()
        for space in department: space.moveBy(displace[0], displace[1])
        spaces += department
        x += 1
    x = 0
    displace[0] = -2000
    y += 1
     
spaceDrawer.draw3D(spaces, displaySize = (1600, 900), update = True)
# update = True will animate the example by updating the display after every space placement.
# About 60x slower to completion, but more interesting to watch.