from numpy.f2py.auxfuncs import throw_error


def opposite_side(x):
    if x == "b":
        return "g"
    if x == "y":
        return "w"
    if x == "r":
        return "o"
    if x == "g":
        return "b"
    if x == "w":
        return "y"
    if x == "o":
        return "r"
    else:
        throw_error("Color does not exist")


def next_side(x):
    if x == "b":
        return "r"
    if x == "r":
        return "g"
    if x == "g":
        return "o"
    if x == "o":
        return "b"
    else:
        throw_error("Color does not exist")


def previous_side(x):
    if x == "b":
        return "o"
    if x == "o":
        return "g"
    if x == "g":
        return "r"
    if x == "r":
        return "b"
    else:
        raise ValueError("Color does not exist")


def convert_table_to_side(t):
    string = t[0] + t[3] + t[6] + t[1] + t[4] + t[7] + t[2] + t[5] + t[8]git add tolo
    return string
