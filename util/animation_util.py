from util.vector_util import V3, V3_Z, V3_ZERO

class Animation:
    def __init__(self, duration, start_value, end_value, easing_function=None, reset_value=None):
        self.duration = duration
        self.time = 0
        self.start_value = start_value
        self.end_value = end_value
        self.easing_function = easing_function if easing_function else ease_in_out
        self.reset_value = reset_value

    def is_animating(self,dt):
        self.time += dt
        return self.time <= self.duration

    def get_animation_value(self):
        t = self.time / self.duration
        eased_t = self.easing_function(t)
        return self.start_value + (self.end_value - self.start_value) * eased_t
    
    def get_reset_value(self):
        return self.reset_value

def linear_easing(t):
    return t

def ease_in_out(t):
    if t < 0.5:
        return 2 * t * t
    else:
        return -1 + (4 * t) - (2 * t * t)
    
# zwraca zmapowanie z i = 0,1,2,...,l-1 na t = -1->1
def shift_coords(i:int,l: int):
    return (i/(l-1) - 0.5) * 2

""" 
    Funkcja zmiany pozycji mini-kostek w animacji rotacji scianek
    przyjmuje lokalne wektory scianki up i right, numer kwadratow na jednym boku (normalnie 3), rozmiar kostki i kat rotacji
    zwraca macierz zmian pozycji kazdej z mini-kostek
 """
def calc_rotation_matrix_for_rubiks_side(local_up: V3, local_right: V3, square_num: int, rubiks_size: float, degrees: float = 90):
    dp = [[V3_ZERO for _ in range(square_num)] for _ in range(square_num)] # macierz zmian pozycji
    for x in range(square_num):
        for y in range(square_num):
            local_v_from_middle = V3(shift_coords(x,square_num), shift_coords(y,square_num), 0)
            local_v_after_rotation = V3.rotate(local_v_from_middle, degrees, V3_Z) # rotacja wokol osi Z
            local_position_change = (local_v_after_rotation - local_v_from_middle) # zmiana pozycji
            global_position_change = local_position_change.x * local_right + local_position_change.y * local_up
            dp[x][y] = global_position_change * rubiks_size
    return dp


face_local_vectors = {
    'F':  (V3(0, 1, 0), V3(1, 0, 0), V3(0, 0, -1)),  # up, right, forward
    "F'": (V3(0, 1, 0), V3(1, 0, 0), V3(0, 0, -1)),

    'B':  (V3(0, 1, 0), V3(1, 0, 0), V3(0, 0, -1)),
    "B'": (V3(0, 1, 0), V3(1, 0, 0), V3(0, 0, -1)),

    'R':  (V3(0, 1, 0), V3(0, 0, -1), V3(1, 0, 0)),
    "R'": (V3(0, -1, 0), V3(0, 0, 1), V3(1, 0, 0)),

    'L':  (V3(0, 1, 0), V3(0, 0, -1), V3(1, 0, 0)),
    "L'": (V3(0, -1, 0), V3(0, 0, 1), V3(1, 0, 0)),

    'U':  (V3(0, 0, 1), V3(1, 0, 0), V3(0, 1, 0)),
    "U'": (V3(0, 0, 1), V3(1, 0, 0), V3(0, 1, 0)),

    'D':  (V3(0, 0, 1), V3(1, 0, 0), V3(0, 1, 0)),
    "D'": (V3(0, 0, 1), V3(1, 0, 0), V3(0, 1, 0)),
}
