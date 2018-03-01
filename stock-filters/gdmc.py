from random import *
from numpy import *
from pymclevel import MCSchematic, MCLevel, BoundingBox
from mcplatform import *

from myglobals import *
import boxutils as bu
from level_extensions import inject as LVinject

# name to show in filter list
displayName = "Settlement Generator"

OPT_Material = "Material"

inputs = (
	(displayName, "label"),
	(OPT_Material, materials.Cobblestone),
	)

MAT_WALLS = materials["Spruce Wood Planks"]
MAT_WINDOWS = materials["Glass"]

def perform(level, box, options):
    LVinject(level)
    
    level.fill(bu.ceiling(box), MAT_WALLS)
    level.fill(bu.floor(box), MAT_WALLS)
    for wall in bu.walls(box):
        level.fill(wall, MAT_WALLS)
        placeWindows(level, wall)
    
    placeDoor( level, Vector(box.minx, box.miny+1, (box.minz + box.maxz)/2) )

########################################################################
########################################################################

DOOR_LOWER_DATA = {
    Direction.East  : 0,
    Direction.South : 1,
    Direction.West  : 2,
    Direction.North : 3
}

#DOOR_UPPER_DATA = [8, 9] # upper unpowered L/R hinge

def placeDoor(level, position, direction = Direction.East, materialId = materials.blocksMatching("Oak Door")[0].ID):
    level.setMaterialAt(position, (materialId, DOOR_LOWER_DATA[direction]))
    level.setMaterialAt(position+Direction.Up, (materialId, 8))

def placeWindows(level, wall):
    shortSide = 0 if wall.size.x == 1 else 2
    longSide = 2-shortSide
    
    shrink = [-1, -1, -1]
    shrink[shortSide] = 0
    wall =  wall.expand(*shrink)
    
    level.fill(wall, MAT_WINDOWS)
