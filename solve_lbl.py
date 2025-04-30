from rubiks_data import RubiksCube
from lbl_algorythms import *


def solve_lbl(cube=RubiksCube()):
    white_cross(cube)
    insert_bottom_corners(cube)
    insert_edges(cube)
    yellow_cross(cube)
    allign_top_edges(cube)
    position_top_corners(cube)
    permutate_top_corners(cube)
    last_move(cube)
    return
