import cube

c = cube.RubiksCube()

print(c.sides)

c.perform_l_move()
c.perform_f_move()

print(c.sides)
