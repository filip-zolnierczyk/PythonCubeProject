from setuptools.command.rotate import rotate
from tools import *

class RubiksCube:
    # kostka przyjmuje tabele 6 tabel z czego każda reprezentuje ścianę kostki
    def __init__(self, tab=["gggggggggg", "rrrrrrrrrr", "bbbbbbbbbb", "oooooooooo", "yyyyyyyyyy", "wwwwwwwwww"]):
        self.facing_user = 'g'
        self.bottom_side = 'w'
        self.top_side = 'y'
        self.sides = {
            "g": "",
            "r": "",
            "b": "",
            "o": "",
            "y": "",
            "w": ""
        }

        codes = ['g','r','b','o','y','w']

        for i,t in enumerate(tab):
            self.sides[codes[i]] = t

    def rotate_side(self, side, clockwise=True):
        pass

    def perform_u_move(self, clockwise=True):
        pass

    def perform_d_move(self, clockwise=True):
        pass

    def perform_l_move(self, clockwise=True):
        self.rotate_side(previous_side(self.facing_user), clockwise)

    def perform_r_move(self, clockwise=True):
        self.rotate_side(next_side(self.facing_user), clockwise)

    def perform_f_move(self, clockwise=True):
        self.rotate_side(self.facing_user, clockwise)

    def perform_b_move(self, clockwise=True):
        self.rotate_side(opposite_side(self.facing_user), clockwise)
