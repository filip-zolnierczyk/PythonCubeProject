import math
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import cube
from vector_util import *
from pygame.math import Vector3 as V3
from orientation_util import *

# Mapa kolorów dla ścianek kostki Rubika
COLOR_MAP = {
    'w': (1, 1, 1),  # Biały
    'r': (1, 0, 0),  # Czerwony
    'b': (0, 0, 1),  # Niebieski
    'o': (1, 0.5, 0),  # Pomarańczowy
    'g': (0, 1, 0),  # Zielony
    'y': (1, 1, 0),   # Żółty
    'x': (0, 0, 0)   # Czarny (kolor domyślny)
}

# Wierzchołki kostki (znormalizowane -> dlugosc boku = 1)
vertices = [
    (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5),
    (-0.5, -0.5,  0.5), (0.5, -0.5,  0.5), (0.5, 0.5,  0.5), (-0.5, 0.5,  0.5)
]

# Ściany kostki
faces = {
    'g': (4, 5, 6, 7),  # Przód
    'r': (1, 2, 6, 5),   # Prawo
    'b': (0, 1, 2, 3),  # Tył
    'o': (0, 3, 7, 4),  # Lewo
    'y': (2, 3, 7, 6),  # Góra
    'w': (0, 1, 5, 4)  # Dół
}

# class for rubiks mini-cubes
class RubiksMiniCubeDisplay:
    def __init__(self, origin=V3_ZERO, size=1):
        self.origin = origin
        self.size = size
        self.colours = ['x' for _ in range(6)]

    def colour_single_side(self, facing, colour):
        self.colours[facing.value] = colour

# class for displaying any rubiks cube
class RubiksCubeDisplay:
    def __init__(self, square_num, pos=V3_ZERO, size = 1, colours_dict=None):
        # init data
        self.pos = pos
        self.square_num = square_num
        self.square_num_sq = square_num*square_num
        self.origin = pos - V3_ONE * size * 0.5 # origin of the cube (corner)
        self.sides = [[] for _ in range(6)] # empty list for each side
        self.mini_cubes = [] # list of all mini-cubes

        # initialize mini-cubes in sides[] array
        mini_cube_size = size / square_num
        for x in range(square_num):
            for y in range(square_num):
                for z in range(square_num):
                    # skip if middle of rubiks cube
                    if x != 0 and x != square_num-1 and y != 0 and y != square_num-1 and z != 0 and z != square_num-1:
                        continue

                    # create a mini-cube at position:
                    mini_cube_origin = V3(
                        self.origin.x + x * mini_cube_size,
                        self.origin.y + y * mini_cube_size,
                        self.origin.z + z * mini_cube_size
                    )
                    mini_cube = RubiksMiniCubeDisplay(mini_cube_origin, mini_cube_size)
                    
                    # add mini-cube to the appropriate side, and list of all mini-cubes
                    self.mini_cubes.append(mini_cube)
                    if x == 0: self.sides[Orientation.LEFT.value].append(mini_cube)
                    if x == square_num-1: self.sides[Orientation.RIGHT.value].append(mini_cube)
                    if y == 0: self.sides[Orientation.BOTTOM.value].append(mini_cube)
                    if y == square_num-1: self.sides[Orientation.TOP.value].append(mini_cube)
                    if z == 0: self.sides[Orientation.BACK.value].append(mini_cube)
                    if z == square_num-1: self.sides[Orientation.FRONT.value].append(mini_cube)

        # set colours if given
        if colours_dict is not None:
            self.set_all_colours(colours_dict)

    # set all sides of the cube to the given colours
    def set_all_colours(self, colours_dict):
        for o in Orientation:
            self.set_side_colours(o, colours_dict[orientation_to_code(o)])

    # set the colours of a single side of the cube
    def set_side_colours(self, facing, colours):
        for i,mini in enumerate(self.sides[facing.value]):
            mini.colour_single_side(facing, colours[i])

    # render
    def draw(self):
        for mc in self.mini_cubes:
            draw_cube(mc.origin, 0.85*mc.size, mc.colours) # draw mini-cube at its origin

def draw_cube(origin=V3_ZERO,size=1,colours=['x'for _ in range(6)]):
    glBegin(GL_QUADS)
    for key,f in faces.items():
        glColor3fv( COLOR_MAP[colours[code_to_orientation(key).value]] ) # black
        for v in f:
            vert_pos = vertices[v]
            glVertex3fv(add_vectors(tuple(origin),mul_vector(vert_pos,size)))
    glEnd()
