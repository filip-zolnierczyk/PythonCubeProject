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
from imgage_data_import import get_imported_img_colour_data

""" 
    green - front
    red - left
    blue - back
    orange - right
    yellow - top
    white - bottom
"""

# constants
MOVE_DURATION = 0.5
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
    p.ui.update_ui_elements(p.rubiks_algorithm, p.pause_solver)
    p.rubiks_algorithm.run_rubiks_solver(p.rubiks_data.sides)

    # initalize cube display
    p.rubiks_display = RubiksCubeDisplay(3, V3(0,0,0), 0.8, p.rubiks_data.sides)

def loop(dt):
    global p

    # animacja zmiany widoku kostki (strzalki <- i -> )
    if p.view_angle_anim_x is not None and p.view_angle_anim_x.is_animating(dt):
        p.rotation_angle_x = p.view_angle_anim_x.get_animation_value()
    glRotatef(p.rotation_angle_x, 0, 1, 0)

    # animacja ruchu scianki kostki
    finished_anim = p.rubiks_display.update_animation(dt)

    # pobranie nowego ruchu z algorytmu do wyswietlenia 
    if finished_anim:
        # update kolorow z poprzedniego ruchu
        if not p.rubiks_display.is_currently_coloured():
            p.rubiks_display.reset_all_animations()
            p.rubiks_display.set_all_colours(p.rubiks_data.sides)

        # nowy ruch kostki
        if not p.pause_solver:
            if p.rubiks_algorithm.is_solving():
                move = p.rubiks_algorithm.get_next_move_transposed()
                move_viewport_x_with_move(move)
                p.rubiks_data.perform_move(move)            
                p.rubiks_display.animate_move(move, MOVE_DURATION)
        
        p.ui.update_ui_elements(p.rubiks_algorithm, not p.pause_solver)

    p.rubiks_display.draw()  # Rysowanie kostki Rubika

def move_viewport_x_with_move(move: str):
    if move == 'X': move_viewport_x(True)
    if move == "X'": move_viewport_x(False)

def move_viewport_x(side: bool):
    global p
    p.view_angle_anim_x = Animation(VIEW_CHANGE_DURATION,p.rotation_angle_x,p.rotation_angle_x+VIEW_CHANGE_AMOUNT*(-1 if side else 1))

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
                if event.key == K_n:
                    move_viewport_x(True)
                if event.key == K_m:
                    move_viewport_x(False)

                # pause solver
                if event.key == K_SPACE:
                    pause_solver = not pause_solver
                
                # select alg
                alg_changed = None
                if   event.key == K_1:  alg_changed = SolvingAlgorithms.LBL
                elif event.key == K_2:  alg_changed = SolvingAlgorithms.Kociemba
                elif event.key == K_3:  alg_changed = SolvingAlgorithms.A_STAR
                elif event.key == K_4:  alg_changed = SolvingAlgorithms.Scramble
                elif event.key == K_5:  alg_changed = SolvingAlgorithms.Test

                if alg_changed is not None:
                    p.rubiks_algorithm.select_rubiks_algorythm(alg_changed)
                    p.rubiks_algorithm.run_rubiks_solver(p.rubiks_data.sides)
                    p.ui.update_ui_elements(p.rubiks_algorithm, not p.pause_solver)
                    p.pause_solver = True

                # other
                if (event.key == K_s):
                    p.rubiks_data.scramble_cube()

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

                # data imports
                if event.key == K_i:
                    if p.rubiks_algorithm.algorythm != SolvingAlgorithms.A_STAR:
                        p.ui.print_onscreen_error("Custom targets only work in A* Algorithm!")
                    else:
                        img_col_data = get_imported_img_colour_data()
                        p.target_size_x = len(img_col_data) // p.cube_size
                        p.target_size_y = len(img_col_data[0]) // p.cube_size
                        p.ui.set_custom_target(img_col_data)
                        pause_solver = True
                        p.ui.select_custom_target_cube(p.custom_cube_select_x, p.custom_cube_select_y)
                if event.key == K_o:
                    p.ui.remove_custom_target()
                    pause_solver = True
                elif event.key == K_c: 
                    img_import_sides = get_cube_by_video()
                    if img_import_sides is not None:
                        p.rubiks_data.set_colours(img_import_sides)

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
