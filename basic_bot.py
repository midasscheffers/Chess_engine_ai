"""
This file hold a basic adversary.

Plan:
Use simple evaluation.
Use alpha beta pruning.
"""


from engine_classes import *


class Chess_Bot:

    def __init__(self, board:Board):
        self.board = board
    

    def make_move(self):
        depth = 3
        sc,m = self.Search_move_tree_for_best_move(depth, -1e10, 1e10)
        self.board.make_move(m)


    def Search_move_tree_for_best_move(self, depth, alpha, beta):
        if depth == 0:
            return self.eval(), None
        moves = self.board.get_moves()
        if not len(moves):
            return -1e10, None
        best_score = -1e10
        best_move = moves[0]
        for m in moves:
            self.board.make_move(m)
            trial, _ = self.Search_move_tree_for_best_move(depth-1, -beta, -alpha)
            trial = -trial
            if trial > best_score:
                best_move = m
                best_score = trial
                if trial > alpha:
                    alpha = trial
            if trial >= beta:
                self.board.unmake_move()
                break
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


