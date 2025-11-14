"""
This file hold a basic adversary.

Plan:
Use simple evaluation.
Use alpha beta pruning.
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

for i in range(1,10):
    print(f"found: {positions_reached(i)} after {i}:ply")