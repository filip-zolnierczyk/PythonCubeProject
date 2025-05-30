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
    A_STAR = "A*" 

class RubiksAlgorithm:
    def __init__(self, algorythm: SolvingAlgorithms = SolvingAlgorithms.Test):
        self.algorythm = algorythm
        self.progress = 0
        self.move_sequence: list = []
        self.solving = False
        
        self.global_rotation_x = 0
        self.global_rotation_y = 0
        self.global_rotation_z = 0

    # przykladowa funkcja
    def get_next_move(self) -> str:
        move = self.move_sequence[self.progress]
        self.progress += 1
        if self.progress == len(self.move_sequence):
            self.solving = False
        #print(f"Performing move: {move}")

        if move[0] == 'X': self.global_rotation_x += 1 if len(move) == 1 else -1
        if move[0] == 'Y': self.global_rotation_y += 1 if len(move) == 1 else -1
        if move[0] == 'Z': self.global_rotation_z += 1 if len(move) == 1 else -1

        return move
    
    def get_next_move_transposed(self) -> str:
        move = self.get_next_move()
        
        if (self.global_rotation_x,self.global_rotation_y,self.global_rotation_z) == (0,0,0):
            return move
        
        if is_reposition_move(move):
            return move
        
        # else transpose move
        special = move[1] if len(move) == 2 else ""
        shifted_base_move = shift_move_xyz(move[0],self.global_rotation_x,self.global_rotation_y,self.global_rotation_z)
        return shifted_base_move+special

    def is_solving(self):
        return self.solving

    def get_upcoming_moves(self, move_num=upcoming_move_num_display) -> list:
        if self.move_sequence == None or len(self.move_sequence) == 0: return []
        return self.move_sequence[max(0,self.progress):min(len(self.move_sequence),self.progress+move_num)]

    def get_upcoming_move_num(self) -> int:
        if self.move_sequence == None: return 0
        return len(self.move_sequence)-self.progress-upcoming_move_num_display

    def is_solving(self):
        return self.progress <= len(self.move_sequence)-1

    def reset_solver(self):
        self.move_sequence = []
        self.progress = 0
        self.global_rotation_x = 0
        self.global_rotation_y = 0
        self.global_rotation_z = 0

    def select_rubiks_algorythm(self, alg: SolvingAlgorithms):
        self.algorythm = alg
        self.solving = False
        self.reset_solver()

    def run_rubiks_solver(self, rubiks_state: dict):
        self.solving = True
        self.reset_solver()

        print(f"Solving with algorythm: {self.algorythm}")

        match self.algorythm:
            case SolvingAlgorithms.LBL:
                self.move_sequence = solve_lbl(rubiks_state)
            case SolvingAlgorithms.Kociemba:
                self.move_sequence = solve_kociemba(rubiks_state)
            case SolvingAlgorithms.A_STAR:
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
            
        # make all moves upper
        for i in range(len(self.move_sequence)):
            self.move_sequence[i] = self.move_sequence[i].upper()