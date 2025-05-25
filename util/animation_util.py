from util.vector_util import V3, V3_Z, V3_ZERO

class Animation:
    def __init__(self, duration, start_value, end_value, easing_function=None, reset_value=None):
        self.duration = duration
        self.time = 0

        self.current_animation_step = 1
        self.last_animation_step_t = 0.0
        self.next_animation_step_t = 1.0

        self.animation_timeline = [(0.0,start_value),(1.0,end_value)]
        self.easing_function = easing_function if easing_function else ease_in_out
        self.reset_value = reset_value

    def add_animation_mid_steps(self, t: float, value: float):
        self.animation_timeline.append( (t,value) )
        self.animation_timeline.sort(key = lambda x : x[0]) # sortujemy po parametrze t w krokach animacji
        self.next_animation_step_t = min(self.next_animation_step_t, t) #assume animation not started yet

    def is_animating(self,dt):
        self.time += dt
        return self.time <= self.duration

    def get_animation_value(self):
        t = self.time / self.duration
        eased_t = self.easing_function(t)

        if self.current_animation_step < len(self.animation_timeline)-1 and eased_t >= self.next_animation_step_t:
            self.current_animation_step += 1
            self.last_animation_step_t = self.next_animation_step_t
            self.next_animation_step_t = self.animation_timeline[self.current_animation_step][0]

        last_t, origin_value = self.animation_timeline[self.current_animation_step - 1]
        target_t, target_value = self.animation_timeline[self.current_animation_step]
        step_t = (eased_t-last_t) / (target_t - last_t)
        return origin_value + (target_value - origin_value) * step_t
    
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
            dp[y][x] = global_position_change * rubiks_size
    return dp


face_local_vectors = {
    'F':  (V3(0, -1, 0), V3(1, 0, 0)),
    "F'": (V3(0, -1, 0), V3(1, 0, 0)),
    'B':  (V3(0, -1, 0), V3(-1, 0, 0)),
    "B'": (V3(0, -1, 0), V3(-1, 0, 0)),
    'R':  (V3(0, -1, 0), V3(0, 0, -1)),
    "R'": (V3(0, -1, 0), V3(0, 0, -1)),
    'L':  (V3(0, -1, 0), V3(0, 0, 1)), 
    "L'": (V3(0, -1, 0), V3(0, 0, 1)), 
    'U':  (V3(0, 0, 1), V3(1, 0, 0)),
    "U'": (V3(0, 0, 1), V3(1, 0, 0)),
    'D':  (V3(0, 0, -1), V3(1, 0, 0)),  
    "D'": (V3(0, 0, -1), V3(1, 0, 0)), 
}
