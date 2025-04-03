import math
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import cube
import util

# Mapa kolorów dla ścianek kostki Rubika
COLOR_MAP = {
    'w': (1, 1, 1),  # Biały
    'r': (1, 0, 0),  # Czerwony
    'b': (0, 0, 1),  # Niebieski
    'o': (1, 0.5, 0),  # Pomarańczowy
    'g': (0, 1, 0),  # Zielony
    'y': (1, 1, 0)   # Żółty
}

# Wierzchołki kostki (znormalizowane -> dlugosc boku = 1)
vertices = [
    (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5),
    (-0.5, -0.5,  0.5), (0.5, -0.5,  0.5), (0.5, 0.5,  0.5), (-0.5, 0.5,  0.5)
]

# Ściany kostki
faces = {
    'g': (4, 5, 6, 7),  # Przód
    'r': (1, 2, 6, 5),   # Prawo
    'b': (0, 1, 2, 3),  # Tył
    'o': (0, 3, 7, 4),  # Lewo
    'y': (2, 3, 7, 6),  # Góra
    'w': (0, 1, 5, 4)  # Dół
}

""" 
    green - front
    red - right
    blue - back
    orange - left
    yellow - top
    white - bottom
"""

rotation_angle = 0

def draw_face(face_key, face_colours, scale):
    glBegin(GL_QUADS)
    
    # podstawowe dlugosci
    square_num = len(face_colours)
    cube_side_square_num = int(math.sqrt(square_num))
    square_side_len = (scale/cube_side_square_num)

    # oblicz wektory wzdluz scianki
    v1, v2, v3, v4 = (util.mul_vector(vertices[x],scale) for x in faces[face_key])
    vector_x = util.sub_vectors(v2,v1)
    vector_y = util.sub_vectors(v4,v1)

    # narysuj wszystkie kwadraty na sciance (9 dla 3x3)
    for y in range(cube_side_square_num):
        for x in range(cube_side_square_num):
            # wybierz kolor kwadratu
            square_ix = y*3 + x
            colour = COLOR_MAP[face_colours[square_ix]]
            glColor3fv(colour)
            
            # oblicz offset obecnego kwadratu wzgledem scianki
            offset_x = util.mul_vector(vector_x,x*square_side_len)
            offset_y = util.mul_vector(vector_y,y*square_side_len)
            offset = util.add_vectors(offset_x,offset_y)

            # oblicz wszystkie 4 katu obecnego kwadratu (po kolei przeciwko wskazowkom zegara)
            SQUARE_MULT = 0.95
            pos1 = util.add_vectors(v1,offset) # lewo dol
            pos2 = util.add_vectors(pos1, util.mul_vector(vector_x,square_side_len*SQUARE_MULT))
            pos3 = util.add_vectors(pos2, util.mul_vector(vector_y,square_side_len*SQUARE_MULT))
            pos4 = util.add_vectors(pos1, util.mul_vector(vector_y,square_side_len*SQUARE_MULT))

            # wyslij pozycje do opengl
            glVertex3fv(pos1); glVertex3fv(pos2); glVertex3fv(pos3); glVertex3fv(pos4)
    
    glEnd()

def draw_cube(scale):
    glBegin(GL_QUADS)
    glColor3fv( (0.1,0.1,0.1) ) # black
    for key,f in faces.items():
        for v in f:
            glVertex3fv(util.mul_vector(vertices[v],scale))
    glEnd()

def draw_rubiks_cube(cube_state, scale):
    draw_cube(scale*0.99)
    for face_key,face_colours in cube_state.items():
        draw_face(face_key, face_colours, scale)

def init():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Rubik's Cube")
    
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.2, 0.2, 0.2, 1.0)  # Szare tło
    gluPerspective(45, (800 / 600), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    glRotatef(45, 45, 45, 0)


def main():
    global rotation_angle
    init()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        #glRotatef(rotation_angle, 1, 1, 0)
        c = cube.RubiksCube(
            ["grgrgrgrgr", "rrrrgrrgrr", "bbrbbbbrbb", "oooowoowoo", "yybyybbyy", "wwwworbgww"]
        )
        draw_rubiks_cube(c.sides, 1)
        glPopMatrix()
        
        pygame.display.flip()
        pygame.time.wait(10)
        #rotation_angle += 1  # Obrót kostki
    
    pygame.quit()

if __name__ == "__main__":
    main()
