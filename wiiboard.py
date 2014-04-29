#!/usr/bin/python
import bge
from balanceboard import PyBalanceBoard

#Global Variables
maxSpeedx = 1
maxSpeedy = 1
WIIXMAX = 430 #length in mm
WIIYMAX = 235 #width in mm
mX = 2*maxSpeedx/WIIXMAX
mY = 2*maxSpeedy/WIIYMAX
topThresh = 300
botThresh = 100
rightThresh = 150
leftThresh =  50
heightThresh = 30
copX = 0
copY = 0

#initialize and calibrate
foo = None

#**Functions**

def UpDir(foo):

    if(foo.getTotal() > heightThresh):
        return 1

def xLinSpeed(x):
    
    b = -maxSpeedx
    y = mX*x + b
    return y
    
def yLinSpeed(x):
    
    b = -maxSpeedy
    y = mY*x + b
    return y    

def calcCOP(tr,tl,br,bl):
    netForce = tr + tl + br + bl
    if((netForce < 50) and (netForce > -50)):
        netForce = 0
        copX = WIIXMAX / 2
        copY = WIIYMAX / 2
    if(netForce != 0):
        copX = ((((tr+br) - (tl+bl)) / (netForce*1.0))+1) * (WIIXMAX/2)
        copY = ((((tr+tl) - (br+bl)) / (netForce*1.0))+1) * (WIIYMAX/2)
    values = [copX ,copY]
    return values

#**Main**
def main():
    
    global foo
    
    if foo is None:
        foo = PyBalanceBoard()    
    
    if(not foo.hasWiiMotes()):
        foo = None
    else:
    
        cont = bge.logic.getCurrentController()
        own = cont.owner
        move = cont.actuators["move"]
        
        #Need two polls for refresh
        foo.poll()
        foo.poll()
        pos = calcCOP(foo.topRight, foo.topLeft, foo.bottomRight, foo.bottomLeft)
        print("%s, %s, %s, %s, %s" % (foo.getTotal(), foo.topRight, foo.topLeft, foo.bottomRight, foo.bottomLeft))
        if(UpDir(foo)):
                dx = xLinSpeed(pos[0])
                dy = yLinSpeed(pos[1])
                move.dLoc = [dx,dy,0.0]
                cont.activate(move)
        else:
            move.dLoc = [0.0, 0.0, 0.0] 
            cont.deactivate(move)
    

    