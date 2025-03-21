import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import renderer as renderer

def init_opengl_window():
    # Initialize pygame
    pygame.init()
    
    # Set up display
    display = (800, 600)  # Window size
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL Window")

    renderer.render_init()
    
    # Set up OpenGL
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Background color (black)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

def user_input():
    for event in pygame.event.get():
        if event.type == QUIT:
            return False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:  # Exit on pressing ESC
                return False
    return True

# Clear the screen
def clear():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

def loop():
    renderer.render_loop()

def draw():    
    # Swap buffers to display the frame
    pygame.display.flip()
    pygame.time.wait(10)  # Small delay to limit frame rate

def main():
    init_opengl_window()

    while 1:
        if not user_input(): break
        clear()
        loop()
        draw()

    pygame.quit()

if __name__ == "__main__":
    main()