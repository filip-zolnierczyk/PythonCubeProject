from pygame.math import Vector3 as V3

def mul_vector(v,s):
    return tuple(x*s for x in v)

def add_to_vector(v,s):
    return tuple(x+s for x in v)

def add_vectors(v1,v2):
    return tuple(x + y for x, y in zip(v1, v2))

def sub_vectors(v1,v2):
    return tuple(x - y for x, y in zip(v1, v2))

V3_ONE = V3(1, 1, 1)
V3_ZERO = V3(0, 0, 0)
V3_Y = V3(0, 1, 0)
V3_X = V3(1, 0, 0)
V3_Z = V3(0, 0, 1)