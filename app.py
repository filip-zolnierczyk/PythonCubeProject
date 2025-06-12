import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from rubiks_data import RubiksCube
from rubiks_display import RubiksCubeDisplay
from solving_algorithms.rubiks_algorithm import RubiksAlgorithm, SolvingAlgorithms
from util.vector_util import V3_ZERO
from util.animation_util import *
import ui as ui_file
from video_capture import get_cube_by_video
from image_data_import import get_imported_img_colour_data
from manual_data_import import get_manual_import_data

""" 
    green - front
    red - left
    blue - back
    orange - right
    yellow - top
    white - bottom
"""

# constants
MOVE_DURATIONS = [0.8, 0.35, 0.075]
VIEW_CHANGE_DURATION = 1.25
VIEW_CHANGE_AMOUNT = 90

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = int(WINDOW_WIDTH * (9/16))

# zmienne globalne
class Params:
    def __init__(self):
        self.rotation_angle_x = 0.0
        self.rotation_angle_y = 0.0
        self.clock = None
        self.rubiks_display: RubiksCubeDisplay = None
        self.rubiks_data: RubiksCube = None
        self.rubiks_algorithm: RubiksAlgorithm = None
        self.running = True
        self.ui: ui_file.AppUI = None
        self.display = None
        self.stepping_mode = False
        self.goto_next_step = False
        self.view_angle_anim_x = 0
        self.view_angle_anim_y = 0
        self.pause_solver = False
        self.custom_cube_select_x = 0
        self.custom_cube_select_y = 0
        self.target_size_x = 0
        self.target_size_y = 0
        self.cube_size = 3
        self.move_duration_ix = len(MOVE_DURATIONS)//2
        self.timer_since_move = 0
        self.image_col_data = [[]]
p: Params = None

def init():
    global p

    p = Params()

    # init pygame window
    pygame.init()
    p.display = (WINDOW_WIDTH, WINDOW_HEIGHT)
    pygame.display.set_mode(p.display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Rubik's Cube")

    # init opengl
    glutInit()
    glEnable(GL_DEPTH_TEST) 
    glClearColor(0.2, 0.2, 0.2, 1.0)
    gluPerspective(45, (WINDOW_WIDTH / WINDOW_HEIGHT), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    glRotatef(45, 1, 1, 0)

    # app data
    p.clock = pygame.time.Clock()
    p.rotation_angle_x = 0
    p.rotation_angle_y = 0
    p.view_angle_anim_x = None
    p.view_angle_anim_y = None
    p.pause_solver = True
    p.ui = ui_file.AppUI(p.display)
    p.ui.create_all_ui_elements()

    # initialize cube data
    p.rubiks_data = RubiksCube()
    #rubiks_data.scramble_cube()
    
    # initalize solver 
    p.rubiks_algorithm = RubiksAlgorithm()
    p.rubiks_algorithm.select_rubiks_algorythm(SolvingAlgorithms.Scramble)
    p.ui.update_ui_elements(p.rubiks_algorithm, p.pause_solver, p.move_duration_ix)
    p.rubiks_algorithm.run_rubiks_solver(p.rubiks_data.sides)

    # initalize cube display
    p.rubiks_display = RubiksCubeDisplay(3, V3(0,0,0), 0.8, p.rubiks_data.sides)


def loop(dt):
    global p

    # animacja zmiany widoku kostki (horizontal  a<- i ->d )
    if p.view_angle_anim_x is not None and p.view_angle_anim_x.is_animating(dt):
        p.rotation_angle_x = p.view_angle_anim_x.get_animation_value()
    glRotatef(p.rotation_angle_x, 0, 1, 0)

    # animacja zmiany widoku kostki (strzalki w ^ i v s  )
    if p.view_angle_anim_y is not None and p.view_angle_anim_y.is_animating(dt):
        p.rotation_angle_y = p.view_angle_anim_y.get_animation_value()
    glRotatef(p.rotation_angle_y, 1, 0, 0)

    # animacja ruchu scianki kostki
    finished_anim = p.rubiks_display.update_animation(dt)

    # pobranie nowego ruchu z algorytmu do wyswietlenia 
    if finished_anim:
        # update kolorow z poprzedniego ruchu
        if not p.rubiks_display.is_currently_coloured():
            p.rubiks_display.reset_all_animations()
            p.rubiks_display.set_all_colours(p.rubiks_data.sides)

        # nowy ruch kostki
        normal_mode_bool = not p.pause_solver and not p.stepping_mode and p.rubiks_algorithm.is_solving() and p.timer_since_move >= 1.3*MOVE_DURATIONS[p.move_duration_ix]
        step_mode_bool = p.stepping_mode and p.goto_next_step

        if (normal_mode_bool or step_mode_bool) and not p.rubiks_display.is_animating() and p.rubiks_algorithm.is_solving():
            move = p.rubiks_algorithm.get_next_move_transposed()
            if p.move_duration_ix <= 1: move_viewport_x_with_move(move)
            p.rubiks_data.perform_move(move)            
            p.rubiks_display.animate_move(move, MOVE_DURATIONS[p.move_duration_ix])
            p.timer_since_move = 0
            p.goto_next_step = False

        if not p.pause_solver:
            p.timer_since_move += dt
        
    p.ui.update_ui_elements(p.rubiks_algorithm, not p.pause_solver, p.move_duration_ix)
    p.rubiks_display.draw()  # Rysowanie kostki Rubika

def move_viewport_x_with_move(move: str):
    if move == 'X': move_viewport_x(True)
    if move == "X'": move_viewport_x(False)

def move_viewport_x(side: bool):
    global p
    p.view_angle_anim_x = Animation(VIEW_CHANGE_DURATION,p.rotation_angle_x,p.rotation_angle_x+VIEW_CHANGE_AMOUNT*(-1 if side else 1))

def move_viewport_y(side: bool):
    global p
    p.view_angle_anim_y = Animation(VIEW_CHANGE_DURATION,p.rotation_angle_y,p.rotation_angle_y+VIEW_CHANGE_AMOUNT*(-1 if side else 1))

def select_custom_target(target_data: list):
    global p

    if target_data is None:
        print("Empty custom target data!")
        return
    
    p.image_col_data = target_data
    p.target_size_x = len(target_data[0]) // p.cube_size
    p.target_size_y = len(target_data) // p.cube_size
    p.custom_cube_select_x = p.custom_cube_select_y = 0
    p.ui.set_custom_target(p.image_col_data)
    p.ui.select_custom_target_cube(p.custom_cube_select_x, p.custom_cube_select_y)
    p.rubiks_algorithm.select_rubiks_algorythm(SolvingAlgorithms.Picture)
    run_custom_target_solver()
    p.ui.update_ui_elements(p.rubiks_algorithm, not p.pause_solver, p.move_duration_ix)

def run_custom_target_solver():
    global p

    target_face = []
    x_offset = p.custom_cube_select_x * p.cube_size
    y_offset = p.custom_cube_select_y * p.cube_size

    for x in range(p.cube_size):
        for y in range(p.cube_size): 
            target_face.append( p.image_col_data[y_offset+y][x_offset+x])

    p.rubiks_algorithm.run_rubiks_solver(p.rubiks_data.sides, target_face)
    p.pause_solver = True

def main():
    global p

    init()

    while True:
        dt = p.clock.tick(60) / 1000  # czas od poprzedniej klatki w sekundach (max 60 FPS)

        # USER INPUT
        usr_quit_action = False
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                usr_quit_action = True

            # button inputs
            if (event.type == KEYDOWN):
                # change view
                if event.key == K_a:
                    move_viewport_x(False)
                if event.key == K_d:
                    move_viewport_x(True)
                if event.key == K_w:
                    move_viewport_y(True)
                if event.key == K_s:
                    move_viewport_y(False)

                if event.key == K_n:
                    p.goto_next_step = p.stepping_mode

                # pause solver
                if event.key == K_SPACE:
                    if p.stepping_mode:
                        p.stepping_mode = False
                        p.ui.print_onscreen_message("Stepping mode disabled")
                    p.pause_solver = not p.pause_solver
                
                # select alg
                alg_changed = None
                if   event.key == K_1:  alg_changed = SolvingAlgorithms.LBL
                elif event.key == K_2:  alg_changed = SolvingAlgorithms.Kociemba
                elif event.key == K_3:  
                    alg_changed = SolvingAlgorithms.Picture
                    select_custom_target([[2,5,2],[5,2,5],[2,5,2]])
                elif event.key == K_4:  alg_changed = SolvingAlgorithms.Scramble
                elif event.key == K_5:  alg_changed = SolvingAlgorithms.Test

                if alg_changed is not None and alg_changed != p.rubiks_algorithm.algorythm:
                    if p.rubiks_algorithm.algorythm == SolvingAlgorithms.Picture:
                        p.ui.remove_custom_target()
                    p.rubiks_algorithm.select_rubiks_algorythm(alg_changed)
                    if alg_changed != SolvingAlgorithms.Picture:
                        p.rubiks_algorithm.run_rubiks_solver(p.rubiks_data.sides)
                    p.ui.update_ui_elements(p.rubiks_algorithm, not p.pause_solver, p.move_duration_ix)
                    p.pause_solver = True

                # custom target
                if (event.key == K_z):
                    print("Stepping mode active")
                    p.ui.print_onscreen_message("Stepping Mode Enabled")
                    p.stepping_mode = True
                    p.pause_solver = True
                if event.key == K_x:
                    p.ui.print_onscreen_message("Stepping Mode Disabled")
                    print("Stepping mode disabled")
                    p.stepping_mode = False 

                if p.ui.custom_target and event.key in [K_LEFT, K_RIGHT, K_DOWN, K_UP]:
                    if event.key == K_LEFT:
                        p.custom_cube_select_x = p.custom_cube_select_x - 1 if p.custom_cube_select_x > 0 else (p.target_size_x-1)
                    if event.key == K_RIGHT:
                        p.custom_cube_select_x = (p.custom_cube_select_x+1)%p.target_size_x
                    if event.key == K_UP:
                        p.custom_cube_select_y = p.custom_cube_select_y - 1 if p.custom_cube_select_y > 0 else (p.target_size_y-1)
                    if event.key == K_DOWN:
                        p.custom_cube_select_y = (p.custom_cube_select_y+1)%p.target_size_y
                    
                    p.ui.select_custom_target_cube(p.custom_cube_select_x, p.custom_cube_select_y)
                    run_custom_target_solver()

                if p.ui.custom_target and event.key == K_b:
                    p.ui.remove_custom_target()
                    p.pause_solver = True
                
                # speed selections
                if event.key == K_MINUS or event.key == K_EQUALS:
                    if event.key == K_EQUALS:
                        p.move_duration_ix = min(len(MOVE_DURATIONS)-1,p.move_duration_ix+1)
                    elif event.key == K_MINUS:
                        p.move_duration_ix = max(0,p.move_duration_ix-1)

                # data imports
                if event.key == K_i:
                    p.rubiks_algorithm.select_rubiks_algorythm(SolvingAlgorithms.Picture)
                    select_custom_target( get_imported_img_colour_data() )

                elif event.key == K_c: 
                    p.ui.print_onscreen_message("Getting camera input ... (please wait)")
                    cam_import_sides = get_cube_by_video()
                    if cam_import_sides is not None:
                        p.rubiks_data.set_colours(cam_import_sides)
                        p.rubiks_display.set_all_colours(cam_import_sides)
                    p.pause_solver = True
                elif event.key == K_m:
                    man_import_sides = get_manual_import_data()
                    if man_import_sides is not None:
                        p.rubiks_data.set_colours(man_import_sides)
                        p.rubiks_display.set_all_colours(man_import_sides)
                    p.pause_solver = True

            p.ui.handle_event(event)

        if usr_quit_action: break
        
        # poczatek rysowania
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()

        # glowna petla programu
        loop(dt)

        # koniec rysowania
        glPopMatrix()
        p.ui.draw()
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()
