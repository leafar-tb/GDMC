from numpy import clip as npclip
from pymclevel import BoundingBox

from myglobals import Vector, Direction

def floor(box):
    return BoundingBox(box.origin, (box.width, 1, box.length))

def ceiling(box):
    return BoundingBox((box.minx, box.maxy-1, box.minz), (box.width, 1, box.length))

def walls(box):
    return [ wall(box, Direction.North), wall(box, Direction.East),
        wall(box, Direction.South), wall(box, Direction.West) ]

def wall(box, direction):
    if direction == Direction.North:
        return BoundingBox(box.origin, (box.width, box.height, 1))
    if direction == Direction.East:
        return BoundingBox((box.maxx-1, box.miny, box.minz), (1, box.height, box.length))
    if direction == Direction.South:
        return BoundingBox((box.minx, box.miny, box.maxz-1), (box.width, box.height, 1))
    if direction == Direction.West:
        return BoundingBox(box.origin, (1, box.height, box.length))
    
    # not walls as such, but close enough
    if direction == Direction.Up:
        return ceiling(box)
    if direction == Direction.Down:
        return floor(box)

def clip(position, box):
    return Vector( npclip( position, box.origin, box.maximum) )
