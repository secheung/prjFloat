import bge
from bge import logic
import random

cont = logic.getCurrentController()
scene = logic.getCurrentScene()
sensor = cont.sensors["Collision"]

player = cont.owner

if(player["life"] > 0):
    player["life"] = player["life"] - 10

#print (player["life"])