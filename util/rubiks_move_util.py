from enum import Enum
from os import remove

from numpy.f2py.auxfuncs import throw_error
import string

from sympy import elliptic_f


class RubiksMove(Enum):
    # Główne ruchy 90° zgodnie z ruchem wskazówek zegara
    U = "U"  # Up
    D = "D"  # Down
    L = "L"  # Left
    R = "R"  # Right
    F = "F"  # Front
    B = "B"  # Back

    # Ruchy przeciwnie do ruchu wskazówek zegara (prime)
    U_PRIME = "U'"  # Up inverse
    D_PRIME = "D'"  # Down inverse
    L_PRIME = "L'"  # Left inverse
    R_PRIME = "R'"  # Right inverse
    F_PRIME = "F'"  # Front inverse
    B_PRIME = "B'"  # Back inverse

    # Ruchy o 180 stopni
    U2 = "U2"  # Up 180°
    D2 = "D2"  # Down 180°
    L2 = "L2"  # Left 180°
    R2 = "R2"  # Right 180°
    F2 = "F2"  # Front 180°
    B2 = "B2"  # Back 180°

    # Obrót całej kostki (rotacje globalne)
    X = "X"  # Rotacja wokół osi X (jak R)
    X_PRIME = "X'"
    X2 = "X2"

    Y = "Y"  # Rotacja wokół osi Y (jak U)
    Y_PRIME = "Y'"
    Y2 = "Y2"

    Z = "Z"  # Rotacja wokół osi Z (jak F)
    Z_PRIME = "Z'"
    Z2 = "Z2"

def opposite_side(x):
    if x == "b":
        return "g"
    if x == "y":
        return "w"
    if x == "r":
        return "o"
    if x == "g":
        return "b"
    if x == "w":
        return "y"
    if x == "o":
        return "r"
    else:
        throw_error("Color does not exist")


def next_side(x):
    if x == "b":
        return "r"
    if x == "r":
        return "g"
    if x == "g":
        return "o"
    if x == "o":
        return "b"
    else:
        throw_error("Color does not exist")


def previous_side(x):
    if x == "b":
        return "o"
    if x == "o":
        return "g"
    if x == "g":
        return "r"
    if x == "r":
        return "b"
    else:
        raise ValueError("Color does not exist")


""" 
    green - front
    red - right
    blue - back
    orange - left
    yellow - top
    white - bottom
"""


def convert_move_to_face(move: string):
    if move.value.find("F") != -1: return 'g'
    if move.value.find("R") != -1: return 'o'
    if move.value.find("B") != -1: return 'b'
    if move.value.find("L") != -1: return 'r'
    if move.value.find("U") != -1: return 'y'
    if move.value.find("D") != -1: return 'w'
    return 'x'

def shift_move_xyz(base_move, offset_x, offset_y, offset_z):
    # kolejnosci zmiany scianek w tabelach
    moves_order_x = ["L","F","R","B"]
    moves_order_y = ["L","U","R","D"]
    moves_order_z = ["D","F","U","B"]

    offset_x = -offset_x; offset_y = -offset_y; offset_z = -offset_z

    # obroty ruchow po kolei x y z uzywajac podane offsety
    if base_move != "U" and base_move != "D":
        global_move_idx = moves_order_x.index(base_move)
        if offset_x < 0: offset_x = (len(moves_order_x)-1)*abs(offset_x) # jeden ruch w lewo to to samo co n-1 ruchow w prawo
        base_move = moves_order_x[ (global_move_idx+offset_x)%len(moves_order_x) ]

    if base_move != "F" and base_move != "B":
        global_move_idx = moves_order_y.index(base_move)
        if offset_y < 0: offset_y = (len(moves_order_y)-1)*abs(offset_y) # jeden ruch w lewo to to samo co n-1 ruchow w prawo
        base_move = moves_order_y[ (global_move_idx+offset_y)%len(moves_order_y) ]

    if base_move != "L" and base_move != "R":
        global_move_idx = moves_order_z.index(base_move)
        if offset_z < 0: offset_z = (len(moves_order_z)-1)*abs(offset_z) # jeden ruch w lewo to to samo co n-1 ruchow w prawo
        base_move = moves_order_z[ (global_move_idx+offset_z)%len(moves_order_z) ]

    return base_move

def code_to_move(code: string):
    match code:
        case "F": return RubiksMove.F
        case "R": return RubiksMove.R
        case "B": return RubiksMove.B
        case "L": return RubiksMove.L
        case "U": return RubiksMove.U
        case "D": return RubiksMove.D
        case "F'": return RubiksMove.F_PRIME
        case "R'": return RubiksMove.R_PRIME
        case "B'": return RubiksMove.B_PRIME
        case "L'": return RubiksMove.L_PRIME
        case "U'": return RubiksMove.U_PRIME
        case "D'": return RubiksMove.D_PRIME
        case "X": return RubiksMove.X
        case "Y": return RubiksMove.Y
        case "Z": return RubiksMove.Z
        case "X'": return RubiksMove.X_PRIME
        case "Y'": return RubiksMove.Y_PRIME
        case "Z'": return RubiksMove.Z_PRIME

def convert_table_to_side(t):
    string = t[0] + t[3] + t[6] + t[1] + t[4] + t[7] + t[2] + t[5] + t[8]
    return string

def optimize_move_table(t):
    for i in range(2):
        #usuwanie ruchów które od razu zostały cofnięte
        for i in range(len(t) - 2):
            if t[i][0] == t[i + 1][0] and len(t[i]) + len(t[i + 1]) == 3:
                t[i] = "#"
                t[i + 1] = "#"

        t[:] = [move for move in t if move != "#"]
        #usuwanie ruchów które zostały powtórzone 4 razy lub zamiana 3 na 1 w przypadku 3 powtórzeń
        for i in range(len(t) - 4):
            if t[i] == t[i + 1] == t[i + 2]:
                if t[i] == t[i + 3]:
                    for j in range(4):
                        t[i + j] = "#"
                else:
                    if len(t[i]) == 2:
                        t[i] = t[i][0]
                        t[i + 1] = "#"
                        t[i + 2] = "#"
                    else:
                        t[i] = t[i] + "'"
                        t[i + 1] = "#"
                        t[i + 2] = "#"
        t[:] = [move for move in t if move != "#"]
        t[:] = [move for move in t if move != "#'"]

    #zamiana podwójnych ruchów na notacje z 2
    for i in range(len(t) - 2):
        if t[i] == t[i + 1]:
            t[i] = t[i][0] + "2"
            t[i + 1] = "#"

    t[:] = [move for move in t if move != "#"]
    return
