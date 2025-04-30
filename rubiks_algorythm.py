from util.rubiks_move_util import *
from random import randint
from random import shuffle
from lbl_algorythms import *
from rubiks_data import RubiksCube

class RubiksAlgorythm:
    def __init__(self, algorythm: str, initial_state: dict):
        self.algorythm = algorythm
        self.progress = 0
        self.move_sequence = []

        self.generate_move_sequence(initial_state)

    # przykladowa funkcja
    def get_next_move(self):
        move = self.move_sequence[self.progress]
        self.progress = (self.progress + 1) % len(self.move_sequence)
        print(f"Performing move: {move.value}")
        return move
    
    def get_upcoming_moves(self):
        return self.move_sequence[self.progress:min(len(self.move_sequence)-1,self.progress+5)]

    def generate_move_sequence(self, initial_state):
        if self.algorythm == "LBL":
            moves = self.solve_lbl(initial_state)
        else:
            moves = [
                RubiksMove.F, #RubiksMove.F_PRIME,
                RubiksMove.R, #RubiksMove.R_PRIME,
                RubiksMove.B, #RubiksMove.B_PRIME,
                RubiksMove.L, #RubiksMove.L_PRIME,
                RubiksMove.U, #RubiksMove.U_PRIME,
                RubiksMove.D, #RubiksMove.D_PRIME,
            ]

        # Randomize moves array
        #shuffle(moves)
        self.move_sequence = moves

    def solve_lbl(self, state):
        cube = RubiksCube(state)
        moves = []
        moves += white_cross(cube)
        moves += insert_bottom_corners(cube)
        moves += insert_edges(cube)
        moves += yellow_cross(cube)
        moves += allign_top_edges(cube)
        moves += position_top_corners(cube)
        moves += permutate_top_corners(cube)
        moves += last_move(cube)
        return moves
    
