import bge
from mathutils import *

import sys
sys.path.append("/usr/local/lib/python3.3/dist-packages")
from game_engine_rift.rift import PyRift

def poll(rift):
    rift.poll()
    bge.logic.rotation = Quaternion((rift.rotation[0],
        rift.rotation[1],
        rift.rotation[2],
        rift.rotation[3]))

try:
    poll(bge.logic.rift)
except AttributeError:
    bge.logic.rift = PyRift()
  
try:
    eu = bge.logic.rotation.to_euler()
except AttributeError:
    eu = Euler((0, 0, 0), 'XYZ')

scene = bge.logic.getCurrentScene()
cam = scene.active_camera
fix = Euler((-1.5707963705062866, 0, 0), 'XYZ')

rot = Euler((-eu.z, eu.y, -eu.x), 'XYZ')
rot.rotate(fix)
cam.worldOrientation = rot