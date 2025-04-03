from setuptools.command.rotate import rotate

import tools
from PythonCubeProject.tools import next_side, previous_side, opposite_side


class RubiksCube:
    def __init__(self, tab=["ggggggggg", "rrrrrrrrr", "bbbbbbbbb", "ooooooooo", "yyyyyyyyy", "wwwwwwwww"]):
        self.facing_user = 'g'
        self.bottom_side = 'w'
        self.top_side = 'y'
        self.sides = {"g": "", "r": "", "b": "", "o": "", "y": "", "w": ""}

        for t in tab:
            s = tools.convert_table_to_side(t)
            c = s[4]
            self.sides[c] = s

    def rotate_side(self, side, clockwise=True):
        face = list(self.sides[side])
        if clockwise:
            rotated_face = [
                face[6], face[3], face[0],
                face[7], face[4], face[1],
                face[8], face[5], face[2]
            ]
        else:
            rotated_face = [
                face[2], face[5], face[8],
                face[1], face[4], face[7],
                face[0], face[3], face[6]
            ]
        self.sides[side] = "".join(rotated_face)

        # Aktualizacja sąsiednich ścian


    def perform_f_move(self, clockwise=True):
        self.rotate_side(self.facing_user, clockwise)

    def perform_r_move(self, clockwise=True):
        self.rotate_side(next_side(self.facing_user), clockwise)

    def perform_l_move(self, clockwise=True):
        self.rotate_side(previous_side(self.facing_user), clockwise)

    def perform_b_move(self, clockwise=True):
        self.rotate_side(opposite_side(self.facing_user), clockwise)

    def perform_u_move(self, clockwise=True):
        pass

    def perform_d_move(self, clockwise=True):
        pass

    def display_cube(self):
        for key, value in self.sides.items():
            print(f"{key.upper()} side:")
            for i in range(0, 9, 3):
                print(value[i:i + 3])
            print()
