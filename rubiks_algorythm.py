from util.rubiks_move_util import *

class RubiksAlgorythm:
    def __init__(self, algorythm: str, initial_state: dict):
        self.algorythm = algorythm

    # przykladowa funkcja
    def get_next_move(self):
        if self.algorythm == "CFOP":
            return RubiksMove.F
        else: 
            return RubiksMove.U