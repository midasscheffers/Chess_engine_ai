"""
For testing the engine
"""



from engine_classes import *
import time

b = Board()
b.load_FEN("rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8")

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
    t_start = time.time()*1000.0
    number = positions_reached(i)
    t_end = time.time()*1000.0
    dt = t_end - t_start
    print(f"Found at ply{i}: {number}, in {dt} ms")