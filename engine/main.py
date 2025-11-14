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

    flag = 0
    is_capture = 1
    is_check = 2
    is_castle = 4
    is_promotion = 8

    




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

    def xy_to_index(x,y):
        return x+8*y

    def load_FEN(self, FEN:str):
        state, turn, castle, ep_square, halfmoves, moves = FEN.split(" ")
        self.halfmoves = int(halfmoves)
        self.moves = int(moves)
        if ep_square == "-":
            self.ep_square = -1
        else:
            self.ep_square = Board.cord_to_index(ep_square)

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
            enem_color = Piece.Black if this_color == Piece.White else Piece.White
            if not this_color == (Piece.White if self.is_white_turn else Piece.Black):
                continue

            # run for different pieces the code
            if this_type == Piece.Knight:
                for m in self.pre_computed.knight_moves_on_sq[sq]:
                    if not Piece.piece_color(self.squares[m]) == this_color:
                        moves.append(Move(sq, m))
            elif this_type in [Piece.Bishop, Piece.Rook, Piece.Queen]:
                for d in self.pre_computed.sliding_moves_on_sq[sq]:
                    if this_type == Piece.Bishop:
                        if (d[0]+d[1])%2 == 1:
                            continue
                    elif this_type == Piece.Rook:
                        if (d[0]+d[1])%2 == 0:
                            continue
                    for sm in self.pre_computed.sliding_moves_on_sq[sq][d]:
                        if Piece.piece_color(self.squares[sm]) == Piece.Empty:
                            moves.append(Move(sq, sm))
                        elif Piece.piece_color(self.squares[sm]) == this_color:
                            break
                        else:
                            moves.append(Move(sq, sm))
                            break
            elif this_type == Piece.Pawn:
                d = -1 if self.is_white_turn else 1
                f_line = 6 if self.is_white_turn else 1
                x,y = sq%8, sq//8
                
                if Piece.piece_color(self.squares[Board.xy_to_index(x, y+d)]) == Piece.Empty:
                            moves.append(Move(sq, Board.xy_to_index(x, y+d)))
                if Piece.piece_color(self.squares[Board.xy_to_index(x, y+2*d)]) == Piece.Empty and y==f_line:
                    moves.append(Move(sq, Board.xy_to_index(x, y+2*d)))
                if Piece.piece_color(self.squares[Board.xy_to_index(x+1, y+d)]) == enem_color and on_board(x+1, y+d):
                    moves.append(Move(sq, Board.xy_to_index(x+1, y+d)))
                if Piece.piece_color(self.squares[Board.xy_to_index(x-1, y+d)]) == enem_color and on_board(x-1, y+d):
                    moves.append(Move(sq, Board.xy_to_index(x-1, y+d)))
                


        return moves
                    


def on_board(x,y):
    if x<0 or x>7 or y<0 or y>7:
        return False
    return True



class pre_computed_data():
    knight_moves = [(-1,-2), (1, -2), (-2, -1), (2, -1), (-2, 1), (2,1), (-1, 2), (1, 2)]
    knight_moves_on_sq = []
    for sq in range(64):
        x,y = sq%8, sq//8
        possible_moves = []
        for km in knight_moves:
            target_x, target_y = x+km[0], y+km[1]
            if on_board(target_x, target_y):
                target_sq = target_x + 8*target_y
                possible_moves.append(target_sq)
        knight_moves_on_sq.append(possible_moves)

    directions = [(-1,-1), (0,-1), (1,-1), (-1,0), (1,0), (-1, 1), (0, 1), (1,1)]
    sliding_moves_on_sq = []
    for sq in range(64):
        sliding_moves_on_sq.append({})
        x,y = sq%8, sq//8
        for d in directions:
            depth = 1
            target_x, target_y = x+d[0]*depth, y+d[1]*depth
            while on_board(target_x, target_y):
                target_sq = target_x + 8*target_y
                if d not in sliding_moves_on_sq[sq].keys():
                    sliding_moves_on_sq[sq][d] = []
                sliding_moves_on_sq[sq][d].append(target_sq)
                depth += 1
                target_x, target_y = x+d[0]*depth, y+d[1]*depth






b = Board()
b.print()
print(b.get_moves())
