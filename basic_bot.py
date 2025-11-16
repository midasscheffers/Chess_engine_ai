"""
This file hold a basic adversary.

Plan:
Use simple evaluation.
Use alpha beta pruning.
"""


from engine_classes import *
from random import choice

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


class Chess_Bot:

    def __init__(self, board:Board):
        self.board = board
    

    def make_move(self):
        depth = 3
        sc,m = self.Search_move_tree_for_best_move(depth)
        self.board.make_move(m)


    def Search_move_tree_for_best_move(self, depth):
        if depth == 0:
            return self.eval(), None
        moves = self.board.get_moves()
        if not len(moves):
            return -1e10, None
        best_score = -1e10
        best_move = moves[0]
        for m in moves:
            self.board.make_move(m)
            trial, _ = self.Search_move_tree_for_best_move(depth-1)
            trial = -trial
            if trial > best_score:
                best_move = m
                best_score = trial
            self.board.unmake_move()

        return best_score, best_move

    
    def eval(self):
        piece_val_dic = {Piece.King:1e6, Piece.Queen:9, Piece.Rook:5, Piece.Bishop:3, Piece.Knight:3, Piece.Pawn:1, Piece.Empty:0}
        piece_val = 0
        for sq in range(64):
            p = self.board.squares[sq]
            sign = 1 if Piece.piece_color(p) == Piece.White else -1
            val = sign * piece_val_dic[Piece.piece_type(p)]
            piece_val += val
        return piece_val


