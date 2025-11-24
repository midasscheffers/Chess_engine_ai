"""
For testing the engine
"""



from engine_classes import *
from basic_bot import *
import time

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

# test positions found
b.load_FEN("rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8")
for i in range(1,5):
    t_start = time.time()*1000.0
    number = positions_reached(i)
    t_end = time.time()*1000.0
    dt = t_end - t_start
    print(f"Found at ply{i}: {number}, in {dt} ms")



b.load_FEN("rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8")
bot = Chess_Bot()
bot.suggest_move()
