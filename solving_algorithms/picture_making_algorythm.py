from rubiks_data import RubiksCube
import random
from solving_algorithms.Kociemba_Algorithm import solve_kociemba
from util.colour_util import colour_num_to_code

random.seed(42)


def create_current_string(cube, end_face_center):
    current_string = (cube.sides[end_face_center][1] + cube.sides[end_face_center][3] + cube.sides[end_face_center][5] +
                      cube.sides[end_face_center][7])
    return current_string


def permutate_corner_front(cube):
    cube.perform_l_move(False)
    cube.perform_b_move()
    cube.perform_l_move()
    cube.perform_b_move(False)


def permutate_corner_bottom(cube):
    cube.perform_l_move(False)
    cube.perform_u_move(False)
    cube.perform_l_move()
    cube.perform_u_move()


def permutate_corner_top(cube):
    cube.perform_l_move(False)
    cube.perform_d_move(False)
    cube.perform_l_move()
    cube.perform_d_move()


def choose_corner_front(cube, f):
    while True:
        for i in range(6):
            if cube.sides[cube.facing_user][0] == f:
                return
            permutate_corner_front(cube)
        cube.perform_b_move()


def choose_corner_bottom(cube, f):
    while True:
        for i in range(6):
            if cube.sides["w"][0] == f:
                return
            permutate_corner_bottom(cube)
        cube.perform_u_move()


def choose_corner_top(cube, f):
    while True:
        for i in range(6):
            if cube.sides["y"][0] == f:
                return
            permutate_corner_top(cube)
        cube.perform_d_move()


def make_face(face):
    cube = RubiksCube()
    end_face_center = face[4]
    required_strings = [face[1] + face[3] + face[5] + face[7], face[3] + face[7] + face[1] + face[5],
                        face[7] + face[5] + face[3] + face[1], face[5] + face[1] + face[7] + face[3]]

    while True:

        x = random.randint(0, 6)

        if x == 0:
            cube.perform_u_move()
        elif x == 1:
            cube.perform_d_move()
        elif x == 2:
            cube.perform_f_move()
        elif x == 3:
            cube.perform_b_move()
        elif x == 5:
            cube.perform_r_move()
        elif x == 6:
            cube.perform_l_move()

        current_string = create_current_string(cube, end_face_center)

        if current_string in required_strings:
            break

    if end_face_center in ("r", "o", "g", "b"):

        while cube.facing_user != end_face_center:
            cube.rotate_cube()

        while current_string != required_strings[0]:
            cube.perform_f_move()
            current_string = create_current_string(cube, end_face_center)

        for i in (0, 6, 8, 2):
            choose_corner_front(cube, face[i])
            cube.perform_f_move()

    elif end_face_center == "w":

        while current_string != required_strings[0]:
            cube.perform_d_move()
            current_string = create_current_string(cube, end_face_center)

        for i in (0, 6, 8, 2):
            choose_corner_bottom(cube, face[i])
            cube.perform_d_move()

    elif end_face_center == "y":

        while current_string != required_strings[0]:
            cube.perform_u_move()
            current_string = create_current_string(cube, end_face_center)

        for i in (0, 6, 8, 2):
            choose_corner_top(cube, face[i])
            cube.perform_u_move()

    while cube.facing_user != 'g':
        cube.rotate_cube()

    return cube

def convert_to_face_string(face_list: list):
    face_str = ""
    for x in face_list:
        face_str += colour_num_to_code[x]
    return face_str

def solve_picture(face: str):
    cube = make_face(face)
    moves = solve_kociemba(cube.sides)
    moves = moves[::-1]
    for i in range(len(moves)):
        if len(moves[i]) == 1:
            moves[i] = moves[i] + "'"
        elif moves[i][1] != '2':
            moves[i] = moves[i][0]
    return moves
