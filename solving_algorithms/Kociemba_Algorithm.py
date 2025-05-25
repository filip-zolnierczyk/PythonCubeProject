import kociemba

def solve_kociemba(state: dict) -> list:   
    if len(state) != 6:
        return ValueError("Kociemba solver only works for 3x3 cubes!")
    
    # convert to kociemba input -> single 52 char string
    face_order = ['y', 'o', 'g', 'w', 'r', 'b'] # ORDER: up right front down left back
    input_string = ""
    for face in face_order:
        input_string += key_convert(state[face])

    solution = kociemba.solve(input_string)

    print("Kociemba solution: " + solution)

    return solution.split()

def key_convert(key: str):
    """ 
        green - front
        red - left
        blue - back
        orange - right
        yellow - up
        white - down
    """
    def char_convert(c):
        match c:
            case 'g': return 'F'
            case 'r': return 'L'
            case 'b': return 'B'
            case 'o': return 'R'
            case 'y': return 'U'
            case 'w': return 'D'
    
    converted = ""
    for s in key:
        converted += char_convert(s)
    return converted