from util.rubiks_move_util import *
from random import randint
from lbl_algorythms import *
from rubiks_data import RubiksCube

upcoming_move_num_display = 4

class RubiksAlgorythm:
    def __init__(self, algorythm: str = "LBL"):
        self.algorythm = algorythm
        self.progress = 0
        self.move_sequence = []
        self.solving = False

    # przykladowa funkcja
    def get_next_move(self):
        move = self.move_sequence[self.progress]
        self.progress += 1
        if self.progress == len(self.move_sequence):
            self.solving = False
        print(f"Performing move: {move.value}")
        return move

    def is_solving(self):
        return self.solving

    def get_upcoming_moves(self, move_num=upcoming_move_num_display):
        return self.move_sequence[self.progress:min(len(self.move_sequence)-1,self.progress+move_num)]

    def get_upcoming_move_num(self):
        return len(self.move_sequence)-self.progress-upcoming_move_num_display

    def select_rubiks_algorythm(self, alg: string):
        if alg not in ['LBL', 'test']:
            return ValueError(f"No algorythm called {alg} implemented!")
        else: 
            self.algorythm = alg

    def run_rubiks_solver(self, rubiks_state: dict):
        self.solving = True

        print(f"Solving with algorythm: {self.algorythm}")

        match self.algorythm:
            case "LBL":
                self.move_sequence = self.solve_lbl(rubiks_state)
            case "test":
                self.move_sequence = [
                    RubiksMove.F, #RubiksMove.F_PRIME,
                    RubiksMove.R, #RubiksMove.R_PRIME,
                    RubiksMove.B, #RubiksMove.B_PRIME,
                    RubiksMove.L, #RubiksMove.L_PRIME,
                    RubiksMove.U, #RubiksMove.U_PRIME,
                    RubiksMove.D, #RubiksMove.D_PRIME,
                ]
            case _: 
                return ValueError("Solving for invalid algorythm!")

    def solve_lbl(self, state):
        cube = RubiksCube(state)
        cube.clear_performed_moves()

        white_cross(cube)
        insert_bottom_corners(cube)
        insert_edges(cube)
        yellow_cross(cube)
        allign_top_edges(cube)
        position_top_corners(cube)
        permutate_top_corners(cube)
        last_move(cube)

        moves = cube.get_performed_moves()
        return moves