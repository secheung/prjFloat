import bge
from bge import logic

cont = logic.getCurrentController()
scene = logic.getCurrentScene()
own = cont.owner
ball = cont.sensors["ball"]
newBall = cont.actuators["newBall"]


if ball.positive:

    cont.activate(newBall)
