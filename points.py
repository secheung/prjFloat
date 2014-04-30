import bge
from bge import logic
import random

cont = logic.getCurrentController()
scene = logic.getCurrentScene()

player = cont.owner

if(player["life"] > 0):
    player["points"] = player["points"] + 1
else:
    player["gameOn"] = "Game Over"
    cont.activate(player.actuators["restartGame"])

if(player["points"] > 2000):
    player["level"] = 2

print("life: "+str(player["life"])+" points: " + str(player["points"]))

#print (player["life"])