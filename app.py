import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import rubiks_data as rubiks_data_file
import rubiks_display as rubiks_display_file
import rubiks_algorythm as rubiks_algorythm_file
from util.vector_util import V3_ZERO

""" 
    green - front
    red - right
    blue - back
    orange - left
    yellow - top
    white - bottom
"""

# zmienne globalne
rotation_angle = 0.0
clock = None
rubiks_display = None
rubiks_data = None
rubiks_algorythm = None
running = True

def init():
    global clock, rubiks_data, rubiks_display, rotation_angle, rubiks_algorythm

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
    rotation_angle = 0

    # initialize cube data
    rubiks_data = rubiks_data_file.RubiksCube(
        ["grgrgrgrgr", "rrrrgrrgrr", "bbrbbbbrbb", "oooowoowoo", "yybyybbyy", "wwwworbgww"]
    )
    rubiks_display = rubiks_display_file.RubiksCubeDisplay(3, V3_ZERO, 1, rubiks_data.sides)
    rubiks_algorythm = rubiks_algorythm_file.RubiksAlgorythm("CFOP", rubiks_data.sides) # przykladowo

def loop(dt):
    global rubiks_data, rubiks_display, rotation_angle, rubiks_algorythm

    # rotacja kostki
    rotation_angle += 60 * dt  # 60 stopni na sekundę
    glRotatef(rotation_angle, 0, 1, 0)

    # integracja z algorytmem ukladania kostki
    if rubiks_display.animating:
        rubiks_display.update_animation(dt)
    else:
        # update kolorow z poprzedniego ruchu
        rubiks_display.set_all_colours(rubiks_data.sides)

        # nowy ruch kostki
        move = rubiks_algorythm.get_next_move()
        rubiks_data.perform_move(move)
        rubiks_display.animate_move(move, 4)

    rubiks_display.draw()  # Rysowanie kostki Rubika
        
def main():
    global clock

    init()

    while True:
        dt = clock.tick(60) / 1000  # czas od poprzedniej klatki w sekundach (max 60 FPS)

        # USER INPUT
        usr_quit_action = False
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                usr_quit_action = True
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
