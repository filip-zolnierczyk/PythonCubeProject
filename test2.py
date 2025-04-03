import cube

c = cube.RubiksCube()

print(c.sides)

c.perform_f_move()
c.rotate_side('g')

print(c.sides)
