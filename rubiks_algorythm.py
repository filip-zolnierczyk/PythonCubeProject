from util.rubiks_move_util import *

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
        return move

    def generate_move_sequence(self, initial_state):
        if self.algorythm == "CFOP":
            self.move_sequence = [RubiksMove.F, RubiksMove.F_PRIME]
        else: 
            self.move_sequence = [RubiksMove.F_PRIME, RubiksMove.F]