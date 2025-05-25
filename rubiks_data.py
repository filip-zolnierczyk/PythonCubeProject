from util.rubiks_move_util import *
from random import shuffle

class RubiksCube:
    def __init__(self, sides_dict={"g":"ggggggggg", "r":"rrrrrrrrr", "b":"bbbbbbbbb", "o":"ooooooooo", "y":"yyyyyyyyy", "w":"wwwwwwwww"}):
        self.facing_user = 'g'
        self.bottom_side = 'w'
        self.top_side = 'y'
        self.sides = {"g": "", "r": "", "b": "", "o": "", "y": "", "w": ""}
        self.performed_moves = []

        codes = ['g', 'r', 'b', 'o', 'y', 'w']

        for i in range(len(sides_dict)):
            self.sides[codes[i]] = sides_dict[codes[i]]

        self.global_rotation_x = 0
        self.global_rotation_y = 0
        self.global_rotation_z = 0

    def set_colours(self, colours: dict):
        self.sides = colours
        self.performed_moves = []

    def clear_performed_moves(self):
        self.performed_moves = []
    def get_performed_moves(self):
        return self.performed_moves

    def scramble_cube(self):
        scramble_moves = [ "F", "R", 'B', 'L', 'U', 'D' ]

        for i in range(2):
            shuffle(scramble_moves)
            for m in scramble_moves:
                self.perform_move(m)

    def rotate_cube_global(self, base_move: string, clockwise: bool):
        clockwise_mult = 1 if clockwise else -1
        match base_move:
            case 'X': self.global_rotation_x = (self.global_rotation_x + clockwise_mult) % 3
            case 'Y': self.global_rotation_y += (self.global_rotation_y + clockwise_mult) % 3
            case 'Z': self.global_rotation_z += (self.global_rotation_z + clockwise_mult) % 3


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

    def perform_move(self, move):
        move_str = move.upper()
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
            base_move = shift_move_xyz(base_move, self.global_rotation_x, self.global_rotation_y, self.global_rotation_z)
            for _ in range(repeat):
                move_function_map[base_move](clockwise)
        elif base_move in ['X','Y','Z']:
            self.rotate_cube_global(base_move,clockwise)
        else:
            raise ValueError(f"Nieznany ruch: {move_str}")

    def rotate_cube_no_append(self, clockwise=True):
        if clockwise:
            self.facing_user = next_side(self.facing_user)
            self.rotate_face(self.top_side, clockwise)
            self.rotate_face(self.bottom_side, not clockwise)

        if not clockwise:
            for i in range(3): self.rotate_cube_no_append(True)

    def rotate_cube(self, clockwise=True):
        if clockwise:
            self.performed_moves.append("x")
        else:
            self.performed_moves.append("x'")
        self.rotate_cube_no_append(clockwise)

    #w przypadku kazdego ruchu trzeba zmienic indexację na kazdej sciance (bo sie obraca) i obrocic pozostale naklejki z 4 scian
    def perform_f_move_no_append(self, clockwise=True):

        temp1 = self.sides[self.top_side][-3:]
        temp2 = self.sides[next_side(self.facing_user)][0] + self.sides[next_side(self.facing_user)][3] + \
                self.sides[next_side(self.facing_user)][6]
        temp3 = self.sides[self.bottom_side][:3]
        temp4 = self.sides[previous_side(self.facing_user)][8] + self.sides[previous_side(self.facing_user)][5] + \
                self.sides[previous_side(self.facing_user)][2]

        self.rotate_face(self.facing_user, clockwise)

        if clockwise:  # działa
            self.sides[self.top_side] = self.sides[self.top_side][:6] + temp4

            self.sides[next_side(self.facing_user)] = temp1[0] + self.sides[next_side(self.facing_user)][1:3] + temp1[
                1] + self.sides[next_side(self.facing_user)][4:6] + temp1[2] + self.sides[next_side(self.facing_user)][
                                                                               7:9]

            self.sides[self.bottom_side] = temp2[::-1] + self.sides[self.bottom_side][3:]

            self.sides[previous_side(self.facing_user)] = self.sides[previous_side(self.facing_user)][0:2] + temp3[0] + \
                                                          self.sides[previous_side(self.facing_user)][3:5] + temp3[1] + \
                                                          self.sides[previous_side(self.facing_user)][6:8] + temp3[2]

        else:
            self.sides[self.top_side] = self.sides[self.top_side][:6] + temp2

            self.sides[next_side(self.facing_user)] = temp3[2] + self.sides[next_side(self.facing_user)][1:3] + temp3[
                1] + self.sides[next_side(self.facing_user)][4:6] + temp3[0] + self.sides[next_side(self.facing_user)][
                                                                               7:9]

            self.sides[self.bottom_side] = temp4[::-1] + self.sides[self.bottom_side][3:]

            self.sides[previous_side(self.facing_user)] = self.sides[previous_side(self.facing_user)][0:2] + temp1[2] + \
                                                          self.sides[previous_side(self.facing_user)][3:5] + temp1[1] + \
                                                          self.sides[previous_side(self.facing_user)][6:8] + temp1[0]

    def perform_f_move(self, clockwise=True):
        if clockwise:
            self.performed_moves.append("F")
        else:
            self.performed_moves.append("F'")
        self.perform_f_move_no_append(clockwise)

    def perform_r_move(self, clockwise=True):
        if clockwise:
            self.performed_moves.append("R")
        else:
            self.performed_moves.append("R'")
        self.rotate_cube_no_append(True)
        self.perform_f_move_no_append(clockwise)
        self.rotate_cube_no_append(False)

    def perform_l_move(self, clockwise=True):
        if clockwise:
            self.performed_moves.append("L")
        else:
            self.performed_moves.append("L'")
        self.rotate_cube_no_append(False)
        self.perform_f_move_no_append(clockwise)
        self.rotate_cube_no_append(True)

    def perform_b_move(self, clockwise=True):
        if clockwise:
            self.performed_moves.append("B")
        else:
            self.performed_moves.append("B'")

        for i in range(2):
            self.rotate_cube_no_append(True)

        self.perform_f_move_no_append(clockwise)

        for i in range(2):
            self.rotate_cube_no_append(True)

    def perform_u_move(self, clockwise=True):

        self.rotate_face(self.top_side, clockwise)
        face = self.sides[self.facing_user][:3]
        right = self.sides[next_side(self.facing_user)][:3]
        back = self.sides[next_side(next_side(self.facing_user))][:3]
        left = self.sides[previous_side(self.facing_user)][:3]

        if clockwise:
            self.performed_moves.append("U")
            self.sides[self.facing_user] = right + self.sides[self.facing_user][3:]
            self.sides[next_side(self.facing_user)] = back + self.sides[next_side(self.facing_user)][3:]
            self.sides[next_side(next_side(self.facing_user))] = left + self.sides[
                                                                            next_side(next_side(self.facing_user))][3:]
            self.sides[previous_side(self.facing_user)] = face + self.sides[previous_side(self.facing_user)][3:]

        else:
            self.performed_moves.append("U'")
            self.sides[self.facing_user] = left + self.sides[self.facing_user][3:]
            self.sides[next_side(self.facing_user)] = face + self.sides[next_side(self.facing_user)][3:]
            self.sides[next_side(next_side(self.facing_user))] = right + self.sides[
                                                                            next_side(next_side(self.facing_user))][3:]
            self.sides[previous_side(self.facing_user)] = back + self.sides[previous_side(self.facing_user)][3:]

    def perform_d_move(self, clockwise=True):

        self.rotate_face(self.bottom_side, clockwise)
        face = self.sides[self.facing_user][-3:]
        right = self.sides[next_side(self.facing_user)][-3:]
        back = self.sides[next_side(next_side(self.facing_user))][-3:]
        left = self.sides[previous_side(self.facing_user)][-3:]

        if clockwise:
            self.performed_moves.append("D")
            self.sides[self.facing_user] = self.sides[self.facing_user][:6] + left
            self.sides[next_side(self.facing_user)] = self.sides[next_side(self.facing_user)][:6] + face
            self.sides[next_side(next_side(self.facing_user))] = self.sides[next_side(next_side(self.facing_user))][:6] + right
            self.sides[previous_side(self.facing_user)] = self.sides[previous_side(self.facing_user)][:6] + back
        else:
            self.performed_moves.append("D'")
            self.sides[self.facing_user] = self.sides[self.facing_user][:6] + right
            self.sides[next_side(self.facing_user)] = self.sides[next_side(self.facing_user)][:6] + back
            self.sides[next_side(next_side(self.facing_user))] = self.sides[next_side(next_side(self.facing_user))][:6] + left
            self.sides[previous_side(self.facing_user)] = self.sides[previous_side(self.facing_user)][:6] + face


    #do debugowania
    def display_cube(self):
        color_emojis = {
            'R': '🔴', 'r': '🔴',
            'G': '🟢', 'g': '🟢',
            'B': '🔵', 'b': '🔵',
            'O': '🟠', 'o': '🟠',
            'Y': '🟡', 'y': '🟡',
            'W': '⚪', 'w': '⚪',
        }

        def face_rows(face):
            return [face[i:i + 3] for i in range(0, 9, 3)]

        U = face_rows(self.sides['y'])
        D = face_rows(self.sides['w'])
        F = face_rows(self.sides[self.facing_user])
        R = face_rows(self.sides[next_side(self.facing_user)])
        B = face_rows(self.sides[next_side(next_side(self.facing_user))])
        L = face_rows(self.sides[previous_side(self.facing_user)])

        print("Up:")
        for row in U:
            print(' '.join(color_emojis[c] for c in row))
        print()

        print("Left | Front | Right | Back:")
        for l, f, r, b in zip(L, F, R, B):
            l_row = ' '.join(color_emojis[c] for c in l)
            f_row = ' '.join(color_emojis[c] for c in f)
            r_row = ' '.join(color_emojis[c] for c in r)
            b_row = ' '.join(color_emojis[c] for c in b)
            print(f"{l_row}   {f_row}   {r_row}   {b_row}")
        print()

        print("Down:")
        for row in D:
            print(' '.join(color_emojis[c] for c in row))

    def perform_f2_move(self):
        for i in range(2):
            self.perform_f_move()

    def perform_r2_move(self):
        for i in range(2):
            self.perform_r_move()

    def perform_l2_move(self):
        for i in range(2):
            self.perform_l_move()

    def perform_b2_move(self):
        for i in range(2):
            self.perform_b_move()

    def perform_u2_move(self):
        for i in range(2):
            self.perform_u_move()

    def perform_d2_move(self):
        for i in range(2):
            self.perform_d_move()
