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

""" 
    green - front
    red - left
    blue - back
    orange - right
    yellow - top
    white - bottom
"""

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
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = int(WINDOW_WIDTH * (9/16))
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
    pause_solver = False
    display = (WINDOW_WIDTH, WINDOW_HEIGHT)
    ui = ui_file.AppUI(display)
    ui.create_bottom_ui_panel()
    ui.create_selected_alg_text()

    # initialize cube data
    rubiks_data = RubiksCube()
    #rubiks_data.scramble_cube()
    
    # initalize solver 
    rubiks_algorithm = RubiksAlgorithm()
    rubiks_algorithm.select_rubiks_algorythm(SolvingAlgorithms.Kociemba)
    ui.update_alg_selected(rubiks_algorithm)
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
                ui.update_bottom_ui_panel(rubiks_algorithm)
                move = rubiks_algorithm.get_next_move()
                rubiks_data.perform_move(move)            
                rubiks_display.animate_move(move, 0.8)

    rubiks_display.draw()  # Rysowanie kostki Rubika
        
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
            
            # Input do zmian orientacji patrzenia na kostke
            VIEW_CHANGE_DURATION = 1.25
            VIEW_CHANGE_AMOUNT = 90

            # button inputs
            if (event.type == KEYDOWN):
                # change view
                if (event.key == K_LEFT):
                    view_angle_anim_x = Animation(VIEW_CHANGE_DURATION,rotation_angle_x,rotation_angle_x+VIEW_CHANGE_AMOUNT)
                if (event.key == K_RIGHT):
                    view_angle_anim_x = Animation(VIEW_CHANGE_DURATION,rotation_angle_x,rotation_angle_x-VIEW_CHANGE_AMOUNT)

                # pause solver
                if (event.type == KEYDOWN and event.key == K_SPACE):
                    pause_solver = not pause_solver
                if (event.type == KEYDOWN and event.key == K_p):
                    pause_solver = False
                
                # select alg
                alg_changed = None
                if   event.key == K_1:  alg_changed = SolvingAlgorithms.LBL
                elif event.key == K_2:  alg_changed = SolvingAlgorithms.Kociemba
                elif event.key == K_8:  alg_changed = SolvingAlgorithms.Test
                elif event.key == K_9:  alg_changed = SolvingAlgorithms.Scramble

                if alg_changed is not None:
                    rubiks_algorithm.select_rubiks_algorythm(alg_changed)
                    rubiks_algorithm.run_rubiks_solver(rubiks_data.sides)
                    ui.update_alg_selected(rubiks_algorithm)
                    ui.update_bottom_ui_panel(rubiks_algorithm)
                    pause_solver = True

                # other
                if (event.key == K_s):
                    rubiks_data.scramble_cube()

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
