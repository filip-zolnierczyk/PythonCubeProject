from util.rubiks_move_util import *
import random
from solving_algorithms.LBL_Algorithm import *
from solving_algorithms.Kociemba_Algorithm import *
from rubiks_data import RubiksCube

upcoming_move_num_display = 3

class SolvingAlgorithms(Enum):
    Kociemba = "Kociemba"
    LBL = "LBL"
    Test = "test"
    Scramble = "Scramble" 

class RubiksAlgorithm:
    def __init__(self, algorythm: SolvingAlgorithms = SolvingAlgorithms.Test):
        self.algorythm = algorythm
        self.progress = 0
        self.move_sequence: list = []
        self.solving = False

    # przykladowa funkcja
    def get_next_move(self):
        move = self.move_sequence[self.progress]
        self.progress += 1
        if self.progress == len(self.move_sequence):
            self.solving = False
        #print(f"Performing move: {move}")
        return move

    def is_solving(self):
        return self.solving

    def get_upcoming_moves(self, move_num=upcoming_move_num_display) -> list:
        if self.move_sequence == None or len(self.move_sequence) == 0: return []
        return self.move_sequence[max(0,self.progress-1):min(len(self.move_sequence)-1,self.progress+move_num)]

    def get_upcoming_move_num(self) -> int:
        if self.move_sequence == None: return 0
        return len(self.move_sequence)-self.progress-upcoming_move_num_display

    def select_rubiks_algorythm(self, alg: SolvingAlgorithms):
        self.algorythm = alg
        self.solving = False
        self.move_sequence = []

    def run_rubiks_solver(self, rubiks_state: dict):
        self.solving = True
        self.progress = 0

        print(f"Solving with algorythm: {self.algorythm}")

        match self.algorythm:
            case SolvingAlgorithms.LBL:
                self.move_sequence = solve_lbl(rubiks_state)
            case SolvingAlgorithms.Kociemba:
                self.move_sequence = solve_kociemba(rubiks_state)
            case SolvingAlgorithms.Test:
                self.move_sequence = [ "F", "R", 'B', 'L', 'U', 'D' ]
            case SolvingAlgorithms.Scramble:
                faces = ['U', 'D', 'L', 'R', 'F', 'B']
                modifiers = ['', "'", '2']
                scramble = []
                prev_face = None

                for _ in range(25):
                    face = random.choice(faces)
                    while face == prev_face: face = random.choice(faces) # unikaj powtorzen scian
                    move = face + random.choice(modifiers)
                    scramble.append(move)
                    prev_face = face

                self.move_sequence = scramble
            case _: 
                return ValueError("Solving for invalid algorythm name: !" + self.algorythm)