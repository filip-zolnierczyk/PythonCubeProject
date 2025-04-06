from enum import Enum

class Orientation(Enum):
    FRONT = 0
    RIGHT = 1
    BACK = 2
    LEFT = 3
    TOP = 4
    BOTTOM = 5

def code_to_orientation(code):
    if code == 'g':
        return Orientation.FRONT
    elif code == 'r':
        return Orientation.RIGHT
    elif code == 'b':
        return Orientation.BACK
    elif code == 'o':
        return Orientation.LEFT
    elif code == 'y':
        return Orientation.TOP
    elif code == 'w':
        return Orientation.BOTTOM
    else:
        raise ValueError("Invalid color code")

def orientation_to_code(orientation):
    if orientation == Orientation.FRONT:
        return 'g'
    elif orientation == Orientation.RIGHT:
        return 'r'
    elif orientation == Orientation.BACK:
        return 'b'
    elif orientation == Orientation.LEFT:
        return 'o'
    elif orientation == Orientation.TOP:
        return 'y'
    elif orientation == Orientation.BOTTOM:
        return 'w'
    else:
        raise ValueError("Invalid orientation")