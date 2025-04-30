# from util.ui_util import *

# class AppUI:
#     def __init__(self, display_size):
#         self.display_size = display_size
#         self.elements = []  # Lista przechowująca elementy UI

#     def add_element(self, element):
#         self.elements.append(element)

#     def draw(self):
#         # Rysowanie wszystkich elementów UI
#         for element in self.elements:
#             element.draw(self.display_size)
    
#     def create_bottom_ui_panel(self):
#         w,h = self.display_size
#         self.add_element(create_panel(w//10,h-w//40-h//6,w-(w//10)*2,h//6))

#     def handle_event(self, event):
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             for element in self.elements:
#                 if element['type'] == 'button' and element['rect'].collidepoint(event.pos):
#                     if element['callback']:
#                         element['callback']()