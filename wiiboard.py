#!/usr/bin/python
import bge
from balanceboard import PyBalanceBoard
#from boardlib import *

#Global Variables
WIIXMAX = 430 #length in mm
WIIYMAX = 235 #width in mm
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
    
def TopDir():
    
    if(copX > topThresh):
        return 1
    
def BotDir():
    
    if(copX < botThresh):
        return 1   

def RightDir():
    
    if(copY > topThresh):
        return 1
    
def LeftDir():
    
    if(copY < topThresh):
        return 1  

def xLinSpeed(x):
    
    b = -0.05
    m = 0.000233
    y = m*x + b
    return y
    
def yLinSpeed(x):
    
    b = -0.05
    m = 0.000426
    y = m*x + b
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
    

    