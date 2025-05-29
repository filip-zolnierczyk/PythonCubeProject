from util.ui_util import *
from solving_algorithms.rubiks_algorithm import RubiksAlgorithm
from util.colour_util import preview_colour_map

info_blue = (71/255,116/255,173/255)
ERROR_DISPLAY_TIME = 4.0

class AppUI:
    def __init__(self, display_size):
        self.display_size = display_size
        self.elements = []  # Lista przechowująca elementy UI
        self.moves_text = None

        self.target_preview_cubes = []  # list of lists [row][col]
        self.selected = (0, 0)
        self.custom_target = False

        self.cube_size = 3

        self.clock_err = pygame.time.Clock()
        self.clock_msg = pygame.time.Clock()
        self.error_displayed = False
        self.msg_displayed = False
        self.onscreen_msg_timer_err = 0
        self.onscreen_msg_timer_msg = 0
        self.onscreen_text_err = None
        self.onscreen_text_msg = None

        self.alg_selected_imgs = None
        self.speed_imgs = None
        self.img_preview_minipanel = None

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
        self.alg_selected_imgs = {
            "LBL": create_img(0, currentHeight, panel_width, alg_select_height, "images/select lbl.png"),
            "Kociemba": create_img(0, currentHeight, panel_width, alg_select_height, "images/select kociemba.png"),
            "A*": create_img(0, currentHeight, panel_width, alg_select_height, "images/select a star.png"),
            "Scramble": create_img(0, currentHeight, panel_width, alg_select_height, "images/select scramble.png"),
            "test": create_img(0, currentHeight, panel_width, alg_select_height, "images/select test.png")
        }
        currentHeight += alg_select_height

        # play pause minipanel init
        play_pause_height = 43/101*h*fill_mult
        pause_minipanel = create_img(0,currentHeight,panel_width,play_pause_height,"images/pause_img.png")
        play_minipanel  = create_img(0,currentHeight,panel_width,play_pause_height,"images/playing_img.png")
        self.play_pause_minipanels = [play_minipanel, pause_minipanel]
        currentHeight += play_pause_height

        # moves display minipanel init
        moves_height = 24/101*h*fill_mult
        moves_minipanel = create_img(0,currentHeight,panel_width,moves_height,"images/moves_img.png")
        self.moves_text = create_text(panel_width*0.125,currentHeight-moves_height*2.232,"F      G, F', B ...",font_size=25) #placeholder text
        currentHeight += moves_height

        # speed selection
        speed_img_h = 17/100*h*fill_mult
        self.speed_imgs = [
            create_img(0,currentHeight,panel_width,speed_img_h,"images/speed1.png"),
            create_img(0,currentHeight,panel_width,speed_img_h,"images/speed2.png"),
            create_img(0,currentHeight,panel_width,speed_img_h,"images/speed3.png")
        ]

        # left bg panel
        left_info_panel = create_panel(0,0,panel_width,h,colour=info_blue, border_colour=(0,0,0), border_width=w*0.01, )

        # add elements
        for img in self.alg_selected_imgs.values():
            self.add_element(img)
        for img in self.speed_imgs:
            self.add_element(img)
        self.add_element(self.play_pause_minipanels[0])
        self.add_element(self.play_pause_minipanels[1])
        self.add_element(moves_minipanel)
        self.add_element(self.moves_text)
        self.add_element(left_info_panel, -1)

    def update_ui_elements(self, rubiks_alg: RubiksAlgorithm, is_playing: bool, speed: float):
        
        for key, img in self.alg_selected_imgs.items(): # self.alg_selected_imgs is a dict with key str
            img.set_visible(key == rubiks_alg.algorythm.value)

        if len(self.play_pause_minipanels) == 2:
            self.play_pause_minipanels[0].set_visible(is_playing)
            self.play_pause_minipanels[1].set_visible(not is_playing)

        moves_arr = rubiks_alg.get_upcoming_moves()
        moves_num = rubiks_alg.get_upcoming_move_num()

        self.speed_imgs[0].set_visible(speed >= 2)
        self.speed_imgs[1].set_visible(speed == 1)
        self.speed_imgs[2].set_visible(speed <= 0)

        self.img_preview_minipanel.set_visible(self.custom_target)

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

        if self.error_displayed:
            dt = self.clock_err.tick(60) / 1000
            self.onscreen_msg_timer_err += dt
            if self.onscreen_msg_timer_err > ERROR_DISPLAY_TIME:
                self.error_displayed = False
                self.onscreen_text_err.set_visible(False)
        if self.msg_displayed:
            dt = self.clock_msg.tick(60) / 1000
            self.onscreen_msg_timer_msg += dt
            if self.onscreen_msg_timer_msg > ERROR_DISPLAY_TIME:
                self.msg_displayed = False
                self.onscreen_text_msg.set_visible(False)

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

        # camera and image import display minipanel init
        cam_import_height = 25/118*h*fill_mult
        img_import_minipanel = create_img(panel_start,currentHeight,panel_width,cam_import_height,"images/img_import_img.png")
        currentHeight += cam_import_height
        cam_import_minipanel = create_img(panel_start,currentHeight,panel_width,cam_import_height,"images/camera_import_img.png")
        currentHeight += cam_import_height
        manual_import_minipanel = create_img(panel_start,currentHeight,panel_width,cam_import_height,"images/manual_import.png")
        currentHeight += cam_import_height

        # rubiks image preview minipanel init
        img_preview_height = 40/118*h*fill_mult
        self.img_preview_minipanel  = create_img(panel_start,currentHeight,panel_width,img_preview_height,"images/img9_img.png")
        self.preview_x_span = (panel_start+panel_width*33/69, panel_start+panel_width*59/69)
        self.preview_y_span = (currentHeight+img_preview_height*9/39, currentHeight+img_preview_height*35/39)
        currentHeight += img_preview_height


        # right bg panel
        right_info_panel = create_panel(panel_start,0,panel_width,h,colour=info_blue, border_colour=(0,0,0), border_width=w*0.01, )

        # add elements
        self.add_element(self.target_select_minipanels[0])
        self.add_element(self.target_select_minipanels[1])
        self.add_element(self.img_preview_minipanel)
        self.add_element(cam_import_minipanel)
        self.add_element(img_import_minipanel)
        self.add_element(manual_import_minipanel)
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
        
        self.preview_colour_data = colour_data



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
                pnl = create_panel(px, py, cell_w*1.03, cell_h*1.03,
                                   colour=preview_colour_map[colour_data[i][j]])
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
        for i, row in enumerate(self.target_preview_cubes):
            for j, pnl in enumerate(row):
                if (i//self.cube_size,j//self.cube_size)==self.selected:
                    pnl.colour = preview_colour_map[self.preview_colour_data[i][j]]
                else:
                    pnl.colour = colour_mult(preview_colour_map[self.preview_colour_data[i][j]], 0.25)

    def print_onscreen(self, txt, is_error = False):
        w, h = self.display_size

        if self.onscreen_text_err is None or self.onscreen_text_msg is None:
            self.onscreen_text_err = create_text(w*0.3,h*0.9,"",colour=(255,0,0),font_size=15)
            self.onscreen_text_msg = create_text(w*0.3,h*0.1,"",colour=(255,255,255),font_size=15)
            self.onscreen_text_err.set_visible(False)
            self.onscreen_text_msg.set_visible(False)
            self.add_element(self.onscreen_text_err)
            self.add_element(self.onscreen_text_msg)

        if is_error: 
            print("ERROR: " + txt)
            self.onscreen_text_err.text = "ERROR " + txt
            self.onscreen_msg_timer_err = 0
            self.onscreen_text_err.set_visible(True)
            self.error_displayed = True
            self.clock_err = pygame.time.Clock()
        else:
            print("Message: " + txt)
            self.onscreen_msg_timer_msg = 0
            self.onscreen_text_msg.text = txt
            self.onscreen_text_msg.set_visible(True)
            self.msg_displayed = True
            self.clock_msg = pygame.time.Clock()

    def print_onscreen_error(self, err: str):
        self.print_onscreen(err, True)

    def print_onscreen_message(self, msg: str):
        self.print_onscreen(msg, False)

    def select_custom_target_cube(self, row, col):
        self.selected = (col, row)
        self.highlight_selected()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for element in self.elements:
                pass

def colour_mult(col: tuple, mult: float):
    r,g,b = col
    return (r*mult,g*mult,b*mult)