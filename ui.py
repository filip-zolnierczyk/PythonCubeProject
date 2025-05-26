from util.ui_util import *
from solving_algorithms.rubiks_algorithm import RubiksAlgorithm

info_blue = (71/255,116/255,173/255)

class AppUI:
    def __init__(self, display_size):
        self.display_size = display_size
        self.elements = []  # Lista przechowująca elementy UI
        self.moves_text = None
        self.alg_selected_text = None

        self.target_preview_cubes = []  # list of lists [row][col]
        self.selected = (0, 0)
        self.custom_target = False

        self.cube_size = 3

    def add_element(self, element, priority = 0):
        self.elements.append((element,priority))
        self.elements.sort(key = lambda x : x[1], reverse=True)

    def draw(self):
        # Rysowanie wszystkich elementów UI
        for element, priority in self.elements:
            element.draw(self.display_size)
    
    def create_all_ui_elements(self):
        self.create_left_info_panel()
        self.create_right_info_panel()

    def create_left_info_panel(self):
        # basic data
        w,h = self.display_size
        panel_width = w*0.25
        self.play_pause_minipanels = []
        fill_mult = 0.65
        currentHeight = 0

        # algorithm select minipanel init
        alg_select_height = 51/101*h*fill_mult
        alg_select_minipanel = create_img(0,currentHeight,panel_width,alg_select_height,"images/algs_img.png")
        self.alg_selected_text = create_text(w*0.03, h*0.88, "---", font_size=25, bg_colour=info_blue)
        currentHeight += alg_select_height

        # play pause minipanel init
        play_pause_height = 25/101*h*fill_mult
        pause_minipanel = create_img(0,currentHeight,panel_width,play_pause_height,"images/pause_img.png")
        play_minipanel  = create_img(0,currentHeight,panel_width,play_pause_height,"images/playing_img.png")
        self.play_pause_minipanels = [play_minipanel, pause_minipanel]
        currentHeight += play_pause_height

        # moves display minipanel init
        moves_height = 24/101*h*fill_mult
        moves_minipanel = create_img(0,currentHeight,panel_width,moves_height,"images/moves_img.png")
        self.moves_text = create_text(panel_width*0.125,currentHeight-moves_height*0.7,"F      G, F', B ...",font_size=25) #placeholder text
        currentHeight += moves_height

        # left bg panel
        left_info_panel = create_panel(0,0,panel_width,h,colour=info_blue, border_colour=(0,0,0), border_width=w*0.01, )

        # add elements
        self.add_element(alg_select_minipanel)
        self.add_element(self.alg_selected_text)
        self.add_element(self.play_pause_minipanels[0])
        self.add_element(self.play_pause_minipanels[1])
        self.add_element(moves_minipanel)
        self.add_element(self.moves_text)
        self.add_element(left_info_panel, -1)

    def update_ui_elements(self, rubiks_alg: RubiksAlgorithm, is_playing: bool):
        if self.alg_selected_text is not None:
            self.alg_selected_text.text = rubiks_alg.algorythm.value

        if len(self.play_pause_minipanels) == 2:
            self.play_pause_minipanels[0].set_visible(is_playing)
            self.play_pause_minipanels[1].set_visible(not is_playing)

        moves_arr = rubiks_alg.get_upcoming_moves()
        moves_num = rubiks_alg.get_upcoming_move_num()

        if self.moves_text is not None:
            text = ""
            if len(moves_arr) != 0: 
                text = moves_arr[0] + "     "
                for i in range(1,len(moves_arr)):
                    if i < len(moves_arr)-1:
                        text += moves_arr[i] + ", " 
                    else:
                        text += moves_arr[i] + " ..."
                if moves_num > 0:
                    text += f" ({moves_num})"
            else:
                text = "        Solved!"
            self.moves_text.text = text

    def create_right_info_panel(self):
        # basic data
        w,h = self.display_size
        panel_width = w*0.25
        panel_start = w*0.75
        fill_mult = 0.75
        currentHeight = 0

        # target minipanel init
        target_select_height = 32/118*h*fill_mult
        target_full_minipanel = create_img(panel_start,currentHeight,panel_width,target_select_height,"images/target_full_img.png")
        target_custom_minipanel = create_img(panel_start,currentHeight,panel_width,target_select_height,"images/target_custom_img.png")
        self.target_select_minipanels = [target_full_minipanel, target_custom_minipanel]
        currentHeight += target_select_height

        # rubiks image preview minipanel init
        img_preview_height = 40/118*h*fill_mult
        img_preview_minipanel  = create_img(panel_start,currentHeight,panel_width,img_preview_height,"images/img9_img.png")
        self.preview_x_span = (panel_start+panel_width*33/69, panel_start+panel_width*59/69)
        self.preview_y_span = (currentHeight+img_preview_height*9/39, currentHeight+img_preview_height*35/39)
        currentHeight += img_preview_height

        # camera and image import display minipanel init
        cam_import_height = 25/118*h*fill_mult
        img_import_minipanel = create_img(panel_start,currentHeight,panel_width,cam_import_height,"images/img_import_img.png")
        currentHeight += cam_import_height
        cam_import_minipanel = create_img(panel_start,currentHeight,panel_width,cam_import_height,"images/camera_import_img.png")
        currentHeight += cam_import_height

        # right bg panel
        right_info_panel = create_panel(panel_start,0,panel_width,h,colour=info_blue, border_colour=(0,0,0), border_width=w*0.01, )

        # add elements
        self.add_element(self.target_select_minipanels[0])
        self.add_element(self.target_select_minipanels[1])
        self.add_element(img_preview_minipanel)
        self.add_element(cam_import_minipanel)
        self.add_element(img_import_minipanel)
        self.add_element(right_info_panel, -1)

    def toggle_custom_target(self, val:bool):
        self.custom_target = val

        for x in range(len(self.target_preview_cubes)):
            for y in range(len(self.target_preview_cubes[0])):
                self.target_preview_cubes[x][y].set_visible(self.custom_target)

        if len(self.target_select_minipanels)==2:
            self.target_select_minipanels[0].set_visible(not self.custom_target)
            self.target_select_minipanels[1].set_visible(self.custom_target)
    
    def set_cube_size(self, size: int):
        self.cube_size = size

    def set_custom_target(self, colour_data: list):
        self.remove_custom_target()

        if colour_data is None: 
            print("Cannot target empty image!")
            return
        
        # colour map
        colour_map = [
            (1,1,1), 
            (1,1,0),
            (0,1,0),     
            (0,0,1),     
            (1,165/255,0),
            (1,0,0),     
        ]

        # cube preview region definitions
        x_start, x_end = self.preview_x_span
        y_start, y_end = self.preview_y_span

        # create cube panels grid
        rows, cols = len(colour_data[0]), len(colour_data) 
        cell_w = (x_end-x_start) / cols
        cell_h = (y_end-y_start) / rows
        
        for i in range(rows):
            row_panels = []
            for j in range(cols):
                px = x_start + j*cell_w
                py = y_start + i*cell_h
                pnl = create_panel(px, py, cell_w*1.01, cell_h*1.01,
                                   colour=colour_map[colour_data[i][j]],
                                   border_colour=(0,0,0), border_width=1)
                self.add_element(pnl, 1)
                row_panels.append(pnl)
            self.target_preview_cubes.append(row_panels)

        self.toggle_custom_target(True)
        
    def remove_custom_target(self):
        self.toggle_custom_target(False)
        
        if len(self.target_preview_cubes) != 0:
            for tpc in self.target_preview_cubes:
                self.elements.remove(tpc)
        self.target_preview_cubes = []

    def highlight_selected(self):
        pass
        # for i, row in enumerate(self.target_preview_cubes):
        #     for j, pnl in enumerate(row):
        #         if (i//self.cube_size,j//self.cube_size)==self.selected:
        #             pnl.colour = (1,1,1)
        #         else:
        #             pnl.colour = (0.5,0.5,0.5)

    def select_custom_target_cube(self, row, col):
        self.selected = (row, col)
        self.highlight_selected()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for element in self.elements:
                pass