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

########################################################################

def splitAlongAxisAt(box, axis, position, isWorldPosition=False):
    if not isWorldPosition:
        position += box.origin[axis]
    
    if position <= box.origin[axis] or position >= box.maximum[axis]:
        return [box]
    
    size = list(box.size)
    size[axis] = position - box.origin[axis]
    b1 = BoundingBox(box.origin, size)
    
    origin2 = list(box.origin)
    origin2[axis] = b1.maximum[axis]
    size[axis] = box.maximum[axis] - origin2[axis]
    b2 = BoundingBox(origin2, size)
    
    return [b1, b2]

########################################################################

class BoundingBox2D:
    
    def __init__(self, box):
        assert isinstance(box, BoundingBox)
        assert 1 in box.size
        self.box = box
        
        # try mapping x to x and y to y
        self.x_axis = 0 if box.size.index(1) != 0 else 2
        self.y_axis = 1 if box.size.index(1) != 1 else 2

    @property
    def width(self):
        return self.box.size[self.x_axis]
    
    @property
    def height(self):
        return self.box.size[self.y_axis]
    
    @property
    def size(self):
        return self.width, self.height
    
    @property
    def positions(self):
        return self.box.positions
    
    def expand(self, dx, dy):
        deltas = [0, 0, 0]
        deltas[self.x_axis] = dx
        deltas[self.y_axis] = dy
        return BoundingBox2D( self.box.expand( *deltas ) )
    
    def __getitem__(self, (x,y)):
        offset = [0, 0, 0]
        offset[self.x_axis] = x
        offset[self.y_axis] = y
        return self.box.origin + Vector( *offset )
