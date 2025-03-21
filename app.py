import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *

def main():
    # Initialize pygame
    pygame.init()
    
    # Set up display
    display = (800, 600)  # Window size
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL Window")

    # Set up OpenGL
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Background color (black)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # Exit on pressing ESC
                    running = False

        # Clear the screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Swap buffers to display the frame
        pygame.display.flip()
        pygame.time.wait(10)  # Small delay to limit frame rate

    pygame.quit()

if __name__ == "__main__":
    main()