from setuptools.command.rotate import rotate
from util.rubiks_move_util import *

class RubiksCube:
    def __init__(self, tab=["ggggggggg", "rrrrrrrrr", "bbbbbbbbb", "ooooooooo", "yyyyyyyyy", "wwwwwwwww"]):
        self.facing_user = 'g'
        self.bottom_side = 'w'
        self.top_side = 'y'
        self.sides = {"g": "", "r": "", "b": "", "o": "", "y": "", "w": ""}

        codes = ['g','r','b','o','y','w']

        for i,t in enumerate(tab):
            self.sides[codes[i]] = t

    def rotate_face(self, side, clockwise=True):
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

    def perform_move(self, move: RubiksMove):
        # Mapowanie enum -> funkcja + kierunek
        move_str = move.value
        base_move = move_str[0]
        clockwise = True
        repeat = 1

        if move_str.endswith("'"):  # np. "R'"
            clockwise = False
        elif move_str.endswith("2"):  # np. "R2"
            repeat = 2

        # wybieramy odpowiednią funkcję na podstawie litery
        move_function_map = {
            'F': self.perform_f_move,
            'R': self.perform_r_move,
            'L': self.perform_l_move,
            'B': self.perform_b_move,
            'U': self.perform_u_move,
            'D': self.perform_d_move,
        }

        if base_move in move_function_map:
            for _ in range(repeat):
                move_function_map[base_move](clockwise)
        else:
            raise ValueError(f"Nieznany ruch: {move_str}")

    #w przypadku kazdego ruchu trzeba zmienic indexację na kazdej sciance (bo sie obraca) i obrocic pozostale naklejki z 4 scian
    def perform_f_move(self, clockwise=True):

        self.rotate_face(self.facing_user, clockwise)

        temp1 = self.sides[self.top_side][-3:]
        temp2 = self.sides[next_side(self.facing_user)][0] + self.sides[next_side(self.facing_user)][3] + self.sides[next_side(self.facing_user)][6]
        temp3 = self.sides[self.bottom_side][:3]
        temp4 = self.sides[previous_side(self.facing_user)][2] + self.sides[previous_side(self.facing_user)][5] + self.sides[previous_side(self.facing_user)][8]

        if clockwise: #chyba działa

            self.sides[self.top_side] = self.sides[self.top_side][:6] + temp4

            print(self.sides[next_side(self.facing_user)])
            self.sides[next_side(self.facing_user)] = temp1[0] + self.sides[next_side(self.facing_user)][1:3] + temp1[1] + self.sides[next_side(self.facing_user)][4:6] + temp1[2] + self.sides[next_side(self.facing_user)][7:9]

            self.sides[self.bottom_side] = temp2[::-1] + self.sides[self.bottom_side][3:]

            self.sides[previous_side(self.facing_user)] = self.sides[previous_side(self.facing_user)][0:2] + temp3[0] + self.sides[previous_side(self.facing_user)][3:5] + temp3[1] + self.sides[previous_side(self.facing_user)][6:8] + temp3[2]

        else: 
            for i in range(3):
                self.perform_f_move(self)


    def perform_r_move(self, clockwise=True):
        self.rotate_face(next_side(self.facing_user), clockwise)

    def perform_l_move(self, clockwise=True):
        self.rotate_face(previous_side(self.facing_user), clockwise)

    def perform_b_move(self, clockwise=True):
        self.rotate_face(opposite_side(self.facing_user), clockwise)

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
