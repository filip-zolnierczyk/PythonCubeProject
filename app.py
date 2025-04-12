import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import rubiks_data as rubiks_data_file
import rubiks_display as rubiks_display_file
import rubiks_algorythm as rubiks_algorythm_file
from util.vector_util import V3_ZERO
from util.animation_util import *

""" 
    green - front
    red - right
    blue - back
    orange - left
    yellow - top
    white - bottom
"""

# zmienne globalne
rotation_angle_x = 0.0
rotation_angle_y = 0.0
clock = None
rubiks_display = None
rubiks_data = None
rubiks_algorythm = None
running = True

def init():
    global clock, rubiks_data, rubiks_display, rotation_angle_x, rotation_angle_y, rubiks_algorythm, view_angle_anim_x, view_angle_anim_y, pause_solver

    # init pygame window
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Rubik's Cube")
    
    # init opengl
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.2, 0.2, 0.2, 1.0)
    gluPerspective(45, (800 / 600), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    glRotatef(45, 1, 1, 0)

    # app data
    clock = pygame.time.Clock()
    rotation_angle_x = 0
    view_angle_anim_x = None
    view_angle_anim_y = None
    pause_solver = False


    # initialize cube data
    rubiks_data = rubiks_data_file.RubiksCube()
    rubiks_display = rubiks_display_file.RubiksCubeDisplay(3, V3_ZERO, 1, rubiks_data.sides)
    rubiks_algorythm = rubiks_algorythm_file.RubiksAlgorythm("CFOP", rubiks_data.sides) # przykladowo

# test_col_dict = {
#     'g': "ggyrywybw",
#     'r': "ggyrywybw",
#     'b': "ggyrywybw",
#     'o': "ggyrywybw",
#     'y': "ggyrywybw",
#     'w': "ggyrywybw",
# }

def loop(dt):
    global rubiks_data, rubiks_display, rotation_angle_x, rubiks_algorythm, view_angle_anim_x, pause_solver

    glRotatef(rotation_angle_x, 0, 1, 0)

    # animacja zmiany widoku kostki (strzalki <- i -> )
    if view_angle_anim_x is not None and view_angle_anim_x.is_animating(dt):
        rotation_angle_x = view_angle_anim_x.get_animation_value()

    # animacja ruchu scianki kostki
    if rubiks_display.is_animating():
        rubiks_display.update_animation(dt)

    # pobranie nowego ruchu z algorytmu do wyswietlenia 
    else:
        # update kolorow z poprzedniego ruchu
        if not rubiks_display.is_currently_coloured():
            rubiks_display.set_all_colours(rubiks_data.sides)

        # nowy ruch kostki
        if not pause_solver:
            move = rubiks_algorythm.get_next_move()
            rubiks_data.perform_move(move)
            
            rubiks_display.animate_move(move, 0.8) # jesli bez animacji to trzeba wykomentowac

    rubiks_display.draw()  # Rysowanie kostki Rubika
        
def main():
    global clock, rotation_angle_x, rotation_angle_y, view_angle_anim_x, view_angle_anim_y, pause_solver

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

            if (event.type == KEYDOWN and event.key == K_LEFT):
                view_angle_anim_x = Animation(VIEW_CHANGE_DURATION,rotation_angle_x,rotation_angle_x+VIEW_CHANGE_AMOUNT)
            if (event.type == KEYDOWN and event.key == K_RIGHT):
                view_angle_anim_x = Animation(VIEW_CHANGE_DURATION,rotation_angle_x,rotation_angle_x-VIEW_CHANGE_AMOUNT)
            if (event.type == KEYDOWN and event.key == K_SPACE):
                pause_solver = not pause_solver

        if usr_quit_action: break
        
        # poczatek rysowania
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()

        # glowna petla programu
        loop(dt)

        # koniec rysowania
        glPopMatrix()
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()
