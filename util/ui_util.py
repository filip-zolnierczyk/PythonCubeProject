from OpenGL.GL import *
import pygame

class UIElement:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.visible = True

    def draw(self, display_size):
        pass

    def handle_event(self, event):
        pass

class Panel(UIElement):
    def __init__(self, x, y, width, height, color=(0.17,0.17,0.17), border_color=None, border_width=0, radius=0):
        super().__init__(x, y, width, height)
        self.color = color
        self.border_color = border_color
        self.border_width = border_width
        self.radius = radius

    def draw(self, display_size):
        if not self.visible:
            return

        screen_w, screen_h = display_size

        # Przejście w tryb rysowania 2D (bez perspektywy)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, screen_w, screen_h, 0, -1, 1)  # układ: (0,0) w lewym górnym rogu
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glColor3f(*self.color)
        glBegin(GL_QUADS)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + self.width, self.y)
        glVertex2f(self.x + self.width, self.y + self.height)
        glVertex2f(self.x, self.y + self.height)
        glEnd()

        # Ramka (opcjonalnie)
        if self.border_color and self.border_width > 0:
            glLineWidth(self.border_width)
            glColor3f(*self.border_color)
            glBegin(GL_LINE_LOOP)
            glVertex2f(self.x, self.y)
            glVertex2f(self.x + self.width, self.y)
            glVertex2f(self.x + self.width, self.y + self.height)
            glVertex2f(self.x, self.y + self.height)
            glEnd()
            
        # Przywrócenie macierzy
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

class Button(Panel):
    def __init__(self, x, y, width, height, color=(0.8, 0.8, 0.8), border_color=(0,0,0), text="", callback=None):
        super().__init__(x, y, width, height, color, border_color, border_width=2)
        self.text = text
        self.callback = callback

    def handle_event(self, event):
        if not self.visible:
            return
        if event.type == 5:  # pygame.MOUSEBUTTONDOWN
            mx, my = event.pos
            if self.x <= mx <= self.x + self.width and self.y <= my <= self.y + self.height:
                if self.callback:
                    self.callback()

class Text(UIElement):
    def __init__(self, x, y, text, color=(1, 1, 1), font_size=16):
        super().__init__(x, y, 0, 0)
        self.text = text
        self.color = color
        self.font_size = font_size  # Placeholder, font rendering requires extra setup

    def draw(self):
        # To implement: Requires font rendering (e.g. using freetype)
        pass

# ============ UTIL METHODS ============

def create_panel(x, y, width, height, **kwargs):
    return Panel(x, y, width, height, **kwargs)

def create_button(x, y, width, height, **kwargs):
    return Button(x, y, width, height, **kwargs)

def create_text(x, y, text, **kwargs):
    return Text(x, y, text, **kwargs)

def position_relative(display_size, rel_x=0.0, rel_y=0.0, width=100, height=50):
    """Pozycjonowanie w zaleznosci od rozdzielczosci: rel_x, rel_y od 0.0 do 1.0"""
    disp_w, disp_h = display_size
    x = int(rel_x * disp_w)
    y = int(rel_y * disp_h)
    return x, y, width, height
