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
    
    cont = bge.logic.getCurrentController()
    own = cont.owner
#pressup = cont.sensors["up"]
#pressdown = cont.sensors["down"]
    move = cont.actuators["move"]
#speed = move.dLoc[1]

#if pressup.positive:
#    speed = speed + 0.05
#    move.dLoc = [0.0, speed, 0.0]
#    cont.activate(move)

#elif pressdown.positive:
#    speed = speed - 0.05
#    cont.deactivate(move)
#    move.dLoc = [0.0, speed, 0.0]


    
#if foo is None:
#    foo = PyBalanceBoard()
#if(foo.hasWiiMotes()):
#    foo.poll()
    

#while foo.hasWiiMotes():
    foo.poll()
  #print("%s, %s, %s, %s, %s",foo.total,foo.topLeft,foo.topRight,foo.bottomLeft,foo.bottomRight)
  #foo.printSensors()
    pos = calcCOP(foo.topRight, foo.topLeft, foo.bottomRight, foo.bottomLeft)
    print("X: %s, Y: %s" % (pos[0], pos[1]))
  
    if(UpDir(foo)):
            dx = xLinSpeed(pos[0])
            dy = yLinSpeed(pos[1])
            move.dLoc = [dx,dy,0.0]
            cont.activate(move)
    else:
        move.dLoc = [0.0, 0.0, 0.0] 
        cont.deactivate(move)
    

    
    
#if(TopDir()):
#    move.dLoc = [0.0, 0.05, 0.0]
#    cont.activate(move)

#move.dLoc = [0.0, 0.0, 0.0]
  
#print("ended")
  