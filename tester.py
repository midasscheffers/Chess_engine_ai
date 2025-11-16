"""
For testing the engine
"""



from engine_classes import *

b = Board()

def positions_reached(depth):
    if depth == 0:
        return 1
    total = 0
    moves = b.get_pseudo_moves()
    for m in moves:
        b.make_move(m)
        total += positions_reached(depth-1)
        b.unmake_move()
    return total


for i in range(1,6):
    print(f"Found at ply{i}: {positions_reached(i)}")