import copy

from kociemba import solve
from solving_algorithms.Kociemba_Algorithm import key_convert
from solving_algorithms.LBL_Algorithm import *
from kociemba import solve

from solving_algorithms.Kociemba_Algorithm import key_convert
from solving_algorithms.LBL_Algorithm import *


def make_face(face):
    #face to string 9 elementowy
    #na początku tworzymy wybraną ścianke
    #dopełniamy elementy (nie powtarza sie 2 razy ten sam kolor na elemencie)
    #dopełniamy reszte kostki (sprawdzamy zgodnosc flipow twistów i permuatcji)
    def find(color, table):
        for i in range(len(table)):
            if color in table[i]:
                x = table[i]
                table.remove(table[i])
                x = list(x)
                if color == x[1]:
                    x.remove(color)
                    return x[::-1]
                x.remove(color)
                return x

    def set_side_value(cube, side, index, value):
        s = cube.sides[side]
        cube.sides[side] = s[:index] + value + s[index + 1:]

    def fill_face(cube, face):

        x = find(face[0], corners)
        set_side_value(cube, previous_side(cube.facing_user), 2, x[0])
        set_side_value(cube, cube.top_side, 6, x[1])

        x = find(face[2], corners)
        set_side_value(cube, next_side(cube.facing_user), 0, x[1])
        set_side_value(cube, cube.top_side, 8, x[0])

        x = find(face[6], corners)
        set_side_value(cube, previous_side(cube.facing_user), 8, x[1])
        set_side_value(cube, cube.bottom_side, 0, x[0])

        x = find(face[8], corners)
        set_side_value(cube, next_side(cube.facing_user), 6, x[0])
        set_side_value(cube, cube.bottom_side, 2, x[1])

        x = find(face[1], edges)
        set_side_value(cube, cube.top_side, 7, x[0])

        x = find(face[3], edges)
        set_side_value(cube, previous_side(cube.facing_user), 5, x[0])

        x = find(face[5], edges)
        set_side_value(cube, next_side(cube.facing_user), 3, x[0])

        x = find(face[7], edges)
        set_side_value(cube, cube.bottom_side, 1, x[0])

    def side_edges():
        cube.rotate_cube()

        a = edges[0][0]
        x = find(a, edges)
        set_side_value(cube, cube.top_side, 7, x[0])
        set_side_value(cube, cube.facing_user, 1, a)

        a = edges[0][0]
        x = find(a, edges)
        set_side_value(cube, cube.bottom_side, 1, x[0])
        set_side_value(cube, cube.facing_user, 7, a)

    def valid_cube(cubestring):
        try:
            return solve(cubestring)
        except ValueError as e:
            return False

    def change_notation(state):
        face_order = ['y', 'o', 'g', 'w', 'r', 'b']  # ORDER: up right front down left back
        input_string = ""
        for face in face_order:
            input_string += key_convert(state[face])
        return input_string

    def twist_corner(cube):
        a = cube.sides[cube.top_side][0]
        b = cube.sides[previous_side(cube.facing_user)][0]
        c = cube.sides[opposite_side(cube.facing_user)][2]
        set_side_value(cube, cube.top_side, 0, c)
        set_side_value(cube, previous_side(cube.facing_user), 0, a)
        set_side_value(cube, opposite_side(cube.facing_user), 2, b)

    def flip_edge(cube):
        a = cube.sides[cube.top_side][5]
        b = cube.sides[next_side(cube.facing_user)][1]
        set_side_value(cube, cube.top_side, 5, b)
        set_side_value(cube, next_side(cube.facing_user), 1, a)

    def change_edge_places(cube):
        a = cube.sides[cube.top_side][5]
        b = cube.sides[cube.top_side][3]
        set_side_value(cube, cube.top_side, 5, b)
        set_side_value(cube, cube.top_side, 3, a)

        a = cube.sides[previous_side(cube.facing_user)][1]
        b = cube.sides[next_side(cube.facing_user)][1]
        set_side_value(cube, previous_side(cube.facing_user), 1, b)
        set_side_value(cube, next_side(cube.facing_user), 1, a)

    def solved_cube(cube):
        for i in ['y', 'o', 'g', 'w', 'r', 'b']:
            string = 9*i
            if cube.sides[i] != string:
                return False
        return True

    def odwroc_algorytm(algorytm):
        ruchy = algorytm.split()[::-1]  # odwrócenie kolejności
        odwrotne_ruchy = []

        for ruch in ruchy:
            if ruch.endswith("2"):
                odwrotne_ruchy.append(ruch)  # ruchy x2 są takie same po odwróceniu
            elif ruch.endswith("'"):
                odwrotne_ruchy.append(ruch[:-1])  # R' → R
            else:
                odwrotne_ruchy.append(ruch + "'")  # R → R'

        return " ".join(odwrotne_ruchy)

    edges = [
        'yg',
        'yr',
        'yb',
        'yo',
        'gr',
        'go',
        'bo',
        'br',
        'wg',
        'wr',
        'wb',
        'wo'
    ]

    corners = [
        'ygr',
        'yog',
        'ybo',
        'yrb',
        'wrg',
        'wgo',
        'wob',
        'wbr'
    ]

    cube = RubiksCube()
    if face[4] != 'y' and face[4] != 'w':

        while face[4] != cube.facing_user:
            cube.rotate_cube()

        cube.sides[cube.facing_user] = face

        fill_face(cube, face)

        side_edges()

        cube.rotate_cube()

        random_face = corners[0][0] + edges[0][0] + corners[1][0] + edges[1][0] + cube.facing_user + edges[2][0] + \
                      corners[2][0] + edges[3][0] + corners[3][0]
        cube.sides[cube.facing_user] = random_face
        fill_face(cube, random_face)

        side_edges()
        cube.rotate_cube()

        cube.display_cube()

        white_cross(cube)
        insert_bottom_corners(cube)
        insert_edges(cube)
        yellow_cross(cube)
        allign_top_edges(cube)
        position_top_corners(cube)

        cube.display_cube()
        cube2 = copy.deepcopy(cube)

        def find_mistakes():
            for u in range(4):
                for p in range(4):
                    for e in range(2):
                        for c in range(3):
                            permutate_top_corners(cube)
                            last_move(cube)
                            if solved_cube(cube):
                                p_result = p
                                e_result = e
                                c_result = c
                                print(p_result, e_result, c_result)
                                return [p_result, e_result, c_result]
                            twist_corner(cube)
                        flip_edge(cube)
                    change_edge_places(cube)
                cube.perform_u_move()

        t = find_mistakes()
        print(t)
        p_result, e_result, c_result = t[0], t[1], t[2]

        for i in range(p_result):
            change_edge_places(cube2)
        for i in range(e_result):
            flip_edge(cube2)
        for i in range(c_result):
            twist_corner(cube2)

        cubestring = change_notation(cube2.sides)
        solution = solve(cubestring)
        print(solution)
        print(odwroc_algorytm(solution))
