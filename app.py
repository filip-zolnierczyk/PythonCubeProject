import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import cube
import cube_display
from vector_util import V3_ZERO

""" 
    green - front
    red - right
    blue - back
    orange - left
    yellow - top
    white - bottom
"""

rotation_angle = 0

def init():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Rubik's Cube")
    
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.2, 0.2, 0.2, 1.0)  # Szare tło
    gluPerspective(45, (800 / 600), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    glRotatef(45, 1, 1, 0)


def main():
    global rotation_angle
    
    init()

    rubiks_data = cube.RubiksCube(
        ["grgrgrgrgr", "rrrrgrrgrr", "bbrbbbbrbb", "oooowoowoo", "yybyybbyy", "wwwworbgww"]
    )
    rubiks_display = cube_display.RubiksCubeDisplay(3, V3_ZERO, 1, rubiks_data.sides)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glRotatef(rotation_angle, 0, 1, 0)
        rubiks_display.draw()  # Rysowanie kostki Rubika
        glPopMatrix()
        
        pygame.display.flip()
        pygame.time.wait(10)
        rotation_angle += 1  # Obrót kostki
    
    pygame.quit()

if __name__ == "__main__":
    main()
