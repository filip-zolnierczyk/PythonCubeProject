import tkinter as tk
from tkinter import messagebox

VALID_COLORS = {
    "W": (255, 255, 255),  # White
    "Y": (255, 255, 0),    # Yellow
    "R": (255, 0, 0),      # Red
    "O": (255, 165, 0),    # Orange
    "B": (0, 0, 255),      # Blue
    "G": (0, 128, 0)       # Green
}

FACE_POSITIONS = {
    "U": (1, 0),
    "L": (0, 1),
    "F": (1, 1),
    "R": (2, 1),
    "B": (3, 1),
    "D": (1, 2)
}

def get_default_face_data():
    return {
        "U": ["Y"] * 9,
        "D": ["W"] * 9,
        "F": ["G"] * 9,
        "B": ["B"] * 9,
        "L": ["R"] * 9,
        "R": ["O"] * 9,
    }

class ManualColorEntry:
    def __init__(self, master, callback):
        self.master = master
        self.callback = callback
        self.entries = {}
        self.face_data = get_default_face_data()

        self.root = tk.Toplevel(master)
        self.root.title("Manual Cube Color Entry")

        self.canvas = tk.Frame(self.root)
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)

        self.info_frame = tk.Frame(self.root)
        self.info_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        self.draw_color_legend()
        self.draw_preview()

        self.accept_button = tk.Button(self.root, text="Validate & Accept", command=self.validate_and_return)
        self.accept_button.pack(side=tk.BOTTOM, pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def draw_color_legend(self):
        tk.Label(self.info_frame, text="Color Legend:", font=("Arial", 12, "bold")).pack(anchor="w")
        for k in VALID_COLORS:
            color_hex = f'#{VALID_COLORS[k][0]:02x}{VALID_COLORS[k][1]:02x}{VALID_COLORS[k][2]:02x}'
            row = tk.Frame(self.info_frame)
            row.pack(anchor="w", pady=2)
            color_preview = tk.Label(row, width=2, bg=color_hex, relief="ridge")
            color_preview.pack(side=tk.LEFT)
            label = tk.Label(row, text=f"  {k} = {color_preview_color_name(k)}")
            label.pack(side=tk.LEFT)

    def draw_preview(self):
        self.cells = {}
        cell_size = 30

        for face, (grid_x, grid_y) in FACE_POSITIONS.items():
            for i in range(3):
                for j in range(3):
                    index = i * 3 + j
                    val = self.face_data[face][index]
                    color = VALID_COLORS.get(val, (150, 150, 150))
                    color_hex = f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}'

                    e = tk.Entry(self.canvas, width=2, justify='center', fg="gray")
                    placeholder = val
                    e.insert(0, placeholder)
                    e.config(bg="white")

                    if index == 4:
                        e.config(state="disabled", disabledbackground=color_hex)
                    else:
                        e.bind("<FocusIn>", lambda event, p=placeholder: self.clear_placeholder(event, p))
                        e.bind("<FocusOut>", lambda event, p=placeholder: self.restore_placeholder(event, p))
                        e.bind("<KeyRelease>", lambda event, face=face, index=index: self.on_key(event, face, index))

                    e.grid(row=(grid_y * 3 + i), column=(grid_x * 3 + j), padx=1, pady=1)
                    self.cells[(face, index)] = e

    def clear_placeholder(self, event, placeholder):
        if event.widget.get() == placeholder and event.widget.cget("fg") == "gray":
            event.widget.delete(0, tk.END)
            event.widget.config(fg="black")

    def restore_placeholder(self, event, placeholder):
        if not event.widget.get():
            event.widget.insert(0, placeholder)
            event.widget.config(fg="gray")

    def on_key(self, event, face, index):
        entry = event.widget
        value = entry.get().upper()
        if value in VALID_COLORS:
            color = VALID_COLORS[value]
            color_hex = f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}'
            entry.configure(bg=color_hex)
            self.face_data[face][index] = value
            next_index = index + 1
            if next_index < 9 and (face, next_index) in self.cells:
                self.cells[(face, next_index if next_index != 4 else 5)].focus_set()

    def validate_and_return(self):
        counts = {k: 0 for k in VALID_COLORS}
        for face in self.face_data:
            for val in self.face_data[face]:
                if val not in VALID_COLORS:
                    messagebox.showerror("Invalid Input", f"Invalid color code: {val}")
                    return
                counts[val] += 1

        for color, count in counts.items():
            if count != 9:
                messagebox.showerror("Invalid Cube", f"Color {color} occurs {count} times instead of 9.")
                return

        centers = [self.face_data[f][4] for f in ["U", "D", "F", "B", "L", "R"]]
        if len(set(centers)) != 6:
            messagebox.showerror("Invalid Centers", "Each center piece must be a different color.")
            return

        self.callback(self.face_data)
        self.root.destroy()

    def on_close(self):
        self.callback(None)
        self.root.destroy()

def color_preview_color_name(letter):
    return {
        "W": "White",
        "Y": "Yellow",
        "R": "Red",
        "O": "Orange",
        "B": "Blue",
        "G": "Green"
    }.get(letter.upper(), "Unknown")

def get_manual_import_data():
    import tkinter as tk
    import queue

    q = queue.Queue()

    def return_data(data):
        sides_dict = {}
        if data is not None:
            for face in data:
                center = data[face][4]
                sides_dict[center.lower()] = ''.join(s.lower() for s in data[face])
            #sides_dict['r'], sides_dict['o'] = sides_dict['o'], sides_dict['r']
            q.put(sides_dict)   
        else: q.put(None)

    root = tk.Tk()
    root.withdraw()
    entry_window = ManualColorEntry(root, return_data)
    root.wait_window(entry_window.root)  # Czeka tylko na zamknięcie Toplevel
    dict_data = q.get()
    print("Importing data manually:")
    print(dict_data)
    return dict_data