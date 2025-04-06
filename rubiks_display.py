import math
import pygame
from pygame.locals import *
from util.vector_util import *
from pygame.math import Vector3 as V3
from util.orientation_util import *
from util.rubiks_move_util import *
from util.colour_util import *
from util.cube_render_util import *

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
        self.animating = False # animation flag

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
    
    def update_animation(self, dt):
        pass
        # if self.animating:
        #     self.animation_time += dt
        #     if self.animation_time >= self.animation_duration:
        #         self.animating = False
        #         self.animation_time = 0.0
        #         return

        #     # Interpolacja między pozycjami początkową i końcową
        #     t = self.animation_time / self.animation_duration
        #     for mini_cube in self.mini_cubes:
        #         mini_cube.origin = add_vectors(self.start_position, mul_vector(sub_vectors(self.end_position, self.start_position), t))

    def is_animating(self):
        return self.animating
    
    def animate_move(self, move: RubiksMove, duration: float):
        self.animating = True
