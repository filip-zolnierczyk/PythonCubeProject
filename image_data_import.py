#!/usr/bin/env python3
# rubiks_ui.py

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import numpy as np
import math

# Paleta kolorów Rubika (z emoji i nazwami)
CUBE_COLORS = {
    0: {'rgb': (255,255,255), 'name': 'White',  'emoji': '⬜'},
    1: {'rgb': (255,255,0),   'name': 'Yellow', 'emoji': '🟨'},
    2: {'rgb': (0,255,0),     'name': 'Green',  'emoji': '🟩'},
    3: {'rgb': (0,0,255),     'name': 'Blue',   'emoji': '🟦'},
    4: {'rgb': (255,165,0),   'name': 'Orange', 'emoji': '🟧'},
    5: {'rgb': (255,0,0),     'name': 'Red',    'emoji': '🟥'},
}

class ImgImportUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Rubik's Image to Cube Pattern")
        self.state('zoomed')

        # zmienne
        self.image = None
        self.img_tk = None
        self.processed_pattern = None
        self.brightness = tk.DoubleVar(value=1.0)
        self.contrast = tk.DoubleVar(value=1.0)
        self.blur = tk.BooleanVar(value=False)
        self.cube_type = tk.IntVar(value=3)
        self.count_x = tk.IntVar(value=3)
        self.count_y = tk.IntVar(value=3)
        # tolerancje kolorów 0-2
        self.tolerance = {k: tk.DoubleVar(value=1.0) for k in CUBE_COLORS.keys()}

        self._build_ui()

    def _build_ui(self):
        # lewy panel
        ctrl = ttk.Frame(self, padding=10)
        ctrl.pack(side='left', fill='y')

        ttk.Button(ctrl, text="Import Image", command=self.import_image).pack(fill='x', pady=5)

        # cube type dropdown
        ttk.Label(ctrl, text="Rodzaj kostki:").pack(anchor='w')
        ttk.Combobox(ctrl, textvariable=self.cube_type, values=[2,3,4], state='readonly').pack(fill='x', pady=2)

        # counts
        ttk.Label(ctrl, text="Ilość kostek X:").pack(anchor='w')
        ttk.Entry(ctrl, textvariable=self.count_x).pack(fill='x', pady=2)
        ttk.Label(ctrl, text="Ilość kostek Y:").pack(anchor='w')
        ttk.Entry(ctrl, textvariable=self.count_y).pack(fill='x', pady=2)

        # filters
        ttk.Label(ctrl, text="Filters:").pack(anchor='w', pady=(10,0))
        ttk.Label(ctrl, text="Brightness").pack(anchor='w')
        ttk.Scale(ctrl, from_=0.1, to=2.0, variable=self.brightness, orient='horizontal').pack(fill='x')
        ttk.Label(ctrl, text="Contrast").pack(anchor='w')
        ttk.Scale(ctrl, from_=0.1, to=2.0, variable=self.contrast, orient='horizontal').pack(fill='x')
        ttk.Checkbutton(ctrl, text="Blur", variable=self.blur).pack(anchor='w', pady=5)

        # tolerance section (optional)
        tol_frame = ttk.Labelframe(ctrl, text="Color Tolerance (opt)")
        tol_frame.pack(fill='x', pady=10)
        for k, info in CUBE_COLORS.items():
            ttk.Label(tol_frame, text=f"{info['emoji']} {info['name']}").pack(anchor='w')
            ttk.Scale(tol_frame, from_=0.0, to=2.0, variable=self.tolerance[k], orient='horizontal').pack(fill='x')

        # action buttons
        ttk.Button(ctrl, text="Generate Preview", command=self.generate_preview).pack(fill='x', pady=5)
        ttk.Button(ctrl, text="Accept Image", command=self.accept).pack(fill='x', pady=5)

        # środki panel - preview obrazka i kostki
        preview_frame = ttk.Frame(self, padding=10)
        preview_frame.pack(side='left', fill='both', expand=True)

        self.canvas_img = tk.Canvas(preview_frame, bg='grey')
        self.canvas_cube = tk.Canvas(preview_frame, bg='white')
        self.canvas_img.pack(side='left', fill='both', expand=True)
        self.canvas_cube.pack(side='left', fill='both', expand=True)

    def import_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files","*.png;*.jpg;*.jpeg;*.bmp")])
        if not path: return
        self.image = Image.open(path).convert('RGB')
        self.show_image(self.image)

    def show_image(self, img):
        # dopasuj tak samo do obu canvases
        w = self.canvas_img.winfo_width()
        h = self.canvas_img.winfo_height()
        size = (w, h)
        img_resized = img.copy().resize(size, Image.BICUBIC)
        self.img_tk = ImageTk.PhotoImage(img_resized)
        for c in (self.canvas_img, self.canvas_cube):
            c.delete('all')
        self.canvas_img.create_image(0,0,anchor='nw', image=self.img_tk)

    def apply_filters(self, img):
        img = ImageEnhance.Brightness(img).enhance(self.brightness.get())
        img = ImageEnhance.Contrast(img).enhance(self.contrast.get())
        if self.blur.get(): img = img.filter(ImageFilter.BLUR)
        return img

    def reduce_to_cube(self, img):
        fx = self.count_x.get() * self.cube_type.get()
        fy = self.count_y.get() * self.cube_type.get()
        img_small = img.resize((fx, fy), Image.BICUBIC)
        arr = np.array(img_small)
        res = np.zeros((fy, fx), dtype=int)
        for i in range(fy):
            for j in range(fx):
                res[i,j] = self.closest_color_tol(tuple(arr[i,j]))
        return res

    def closest_color_tol(self, rgb):
        dlist = [(math.dist(rgb, info['rgb']), k) for k, info in CUBE_COLORS.items()]
        dlist.sort()
        d0, k0 = dlist[0]
        d1, k1 = dlist[1]
        thr = self.tolerance[k0].get() * math.dist((0,0,0),(255,255,255))
        return k0 if d0 <= thr else k1

    def generate_preview(self):
        if not self.image:
            messagebox.showerror("Error","No image imported")
            return
        img_f = self.apply_filters(self.image)
        self.show_image(img_f)
        pattern = self.reduce_to_cube(img_f)
        self.processed_pattern = pattern
        self.draw_cube(pattern)

    def draw_cube(self, pattern):
        self.canvas_cube.delete('all')
        h, w = pattern.shape
        cw = self.canvas_cube.winfo_width()/w
        ch = self.canvas_cube.winfo_height()/h
        for i in range(h):
            for j in range(w):
                rgb = CUBE_COLORS[pattern[i,j]]['rgb']
                color = '#%02x%02x%02x' % rgb
                self.canvas_cube.create_rectangle(j*cw, i*ch, (j+1)*cw, (i+1)*ch, fill=color, outline='black')

    def accept(self):
        self.destroy()

def get_imported_img_colour_data():
    app = ImgImportUI()
    app.mainloop()

    if hasattr(app, 'processed_pattern'):
        print("Imported data from img:")
        print(app.processed_pattern)
        return app.processed_pattern
    
    return None
