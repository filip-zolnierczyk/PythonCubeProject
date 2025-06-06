from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from util.vector_util import mul_vector, add_vectors, V3_ZERO
from util.colour_util import COLOR_MAP

# Wierzchołki kostki (znormalizowane -> dlugosc boku = 1)
vertices = [
    (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5),
    (-0.5, -0.5,  0.5), (0.5, -0.5,  0.5), (0.5, 0.5,  0.5), (-0.5, 0.5,  0.5)
]

# Ściany kostki
faces = [
    (4, 5, 6, 7),  # Przód
    (0, 3, 7, 4),  # Lewo
    (0, 1, 2, 3),  # Tył
    (1, 2, 6, 5),   # Prawo
    (2, 3, 7, 6),  # Góra
    (0, 1, 5, 4)  # Dół
]

mini_cube_ix_shift = [
    [0,3,6,1,4,7,2,5,8], # column to row shift
    [0,1,2,3,4,5,6,7,8],
    [0,3,6,1,4,7,2,5,8], # column to row shift
    [0,1,2,3,4,5,6,7,8],
    [0,1,2,3,4,5,6,7,8],
    [0,1,2,3,4,5,6,7,8],
]

def draw_cube(origin=V3_ZERO, size=1, colours=['x' for _ in range(6)], local_rotation=0, rotation_v=None):
    glPushMatrix()

    # Przesunięcie do pozycji środka obrotu
    glTranslatef(*origin)

    # Jeśli podano oś obrotu, wykonaj obrót
    if rotation_v is not None:
        glRotatef(local_rotation, *rotation_v)

    glBegin(GL_QUADS)
    for i, f in enumerate(faces):
        glColor3fv(COLOR_MAP[colours[i]])
        for v in f:
            glVertex3fv(mul_vector(vertices[v], size))
    glEnd()

    glPopMatrix()
