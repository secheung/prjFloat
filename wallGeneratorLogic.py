import bge
from bge import logic
import random
import math

def main():
    cont = logic.getCurrentController()
    scene = logic.getCurrentScene()
    actuator = cont.actuators["addObj"]

    generator = cont.owner
    generator['wallPulse'] = generator['wallPulse'] + 1

    player = scene.objects['player']

    if(generator['wallPulse'] == 5):
        generator.worldPosition = [generator["wallPos"],8,0]
        cont.activate(actuator)
        generator['wallPulse'] = 0

    if(player["level"] == 2):
        generator["degree"] = generator["degree"] + 1
        generator["wallPos"] = generator["wallPos"] + sineWave(generator["degree"])

    if(generator["degree"] > 360):
        generator["degree"] = 0

def sineWave(degree):
    return math.sin(math.radians(degree)) * 0.1