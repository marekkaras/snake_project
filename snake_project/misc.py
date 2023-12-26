# -*- coding: utf-8 -*-
from enum import Enum
from collections import namedtuple


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    
Point = namedtuple('Point', 'x, y')

BLOCK_SIZE = 20
SPEED = 20
