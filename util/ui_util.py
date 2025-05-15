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
    def __init__(self, x, y, text, font_size=16, color=(255, 255, 255)):
        super().__init__(x, y, 0, 0)
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.font_size = font_size  # Placeholder, font rendering requires extra setup

    def draw(self, display_size=None):
        font = pygame.font.Font(pygame.font.get_default_font(), self.font_size)
        text_surface = font.render(self.text, True, self.color).convert_alpha()
        text_data = pygame.image.tostring(text_surface, "RGBA", True)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glWindowPos2f(self.x,self.y)
        glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)

class Image(UIElement):
    def __init__(self, x, y, width, height, image_path):
        super().__init__(x, y, width, height)
        self.texture_id = None
        self.image_path = image_path
        self.image_width = 0
        self.image_height = 0
        self._load_texture()

    def _load_texture(self):
        surface = pygame.image.load(self.image_path).convert_alpha()
        image_data = pygame.image.tostring(surface, "RGBA")
        self.image_width, self.image_height = surface.get_size()

        self.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.image_width, self.image_height, 0,
                     GL_RGBA, GL_UNSIGNED_BYTE, image_data)

    def draw(self, display_size):
        if not self.visible or self.texture_id is None:
            return

        x, y, w, h = self.x, self.y, self.width, self.height
        screen_w, screen_h = display_size

        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glColor4f(1.0, 1.0, 1.0, 1.0)

        # 2D ortho matrix
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, screen_w, screen_h, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        # Rysowanie skalowanego prostokąta z teksturą
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex2f(x, y)
        glTexCoord2f(1, 0)
        glVertex2f(x + w, y)
        glTexCoord2f(1, 1)
        glVertex2f(x + w, y + h)
        glTexCoord2f(0, 1)
        glVertex2f(x, y + h)
        glEnd()

        glDisable(GL_TEXTURE_2D)

        # Restore matrix
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)


# ============ UTIL METHODS ============

def create_panel(x, y, width, height, **kwargs):
    return Panel(x, y, width, height, **kwargs)

def create_button(x, y, width, height, **kwargs):
    return Button(x, y, width, height, **kwargs)

def create_text(x, y, text, **kwargs):
    return Text(x, y, text, **kwargs)

def create_img(x,y, width,height, path):
    return Image(x,y,width,height,path)

def position_relative(display_size, rel_x=0.0, rel_y=0.0, width=100, height=50):
    """Pozycjonowanie w zaleznosci od rozdzielczosci: rel_x, rel_y od 0.0 do 1.0"""
    disp_w, disp_h = display_size
    x = int(rel_x * disp_w)
    y = int(rel_y * disp_h)
    return x, y, width, height
