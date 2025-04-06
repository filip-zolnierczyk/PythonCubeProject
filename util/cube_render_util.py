from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from util.vector_util import mul_vector, add_vectors, V3_ZERO
from util.colour_util import COLOR_MAP
from util.orientation_util import code_to_orientation

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

def draw_cube(origin=V3_ZERO,size=1,colours=['x'for _ in range(6)]):
    glBegin(GL_QUADS)
    for key,f in faces.items():
        glColor3fv( COLOR_MAP[colours[code_to_orientation(key).value]] ) # black
        for v in f:
            vert_pos = vertices[v]
            glVertex3fv(add_vectors(tuple(origin),mul_vector(vert_pos,size)))
    glEnd()
