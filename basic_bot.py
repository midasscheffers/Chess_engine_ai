"""
This file hold a basic adversary.

Plan:
Use simple evaluation.
Use alpha beta pruning.
"""


from engine_classes import *
from copy import deepcopy
from random import choice

class Chess_Bot:
    

    def suggest_move(self, board:Board, mode:str="Default"):
        if mode=="Default":
            depth = 3
            temp_board = deepcopy(board)
            sc,m = self.Search_move_tree_for_best_move(temp_board, depth, -1e10, 1e10)
            return m
        else:
            moves = board.get_moves()
            return choice(moves)


    def Search_move_tree_for_best_move(self, board:Board, depth:int, alpha:float, beta:float):
        if depth == 0:
            return self.eval(board), None
        moves = board.get_moves()
        if not len(moves):
            return -1e10, None
        best_score = -1e10
        best_move = moves[0]
        for m in moves:
            board.make_move(m)
            trial, _ = self.Search_move_tree_for_best_move(board, depth-1, -beta, -alpha)
            trial = -trial
            if trial > best_score:
                best_move = m
                best_score = trial
                if trial > alpha:
                    alpha = trial
            if trial >= beta:
                board.unmake_move()
                break
            board.unmake_move()

        return best_score, best_move

    
    def eval(self, board:Board):
        piece_val_dic = {Piece.King:1e6, Piece.Queen:9, Piece.Rook:5, Piece.Bishop:3, Piece.Knight:3, Piece.Pawn:1, Piece.Empty:0}
        piece_val = 0
        for sq in range(64):
            p = board.squares[sq]
            sign = 1 if Piece.piece_color(p) == Piece.White else -1
            val = sign * piece_val_dic[Piece.piece_type(p)]
            piece_val += val
        return piece_val


