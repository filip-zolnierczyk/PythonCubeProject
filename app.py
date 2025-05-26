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
rotation_angle_x = 0.0
rotation_angle_y = 0.0
clock = None
rubiks_display = None
rubiks_data = None
rubiks_algorithm = None
running = True
ui = None
display = None

def init():
    global clock, rubiks_data, rubiks_display, rotation_angle_x, rotation_angle_y, rubiks_algorithm, view_angle_anim_x, view_angle_anim_y, pause_solver, ui, display

    # init pygame window
    pygame.init()
    display = (WINDOW_WIDTH, WINDOW_HEIGHT)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Rubik's Cube")
    
    # init opengl
    glutInit()
    glEnable(GL_DEPTH_TEST) 
    glClearColor(0.2, 0.2, 0.2, 1.0)
    gluPerspective(45, (WINDOW_WIDTH / WINDOW_HEIGHT), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    glRotatef(45, 1, 1, 0)

    # app data
    clock = pygame.time.Clock()
    rotation_angle_x = 0
    view_angle_anim_x = None
    view_angle_anim_y = None
    pause_solver = True
    display = (WINDOW_WIDTH, WINDOW_HEIGHT)
    ui = ui_file.AppUI(display)
    ui.create_all_ui_elements()

    # initialize cube data
    rubiks_data = RubiksCube()
    #rubiks_data.scramble_cube()
    
    # initalize solver 
    rubiks_algorithm = RubiksAlgorithm()
    rubiks_algorithm.select_rubiks_algorythm(SolvingAlgorithms.Scramble)
    ui.update_ui_elements(rubiks_algorithm, pause_solver)
    rubiks_algorithm.run_rubiks_solver(rubiks_data.sides)

    # initalize cube display
    rubiks_display = RubiksCubeDisplay(3, V3(0,0,0), 0.8, rubiks_data.sides)

def loop(dt):
    global rubiks_data, rubiks_display, rotation_angle_x, rubiks_algorithm, view_angle_anim_x, pause_solver, ui, display


    # animacja zmiany widoku kostki (strzalki <- i -> )
    if view_angle_anim_x is not None and view_angle_anim_x.is_animating(dt):
        rotation_angle_x = view_angle_anim_x.get_animation_value()
    glRotatef(rotation_angle_x, 0, 1, 0)

    # animacja ruchu scianki kostki
    finished_anim = rubiks_display.update_animation(dt)

    # pobranie nowego ruchu z algorytmu do wyswietlenia 
    if finished_anim:
        # update kolorow z poprzedniego ruchu
        if not rubiks_display.is_currently_coloured():
            rubiks_display.reset_all_animations()
            rubiks_display.set_all_colours(rubiks_data.sides)

        # nowy ruch kostki
        if not pause_solver:
            if rubiks_algorithm.is_solving():
                move = rubiks_algorithm.get_next_move_transposed()
                move_viewport_x_with_move(move)
                rubiks_data.perform_move(move)            
                rubiks_display.animate_move(move, MOVE_DURATION)
        
        ui.update_ui_elements(rubiks_algorithm, not pause_solver)

    rubiks_display.draw()  # Rysowanie kostki Rubika

def move_viewport_x_with_move(move: str):
    if move == 'X': move_viewport_x(True)
    if move == "X'": move_viewport_x(False)

def move_viewport_x(side: bool):
    global view_angle_anim_x
    view_angle_anim_x = Animation(VIEW_CHANGE_DURATION,rotation_angle_x,rotation_angle_x+VIEW_CHANGE_AMOUNT*(-1 if side else 1))

def main():
    global clock, rotation_angle_x, rotation_angle_y, view_angle_anim_x, view_angle_anim_y, pause_solver, ui, display, rubiks_algorithm, rubiks_data

    init()

    while True:
        dt = clock.tick(60) / 1000  # czas od poprzedniej klatki w sekundach (max 60 FPS)

        # USER INPUT
        usr_quit_action = False
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                usr_quit_action = True

            # button inputs
            if (event.type == KEYDOWN):
                # change view
                if event.key == K_LEFT:
                    move_viewport_x(True)
                if event.key == K_RIGHT:
                    move_viewport_x(False)

                # pause solver
                if event.key == K_SPACE:
                    pause_solver = not pause_solver
                
                # select alg
                alg_changed = None
                if   event.key == K_1:  alg_changed = SolvingAlgorithms.LBL
                elif event.key == K_2:  alg_changed = SolvingAlgorithms.Kociemba
                elif event.key == K_8:  alg_changed = SolvingAlgorithms.Test
                elif event.key == K_9:  alg_changed = SolvingAlgorithms.Scramble

                if alg_changed is not None:
                    rubiks_algorithm.select_rubiks_algorythm(alg_changed)
                    rubiks_algorithm.run_rubiks_solver(rubiks_data.sides)
                    ui.update_ui_elements(rubiks_algorithm, not pause_solver)
                    pause_solver = True

                # other
                if (event.key == K_s):
                    rubiks_data.scramble_cube()

                # data imports
                if event.key == K_i:
                    img_col_data = get_imported_img_colour_data()
                    ui.set_custom_target(img_col_data)
                    pause_solver = True
                    ui.select_custom_target_cube(1,1)
                if event.key == K_o:
                    ui.remove_custom_target()
                    pause_solver = True
                elif event.key == K_c: 
                    img_import_sides = get_cube_by_video()
                    if img_import_sides is not None:
                        rubiks_data.set_colours(img_import_sides)

            ui.handle_event(event)

        if usr_quit_action: break
        
        # poczatek rysowania
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()

        # glowna petla programu
        loop(dt)

        # koniec rysowania
        glPopMatrix()
        ui.draw()
        pygame.display.flip()

        # Rysowanie UI po OpenGL
        screen_surface = pygame.display.get_surface()
    
    pygame.quit()

if __name__ == "__main__":
    main()
