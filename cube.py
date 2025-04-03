import tools


class RubiksCube:
    # kostka przyjmuje tabele 6 tabel z czego każda reprezentuje ścianę kostki
    def __init__(self, tab = ["ggggggggg", "rrrrrrrrr", "bbbbbbbbb", "ooooooooo", "yyyyyyyyy", "wwwwwwwww"]):
        self.facing_user = 'g'
        self.bottom_side = 'w'
        self.top_side = 'y'
        self.sides = {
            "g": "",
            "r": "",
            "b": "",
            "o": "",
            "y": "",
            "w": ""
        }

        for t in tab:
            (c, s) = tools.convert_table_to_side(t)
            self.sides[c] = s

    def rotate_side(self, side, clockwise=True):
        s = self.sides[side]
        if clockwise:
            self.sides[side] = s[5] + s[2] + s[7] + s[0] + s[4] + s[1] + s[6] + s[3]
        else:
            self.sides[side] = s[3] + s[6] + s[1] + s[4] + s[0] + s[7] + s[2] + s[5]

    def perform_u_move(self, clockwise=True):
        order = ["g", "r", "b", "o"] if clockwise else ["g", "o", "b", "r"]
        temp = self.sides[order[0]][:3]

        for i in range(3):
            self.sides[order[i]] = self.sides[order[i + 1]][:3] + self.sides[order[i]][3:]

        self.sides[order[3]] = temp + self.sides[order[3]][3:]
        self.rotate_side(self.top_side, clockwise)

    def perform_d_move(self, clockwise=True):
        order = ["g", "o", "b", "r"] if clockwise else ["g", "r", "b", "o"]
        temp = self.sides[order[0]][-3:]

        for i in range(3):
            self.sides[order[i]] = self.sides[order[i + 1]][:-3] + self.sides[order[i]][-3:]

        self.sides[order[3]] = self.sides[order[3]][:-3] + temp
        self.rotate_side(self.bottom_side, clockwise)

    def perform_l_move(self, clockwise=True):
        # Ustalamy, która ściana jest "lewa" w zależności od facing_user
        left_mapping = {
            "g": ["y", "o", "w", "r"],
            "r": ["y", "b", "w", "g"],
            "b": ["y", "r", "w", "o"],
            "o": ["y", "g", "w", "b"]
        }
        order = left_mapping[self.facing_user] if clockwise else left_mapping[self.facing_user][::-1]

        temp = self.sides[order[0]][0] + self.sides[order[0]][3] + self.sides[order[0]][6]

        for i in range(3):
            self.sides[order[i]] = (self.sides[order[i + 1]][0] + self.sides[order[i + 1]][3] +
                                    self.sides[order[i + 1]][6] + self.sides[order[i]][1:])

        self.sides[order[3]] = temp + self.sides[order[3]][1:]
        self.rotate_side("o" if self.facing_user == "g" else "g", clockwise)

    def perform_r_move(self, clockwise=True):
        # Analogicznie jak w `perform_l_move`, ale dla prawej strony
        right_mapping = {
            "g": ["y", "r", "w", "o"],
            "r": ["y", "b", "w", "g"],
            "b": ["y", "o", "w", "r"],
            "o": ["y", "g", "w", "b"]
        }
        order = right_mapping[self.facing_user] if clockwise else right_mapping[self.facing_user][::-1]

        temp = self.sides[order[0]][2] + self.sides[order[0]][5] + self.sides[order[0]][8]

        for i in range(3):
            self.sides[order[i]] = (self.sides[order[i + 1]][2] + self.sides[order[i + 1]][5] +
                                    self.sides[order[i + 1]][8] + self.sides[order[i]][:2] +
                                    self.sides[order[i]][3:5] + self.sides[order[i]][6:8])

        self.sides[order[3]] = temp + self.sides[order[3]][:2] + self.sides[order[3]][3:5] + self.sides[order[3]][6:8]
        self.rotate_side("r" if self.facing_user == "g" else "b", clockwise)

    def perform_f_move(self, clockwise=True):
        # Przód zależy od facing_user
        front_mapping = {
            "g": ["y", "g", "w", "b"],
            "r": ["y", "r", "w", "g"],
            "b": ["y", "b", "w", "o"],
            "o": ["y", "o", "w", "r"]
        }
        order = front_mapping[self.facing_user] if clockwise else front_mapping[self.facing_user][::-1]

        temp = self.sides[order[0]][6:]  # Dolna warstwa żółtej ściany

        for i in range(3):
            self.sides[order[i]] = self.sides[order[i + 1]][6:] + self.sides[order[i]][:6]

        self.sides[order[3]] = temp + self.sides[order[3]][:6]
        self.rotate_side(self.facing_user, clockwise)

    def perform_b_move(self, clockwise=True):
        # Tył zależy od facing_user
        back_mapping = {
            "g": ["y", "b", "w", "g"],
            "r": ["y", "g", "w", "r"],
            "b": ["y", "o", "w", "b"],
            "o": ["y", "r", "w", "o"]
        }
        order = back_mapping[self.facing_user] if clockwise else back_mapping[self.facing_user][::-1]

        temp = self.sides[order[0]][:3]  # Górna warstwa żółtej ściany

        for i in range(3):
            self.sides[order[i]] = self.sides[order[i + 1]][:3] + self.sides[order[i]][3:]

        self.sides[order[3]] = temp + self.sides[order[3]][3:]
        self.rotate_side("b" if self.facing_user == "g" else "o", clockwise)
