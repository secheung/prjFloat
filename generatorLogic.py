import bge
from bge import logic
import random

cont = logic.getCurrentController()
scene = logic.getCurrentScene()
actuator = cont.actuators["addObj"]

generator = scene.objects['generator']


genProb = random.randint(1,100)
print (genProb)

xPos = random.randint(-5,5)

if(genProb > 95):
    generator.worldPosition = [xPos,-8,0]
    cont.activate(actuator)