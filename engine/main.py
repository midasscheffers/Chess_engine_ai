"""
This file holds all the classes needed to run the chess engine 
"""
from dataclasses import dataclass


@dataclass
class Piece():
    Empty = 0
    King = 1
    Pawn = 2
    Knight = 3
    Bishop = 4
    Rook = 5
    Queen = 6

    White = 8
    Black = 16

    def piece_color(p):
        return 24 & p
    

    def piece_type(p):
        return 7 & p


    def char_to_piece(p:str):
        color = Piece.White if p.isupper() else Piece.Black
        char_to_type_dict = {"k":Piece.King, "p": Piece.Pawn, "n":Piece.Knight, "b":Piece.Bishop, "r":Piece.Rook, "q":Piece.Queen}
        p_type = char_to_type_dict[p.lower()]
        return color | p_type


    def piece_to_char(p:int):
        type_to_char_dict = {Piece.King:"k", Piece.Pawn:"p", Piece.Knight:"n", Piece.Bishop:"b", Piece.Rook:"r", Piece.Queen:"q", Piece.Empty:"."}
        p_str = type_to_char_dict[Piece.piece_type(p)]
        if Piece.piece_color(p) == Piece.White:
            p_str = p_str.upper()
        return p_str



@dataclass
class Move:
    start:int = 0
    target:int = 0

    




class Board():

    def __init__(self):
        self.squares = [0 for _ in range(64)]
        self.castle_rights = 15
        self.moves = 1
        self.halfmoves = 0
        self.ep_square = -1
        self.is_white_turn = 1
        self.captured_material = []
        self.pre_computed = pre_computed_data()
        self.load_FEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")


    def set_piece(self, p:Piece, sqr:int):
        self.squares[sqr] = p


    def index_to_cord(i:int):
        x = i%8
        y = 8-(i//8)
        return str(chr(x+97))+str(y)


    def cord_to_index(cord:str):
        x,y = ord(cord[0])-97, int(cord[1])-1
        return x+(56-y*8)


    def load_FEN(self, FEN:str):
        state, turn, castle, ep_square, halfmoves, moves = FEN.split(" ")
        self.halfmoves = int(halfmoves)
        self.moves = int(moves)
        if ep_square == "-":
            self.ep_square = -1
        else:
            self.ep_square = self.cord_to_index(ep_square)

        if turn == "w":
            self.is_white_turn = 1
        else:
            self.is_white_turn = 0

        self.castle_rights = 0
        str_to_castle_dict = {"-":0, "K":8, "Q":4, "k":2, "q":1}
        for c in castle:
            self.castle_rights = self.castle_rights | str_to_castle_dict[c]
        
        self.squares = [0 for _ in range(64)]
        lines = state.split("/")
        for j,l in enumerate(lines):
            k = 0
            for c in l:
                if c.isnumeric():
                    k+= int(c)
                else:
                    self.set_piece(Piece.char_to_piece(c), j*8+k)
                    k+= 1
        
    
    def print(self):
        for i,p in enumerate(self.squares):
            print(Piece.piece_to_char(p),end="")
            if i%8==7:
                print()
        turn = "w" if self.is_white_turn else "b"
        print(f"turn:{turn}, moves:{self.moves}, half moves:{self.halfmoves}, castle rights:{self.castle_rights}, ep_sqr:{self.ep_square}")
    

    def print_squares(sqrs):
        for i in range(64):
            if i in sqrs:
                print("X",end="")
            else:
                print(".",end="")
            if i%8==7:
                print()


    def make_move(self, m:Move):
        p_start = self.squares[m.start]
        p_end = self.squares[m.target]
        self.squares[m.start] = Piece.Empty
        self.squares[m.target] = p_start
        if Piece.piece_type(p_end) == Piece.Empty:
            self.captured_material.append(p_end)
    

    def get_moves(self):
        moves = []
        for sq, p in enumerate(self.squares):
            this_type = Piece.piece_type(p)
            this_color = Piece.piece_color(p)
            if not this_color == (Piece.White if self.is_white_turn else Piece.Black):
                continue
            match this_type:
                case Piece.Knight:
                    for m in self.pre_computed.knight_moves_on_sq[sq]:
                        if not Piece.piece_color(self.squares[m]) == this_color:
                            moves.append(Move(sq, m))
        return moves
                    


def is_wrapped(sq, offset):
    """
    We do the following to determin if a move stays on the board and is not wrapped.
        1. convert sq to x,y
        2. convert offset to x',y'
        3. determin if x+x', y+y' on the board
    (Works only on offset within 3 spaces of original tile)
    """
    
    x_0,y_0 = sq%8, sq//8

    x_1,y_1 = ((offset+3)%8)-3, (offset+3)//8
    x_2,y_2 = x_0+x_1, y_0+y_1
    if x_2<0 or x_2 > 7 or y_2<0 or y_2 > 7:
        return True
    return False



class pre_computed_data():
    knight_moves = [-17, -15, -10, -6, 6, 10, 15, 17]
    knight_moves_on_sq = []
    for sq in range(64):
        possible_moves = []
        for km in knight_moves:
            if not is_wrapped(sq, km):
                possible_moves.append(sq+km)
        knight_moves_on_sq.append(possible_moves)

    straight_moves = []




b = Board()
b.print()
print(b.get_moves())

