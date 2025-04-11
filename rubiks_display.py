import math
import pygame
from pygame.locals import *
from util.vector_util import *
from pygame.math import Vector3 as V3
from util.orientation_util import *
from util.rubiks_move_util import *
from util.colour_util import *
from util.cube_render_util import *
from util.animation_util import *

# class for rubiks mini-cubes
class RubiksMiniCubeDisplay:
    def __init__(self, origin: V3 = V3_ZERO, size: float = 1):
        self.origin = origin
        self.size = size
        self.colours = ['x' for _ in range(6)]
        self.local_rotation = 0
        self.rotation_vector = None

    def colour_single_side(self, facing, colour):
        self.colours[facing.value] = colour

    def set_rotation_vector(self,v):
        self.rotation_vector = v

# class for displaying any rubiks cube
class RubiksCubeDisplay:
    def __init__(self, square_num: int, pos: V3 = V3_ZERO, size: float = 1, colours_dict: dict = None):
        # init data
        self.pos = pos
        self.square_num = square_num
        self.square_num_sq = square_num*square_num
        self.origin = pos - V3_ONE * size * 0.5 # origin of the cube (corner)
        self.sides = [[] for _ in range(6)] # empty list for each side
        self.mini_cubes = [] # list of all mini-cubes
        self.position_animation_objects = [] # list of animation objects for this mini-cube
        self.rotation_animation_objects = [] # list of animation objects for this mini-cube

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

        # uporzadkuj mini-kostki do poprawnej orientacji (1: xyz 2: xyz 3: xyz) po kolei rzedy od gory do dolu
        """ 
            green - front
            red - right
            blue - back
            orange - left
            yellow - top
            white - bottom
        """
        self.sides = [
            [self.sides[0][i + j*square_num] for i in reversed(range(square_num)) for j in range(square_num)], # kolumny --> rzedy
            self.sides[1][::-1], # obrot 180 stopni
            [self.sides[2][i + j*square_num] for i in reversed(range(square_num)) for j in reversed(range(square_num))], # kolumny --> rzedy
            [self.sides[3][(square_num - 1 - j) + i*square_num] for i in reversed(range(square_num)) for j in reversed(range(square_num))],
            [self.sides[4][i + j*square_num] for i in range(square_num) for j in range(square_num)], # kolumny --> rzedy
            [self.sides[5][i + j*square_num] for i in reversed(range(square_num)) for j in range(square_num)], # kolumny --> rzedy
        ]

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
            draw_cube(mc.origin, 0.85*mc.size, mc.colours, mc.local_rotation, mc.rotation_vector) # draw mini-cube at its origin
    
    def update_animation(self, dt):
        # Animate positions
        for i,anim_obj in enumerate(self.position_animation_objects):
            mini, anim = anim_obj
            if not anim.is_animating(dt):
                mini.origin = anim.get_reset_value()
                self.position_animation_objects.pop(i)
            else:
                mini.origin = anim.get_animation_value()

        # Animate Rotations
        for i,anim_obj in enumerate(self.rotation_animation_objects):
            mini, anim = anim_obj
            if not anim.is_animating(dt):
                mini.local_rotation = anim.get_reset_value()
                self.rotation_animation_objects.pop(i)
            else:
                mini.local_rotation = anim.get_animation_value()

    def is_animating(self):
        return len(self.position_animation_objects) > 0 or len(self.rotation_animation_objects) > 0
    
    def animate_move(self, move: RubiksMove, duration: float):
        v1,v2,v3 = face_local_vectors[move.value]
        orientation_code = convert_move_to_face(move)
        orientation = code_to_orientation(orientation_code)
        clockwise = move.value.find("'") != -1
        rotation = 90 if clockwise else -90
        dp = calc_rotation_matrix_for_rubiks_side(v1, v2, self.square_num, self.mini_cubes[orientation.value].size, rotation)

        for i,mini in enumerate(self.sides[orientation.value]):
            self.position_animation_objects.append( (mini,Animation(duration, mini.origin, mini.origin + dp[i//self.square_num][i%self.square_num], reset_value=mini.origin)) )
            self.rotation_animation_objects.append( (mini,Animation(duration, 0, -rotation, reset_value=0)) )
            mini.rotation_vector = v3