from enum import Enum
from numpy.f2py.auxfuncs import throw_error
import string

class RubiksMove(Enum):
    # Główne ruchy 90° zgodnie z ruchem wskazówek zegara
    U = "U"   # Up
    D = "D"   # Down
    L = "L"   # Left
    R = "R"   # Right
    F = "F"   # Front
    B = "B"   # Back

    # Ruchy przeciwnie do ruchu wskazówek zegara (prime)
    U_PRIME = "U'"   # Up inverse
    D_PRIME = "D'"   # Down inverse
    L_PRIME = "L'"   # Left inverse
    R_PRIME = "R'"   # Right inverse
    F_PRIME = "F'"   # Front inverse
    B_PRIME = "B'"   # Back inverse

    # Ruchy o 180 stopni
    U2 = "U2"   # Up 180°
    D2 = "D2"   # Down 180°
    L2 = "L2"   # Left 180°
    R2 = "R2"   # Right 180°
    F2 = "F2"   # Front 180°
    B2 = "B2"   # Back 180°

    # Obrót całej kostki (rotacje globalne)
    X = "X"     # Rotacja wokół osi X (jak R)
    X_PRIME = "X'"
    X2 = "X2"

    Y = "Y"     # Rotacja wokół osi Y (jak U)
    Y_PRIME = "Y'"
    Y2 = "Y2"

    Z = "Z"     # Rotacja wokół osi Z (jak F)
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
    if move.value.find("R") != -1: return 'r'
    if move.value.find("B") != -1: return 'b'
    if move.value.find("L") != -1: return 'o'
    if move.value.find("U") != -1: return 'y'
    if move.value.find("D") != -1: return 'w'
    return 'x'

def convert_table_to_side(t):
    string = t[0] + t[3] + t[6] + t[1] + t[4] + t[7] + t[2] + t[5] + t[8]
    return string
