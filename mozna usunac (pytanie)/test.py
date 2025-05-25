from rubiks_data import RubiksCube
from solve_lbl import *

c = RubiksCube()

c.perform_f_move()
c.perform_u_move()
c.perform_l_move()
c.perform_u_move(False)
c.perform_b_move(False)
c.perform_u_move()
c.perform_l_move()
c.perform_u_move()
c.perform_l_move()
c.perform_u_move(False)
c.perform_b_move(False)
c.perform_l_move()
c.perform_u_move()
c.perform_l_move()
c.perform_u_move()
c.perform_d_move(False)
c.display_cube()

solve_lbl(c)
print("-------------------")
c.display_cube()
print(c.performed_moves)
print(len(c.performed_moves))



