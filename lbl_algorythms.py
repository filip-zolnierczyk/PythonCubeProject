from util.rubiks_move_util import next_side, previous_side, opposite_side


def corner_insert_right(cube):
    cube.perform_r_move()
    cube.perform_u_move()
    cube.perform_r_move(False)
    cube.perform_u_move(False)


def corner_insert_left(cube):
    cube.perform_l_move(False)
    cube.perform_u_move(False)
    cube.perform_l_move()
    cube.perform_u_move()


def sune(cube):
    cube.perform_r_move()
    cube.perform_u_move()
    cube.perform_r_move(False)
    cube.perform_u_move()
    cube.perform_r_move()
    cube.perform_u2_move()
    cube.perform_r_move(False)
    cube.perform_u_move()


def position_corners(cube):
    cube.perform_u_move()
    cube.perform_r_move()
    cube.perform_u_move(False)
    cube.perform_l_move(False)
    cube.perform_u_move()
    cube.perform_r_move(False)
    cube.perform_u_move(False)
    cube.perform_l_move()


def rotate_top_corner(cube):
    for _ in range(2):
        cube.perform_r_move(False)
        cube.perform_d_move()
        cube.perform_r_move()
        cube.perform_d_move(False)


#lbl steps:


def white_cross(cube):

    while not (cube.sides[cube.top_side][1] == "w" and cube.sides[cube.top_side][3] == "w" and cube.sides[cube.top_side][5] == "w" and cube.sides[cube.top_side][7] == "w"):

        #biale na dole
        if cube.sides[cube.bottom_side][1] == "w":
            if cube.sides[cube.top_side][7] != "w":
                cube.perform_f2_move()
            else:
                while cube.sides[cube.top_side][7] == "w":
                    cube.perform_u_move()
                cube.perform_f2_move()

        #obrocone biale na dole
        if cube.sides[cube.facing_user][7] == "w":
            if cube.sides[cube.top_side][7] != "w":
                cube.perform_f_move()
                cube.perform_u_move()
                cube.perform_l_move(False)
            else:
                while cube.sides[cube.top_side][7] == "w":
                    cube.perform_u_move()
                cube.perform_f_move()
                cube.perform_u_move()
                cube.perform_l_move(False)
        # obrocone biale gorze
        if cube.sides[cube.facing_user][1] == "w":
            cube.perform_f_move()
            cube.perform_u_move(False)
            cube.perform_r_move()
            cube.perform_u_move()



        # biale na bokach
        if cube.sides[cube.facing_user][3] == "w":
            if cube.sides[cube.top_side][3] != "w":
                cube.perform_l_move(False)
            else:
                while cube.sides[cube.top_side][3] == "w":
                    cube.perform_u_move()
                cube.perform_l_move(False)

        if cube.sides[cube.facing_user][5] == "w":
            if cube.sides[cube.top_side][5] != "w":
                cube.perform_r_move()
            else:
                while cube.sides[cube.top_side][5] == "w":
                    cube.perform_u_move()
                cube.perform_r_move()

        cube.rotate_cube()

    #włożenie białych na dół
    for i in range(4):

        if cube.sides[cube.top_side][1] == "w":
            if cube.sides[next_side(next_side(cube.facing_user))][1] == \
                    cube.sides[next_side(next_side(cube.facing_user))][4]:
                cube.perform_b2_move()
        if cube.sides[cube.top_side][3] == "w":
            if cube.sides[previous_side(cube.facing_user)][1] == cube.sides[previous_side(cube.facing_user)][4]:
                cube.perform_l2_move()
        if cube.sides[cube.top_side][5] == "w":
            if cube.sides[next_side(cube.facing_user)][1] == cube.sides[next_side(cube.facing_user)][4]:
                cube.perform_r2_move()
        if cube.sides[cube.top_side][7] == "w":
            if cube.sides[cube.facing_user][1] == cube.sides[cube.facing_user][4]:
                cube.perform_f2_move()
        cube.perform_u_move()


def insert_bottom_corners(cube): #działa a nie powinno xd

    def check_corners(cube):

        #prawy róg
        if cube.sides[next_side(cube.facing_user)][0] == "w" and cube.sides[cube.top_side][8] == next_side(cube.facing_user) and cube.sides[cube.facing_user][2] == cube.facing_user:
            corner_insert_right(cube)

        #lewy róg
        if cube.sides[previous_side(cube.facing_user)][2] == "w" and cube.sides[cube.top_side][6] == previous_side(cube.facing_user) and cube.sides[cube.facing_user][0] == cube.facing_user:
            corner_insert_left(cube)

        # prawy róg białe do góry
        if cube.sides[next_side(cube.facing_user)][0] == cube.facing_user and cube.sides[cube.top_side][8] == "w" and cube.sides[cube.facing_user][2] == next_side(cube.facing_user):
            for a in range(3):
                corner_insert_right(cube)

        if cube.sides[previous_side(cube.facing_user)][2] == cube.facing_user and cube.sides[cube.top_side][
            6] == "w" and cube.sides[cube.facing_user][0] == previous_side(cube.facing_user):
            for a in range(3):
                corner_insert_left(cube)

    def wrongly_insterted_corners(cube):
        if cube.sides[cube.facing_user][8] == "w" or cube.sides[next_side(cube.facing_user)][6] == "w" or (cube.sides[cube.bottom_side][2] == "w" and cube.sides[cube.facing_user][8] != cube.facing_user):
            corner_insert_right(cube)

    while not (cube.sides["g"][6:] == "ggg" and cube.sides["r"][6:] == "rrr" and cube.sides["b"][6:] == "bbb" and cube.sides["o"][6:] == "ooo"):
        for j in range(4):
            check_corners(cube)
            cube.perform_u_move()
        cube.rotate_cube()
        wrongly_insterted_corners(cube)


def insert_edges(cube):
    while not (cube.sides["g"][3:6] == "ggg" and cube.sides["r"][3:6] == "rrr" and cube.sides["b"][3:6] == "bbb" and cube.sides["o"][3:6] == "ooo"):
        for j in range(4):
            if cube.sides[cube.facing_user][1] == cube.facing_user:

                if cube.sides[cube.top_side][7] == next_side(cube.facing_user):
                    cube.perform_u_move()
                    corner_insert_right(cube)
                    cube.rotate_cube()
                    corner_insert_left(cube)
                    cube.rotate_cube(False)

                if cube.sides[cube.top_side][7] == previous_side(cube.facing_user):
                    cube.perform_u_move(False)
                    corner_insert_left(cube)
                    cube.rotate_cube(False)
                    corner_insert_right(cube)
                    cube.rotate_cube()

            cube.perform_u_move()

        #edge case
        t = []
        t.append(cube.sides["g"][1])
        t.append(cube.sides["r"][1])
        t.append(cube.sides["b"][1])
        t.append(cube.sides["0"][1])
        for a in range(4):
            t.append(cube.sides[cube.top_side][1+a*2])
        if t.count("y") == 4:
            pass


        cube.rotate_cube()


def yellow_cross(cube):

    def permutate_top(cube):
        cube.perform_f_move()
        corner_insert_right(cube)
        cube.perform_f_move(False)

    def check_dot_formation(cube):
        for i in range(4):
            if cube.sides[cube.top_side][i*2+1] == "y":
                return
        permutate_top(cube)

    def check_l_or_line(cube):
        if cube.sides[cube.top_side][3] == "y" == cube.sides[cube.top_side][5]:
            permutate_top(cube)
        elif cube.sides[cube.top_side][1] == "y" == cube.sides[cube.top_side][7]:
            cube.perform_u_move()
            permutate_top(cube)
        else:
            while not (cube.sides[cube.top_side][1] == "y" == cube.sides[cube.top_side][3]):
                cube.perform_u_move()
            permutate_top(cube)
            permutate_top(cube)

    while not (cube.sides[cube.top_side][1] == "y" and cube.sides[cube.top_side][3] == "y" and
               cube.sides[cube.top_side][5] == "y" and cube.sides[cube.top_side][7] == "y"):
        check_dot_formation(cube)
        check_l_or_line(cube)


def allign_top_edges(cube):
    rotation_count = 0
    while (not (cube.sides[cube.facing_user][1] == cube.facing_user and cube.sides[next_side(cube.facing_user)][1] == next_side(cube.facing_user) and
               cube.sides[opposite_side(cube.facing_user)][1] == opposite_side(cube.facing_user) and cube.sides[previous_side(cube.facing_user)][1] == previous_side(cube.facing_user)) and
           rotation_count < 3):
        if cube.sides[cube.facing_user][1] == cube.facing_user and cube.sides[opposite_side(cube.facing_user)][1] == opposite_side(cube.facing_user):
            cube.perform_u_move()
            sune(cube)
            cube.rotate_cube()
            cube.rotate_cube()
            sune(cube)
            while cube.sides[cube.facing_user][1] != cube.sides[cube.facing_user][4]:
                cube.perform_u_move()
            return
        cube.perform_u_move()
        rotation_count += 1
    if rotation_count == 3:
        for i in range(4):
            for j in range(4):
                if (cube.sides[next_side(cube.facing_user)][1] == next_side(cube.facing_user) and cube.sides[opposite_side(cube.facing_user)][1] == opposite_side(cube.facing_user)):
                    sune(cube)
                    while cube.sides[cube.facing_user][1] != cube.sides[cube.facing_user][4]:
                        cube.perform_u_move()
                    return
                cube.perform_u_move()
            cube.rotate_cube()
    while cube.sides[cube.facing_user][1] != cube.sides[cube.facing_user][4]:
        cube.perform_u_move()


def position_top_corners(cube):
    def is_right_corner_ok(cube):
        l = []
        l.append(cube.sides[cube.facing_user][2])
        l.append(cube.sides[next_side(cube.facing_user)][0])
        l.append(cube.sides[cube.top_side][8])
        if cube.facing_user in l and next_side(cube.facing_user) in l:
            return True

    def is_left_corner_ok(cube):
        l = []
        l.append(cube.sides[cube.facing_user][0])
        l.append(cube.sides[previous_side(cube.facing_user)][2])
        l.append(cube.sides[cube.top_side][6])
        if cube.facing_user in l and previous_side(cube.facing_user) in l:
            return True

    for i in range(4):
        if is_right_corner_ok(cube):
            while not is_left_corner_ok(cube):
                position_corners(cube)
            return
        cube.rotate_cube()


def permutate_top_corners(cube):
    while cube.sides[cube.top_side] != "yyyyyyyyy":
        while cube.sides[cube.top_side][8] != "y":
            rotate_top_corner(cube)
        cube.perform_u_move(False)


def last_move(cube):
    while cube.sides[cube.facing_user][0] != cube.sides[cube.facing_user][4]:
        cube.perform_u_move()