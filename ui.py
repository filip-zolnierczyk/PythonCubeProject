from util.ui_util import *
from solving_algorithms.rubiks_algorithm import RubiksAlgorithm

class AppUI:
    def __init__(self, display_size):
        self.display_size = display_size
        self.elements = []  # Lista przechowująca elementy UI
        self.moves_text = None
        self.alg_selected_text = None

    def add_element(self, element):
        self.elements.append(element)

    def draw(self):
        # Rysowanie wszystkich elementów UI
        for element in self.elements:
            element.draw(self.display_size)
    
    def create_bottom_ui_panel(self):
        w,h = self.display_size
        
        img_w = 1500
        img_h = 383
        width = 0.6*w
        px,py,pw,ph = (w-width)/2, (h-width*img_h/img_w), width, width*img_h/img_w
        self.add_element(create_img(px,py,pw,ph,"images/test_img.png"))
        
        px,py = w*0.49, width*img_h/img_w/6
        self.moves_text = create_text(px,py,"F   G, F', B ...",font_size=40) #placeholder text
        self.add_element(self.moves_text)

    def create_selected_alg_text(self):
        w,h = self.display_size
        self.alg_selected_text = create_text(w*0.02, h*0.90, "Selected: ---", font_size=30)
        self.add_element(self.alg_selected_text)

    def update_bottom_ui_panel(self,cube_alg: RubiksAlgorithm):
        moves_arr = cube_alg.get_upcoming_moves()
        moves_num = cube_alg.get_upcoming_move_num()

        text = ""
        if len(moves_arr) != 0: 
            text = moves_arr[0] + "       "
            for i in range(1,len(moves_arr)):
                if i < len(moves_arr)-1:
                    text += moves_arr[i] + ", " 
                else:
                    text += moves_arr[i] + " ..."
            if moves_num > 0:
                text += f" ({moves_num})"
        else:
            text = "       Solved!"
        self.moves_text.text = text

    def update_alg_selected(self,cube_alg: RubiksAlgorithm):
        self.alg_selected_text.text = "Selected: " + cube_alg.algorythm.value

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for element in self.elements:
                pass