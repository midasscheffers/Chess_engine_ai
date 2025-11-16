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
    flag:int = 0
    captured_piece:int = 0

    is_capture = 1
    is_castle = 2
    is_promotion = 4
    is_double_pawn_move = 8
    is_ep = 16

    




class Board():

    def __init__(self):
        self.squares = [0 for _ in range(64)]
        self.castle_rights = [15]
        self.moves = 1
        self.halfmoves = 0
        self.ep_square = [-1]
        self.is_white_turn = 1
        self.captured_material = []
        self.moves_made = []
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
        self.moves_made = []
        self.halfmoves = int(halfmoves)
        self.moves = int(moves)
        if ep_square == "-":
            self.ep_square = [-1]
        else:
            self.ep_square = [Board.cord_to_index(ep_square)]

        if turn == "w":
            self.is_white_turn = 1
        else:
            self.is_white_turn = 0

        self.castle_rights = 0
        str_to_castle_dict = {"-":0, "K":8, "Q":4, "k":2, "q":1}
        for c in castle:
            self.castle_rights = self.castle_rights | str_to_castle_dict[c]
        self.castle_rights = [self.castle_rights]
        
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
        print(f"turn:{turn}, moves:{self.moves}, half moves:{self.halfmoves}, castle rights:{self.castle_rights[-1]}, ep_sqr:{self.ep_square[-1]}")
    

    def print_squares(sqrs):
        for i in range(64):
            if i in sqrs:
                print("X",end="")
            else:
                print(".",end="")
            if i%8==7:
                print()


    def make_move(self, m:Move):
        self.moves_made.append(m)
        p_start = self.squares[m.start]
        p_end = self.squares[m.target]
        self.squares[m.start] = Piece.Empty
        if m.flag & Move.is_capture:
            self.captured_material.append(m.captured_piece)
        castled = False
        if m.flag & Move.is_castle:
            dir = m.target-m.start
            if dir == 2:
                self.squares[m.target+1] = 0
                self.squares[m.target-1] = Piece.piece_color(p_start) | Piece.Rook
            else:
                self.squares[m.target-2] = 0
                self.squares[m.target+1] = Piece.piece_color(p_start) | Piece.Rook
        # castle rights logic
        if p_start == Piece.King|Piece.White:
            self.castle_rights.append(self.castle_rights[-1] & 3)
        elif p_start == Piece.King|Piece.Black:
            self.castle_rights.append(self.castle_rights[-1] & 12)
        elif p_start == Piece.Rook|Piece.White:
            if m.start%8 == 0:
                self.castle_rights.append(self.castle_rights[-1] & 11)
            else:
                self.castle_rights.append(self.castle_rights[-1] & 7)
        elif p_end == Piece.Rook|Piece.White:
            if m.target%8 == 0:
                self.castle_rights.append(self.castle_rights[-1] & 11)
            else:
                self.castle_rights.append(self.castle_rights[-1] & 7)
        elif p_start == Piece.Rook|Piece.Black:
            if m.start%8 == 0:
                self.castle_rights.append(self.castle_rights[-1] & 14)
            else:
                self.castle_rights.append(self.castle_rights[-1] & 13)
        elif p_end == Piece.Rook|Piece.Black:
            if m.target%8 == 0:
                self.castle_rights.append(self.castle_rights[-1] & 14)
            else:
                self.castle_rights.append(self.castle_rights[-1] & 13)
        else:
            self.castle_rights.append(self.castle_rights[-1])
        #
        if m.flag & Move.is_double_pawn_move:
            self.ep_square.append((m.start+m.target)//2)
        else:
            self.ep_square.append(-1)
        if m.flag & Move.is_ep:
            self.squares[m.target -8*(m.target//8 - m.start//8)] = 0
        if m.flag & Move.is_promotion:
            self.squares[m.target] = Piece.piece_color(p_start) | Piece.Queen
        else:
            self.squares[m.target] = p_start
        self.halfmoves += 1
        self.moves += 1 if not self.is_white_turn else 0
        self.is_white_turn = not self.is_white_turn
            

    def unmake_move(self):
        if not len(self.moves_made):
            return
        self.ep_square.pop()
        self.castle_rights.pop()
        m = self.moves_made.pop()
        p_start = self.squares[m.start]
        p_end = self.squares[m.target]
        self.squares[m.start] = self.squares[m.target]
        if m.flag & Move.is_promotion:
            self.squares[m.start] = Piece.piece_color(p_end) | Piece.Pawn
        if m.flag & Move.is_castle:
            dir = m.target-m.start
            if dir == 2:
                self.squares[m.target+1] = Piece.piece_color(p_end) | Piece.Rook
                self.squares[m.target-1] = 0
            else:
                self.squares[m.target-2] = Piece.piece_color(p_end) | Piece.Rook
                self.squares[m.target+1] = 0
        if m.flag & Move.is_capture and not m.flag & Move.is_ep:
            self.squares[m.target] = m.captured_piece
            self.captured_material.pop()
        elif m.flag & Move.is_ep:
            piece = self.captured_material.pop()
            self.squares[m.target -8*(m.target//8 - m.start//8)] = piece
            self.squares[m.target] = Piece.Empty
        else:
            self.squares[m.target] = Piece.Empty
        self.halfmoves += -1
        self.moves += -1 if self.is_white_turn else 0
        self.is_white_turn = not self.is_white_turn

    
    def get_sq_king(self, opps=False):
        if opps:
            color = Piece.White if not self.is_white_turn else Piece.Black
        else:
            color = Piece.White if self.is_white_turn else Piece.Black
        for sq, p in enumerate(self.squares):
            if p == color | Piece.King:
                return sq
        

    def controlled_by_enemy(self, sq, opps=False):
        if sq == None:
            return True
        if opps:
            enem_color = Piece.White if self.is_white_turn else Piece.Black
            enem_pawn_dir = 1 if self.is_white_turn else -1
        else:
            enem_color = Piece.White if not self.is_white_turn else Piece.Black
            enem_pawn_dir = 1 if not self.is_white_turn else -1
        #check if an enemy sliding piece is looking at the sq
        # self.print()
        # print("cc", sq)
        for d in self.pre_computed.sliding_moves_on_sq[sq]:
            pieces_to_check_for = [Piece.Queen|enem_color, Piece.Bishop|enem_color] if ((d[0]+d[1])%2==0) else [Piece.Queen|enem_color, Piece.Rook|enem_color]
            first_slide_check = True
            for sm in self.pre_computed.sliding_moves_on_sq[sq][d]:
                if not self.squares[sm] == Piece.Empty:
                    if first_slide_check and self.squares[sm] == Piece.King|enem_color:
                        return True
                    if self.squares[sm] in pieces_to_check_for:
                        return True , f"by {self.squares[sm]} on {sm}" 
                    break
                first_slide_check = False
        # check if a knight is a knight move away
        for km in self.pre_computed.knight_moves_on_sq[sq]:
            if self.squares[km] == Piece.Knight | enem_color:
                return True, f"by {Piece.Knight | enem_color} on {km}" 
        # check for pawns
        x,y = sq%8, sq//8
        if on_board(x+1, y+enem_pawn_dir) and self.squares[(x+1+8*(y+enem_pawn_dir))] == Piece.Pawn | enem_color:
            return True
        if on_board(x-1, y+enem_pawn_dir) and self.squares[(x-1+8*(y+enem_pawn_dir))] == Piece.Pawn | enem_color:
            return True

        return False


    def get_moves(self):
        moves = self.get_pseudo_moves()
        final = []
        for m in moves:
            self.make_move(m)
            king_sq = self.get_sq_king(opps=True)
            # print("ks", king_sq)
            if not self.controlled_by_enemy(king_sq, opps=True):
                final.append(m)
            self.unmake_move()
        return final


    def get_pseudo_moves(self, color_to_check=None, check_casteling=True):
        if color_to_check == None:
            color_to_check = (Piece.White if self.is_white_turn else Piece.Black)
        moves = []
        for sq, p in enumerate(self.squares):
            this_type = Piece.piece_type(p)
            this_color = Piece.piece_color(p)
            enem_color = Piece.Black if this_color == Piece.White else Piece.White
            if not this_color == color_to_check:
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
                l_line = 0 if self.is_white_turn else 7
                x,y = sq%8, sq//8
                
                if on_board(x, y+d) and Piece.piece_color(self.squares[Board.xy_to_index(x, y+d)]) == Piece.Empty:
                    m = Move(sq, Board.xy_to_index(x, y+d))
                    if y+d == l_line:
                        m.flag |= Move.is_promotion
                    moves.append(m)
                    if y==f_line and Piece.piece_color(self.squares[Board.xy_to_index(x, y+2*d)]) == Piece.Empty:
                        m = Move(sq, Board.xy_to_index(x, y+2*d))
                        m.flag |= Move.is_double_pawn_move
                        moves.append(m)
                if on_board(x+1, y+d) and Piece.piece_color(self.squares[Board.xy_to_index(x+1, y+d)]) == enem_color:
                    m = Move(sq, Board.xy_to_index(x+1, y+d))
                    if y+d == l_line:
                        m.flag |= Move.is_promotion
                    moves.append(m)
                if on_board(x-1, y+d) and Piece.piece_color(self.squares[Board.xy_to_index(x-1, y+d)]) == enem_color:
                    m = Move(sq, Board.xy_to_index(x-1, y+d))
                    if y+d == l_line:
                        m.flag |= Move.is_promotion
                    moves.append(m)
                if Board.xy_to_index(x+1, y+d) == self.ep_square[-1]:
                    m = Move(sq, Board.xy_to_index(x+1, y+d))
                    m.flag |= Move.is_ep
                    m.flag |= Move.is_capture
                    m.captured_piece = enem_color | Piece.Pawn
                    moves.append(m)
                if Board.xy_to_index(x-1, y+d) == self.ep_square[-1]:
                    m = Move(sq, Board.xy_to_index(x-1, y+d))
                    m.flag |= Move.is_ep
                    m.flag |= Move.is_capture
                    m.captured_piece = enem_color | Piece.Pawn
                    moves.append(m)
            elif this_type == Piece.King:
                for d in self.pre_computed.sliding_moves_on_sq[sq]:
                    sm = self.pre_computed.sliding_moves_on_sq[sq][d][0]
                    if not Piece.piece_color(self.squares[sm]) == this_color:
                        moves.append(Move(sq, sm))
                possible_castle = [8,4] if this_color == Piece.White else [2,1]
                for fl in possible_castle:
                    if self.castle_rights[-1] & fl and check_casteling:
                        sqs_to_check = castle_sqrs(fl)
                        possible = True
                        for sq_tc in sqs_to_check:
                            # check if all is clear
                            if not self.squares[sq_tc] == Piece.Empty and not sq_tc == sq:
                                possible = False
                            if self.controlled_by_enemy(sq_tc):
                                possible = False
                            # check if not sqrs controlled by enemy
                        if possible:
                            m = Move(sq, sqs_to_check[0])
                            m.flag = Move.is_castle
                            moves.append(m)



        for m in moves:
            if not self.squares[m.target] == Piece.Empty:
                m.flag |= Move.is_capture
                m.captured_piece = self.squares[m.target]
                


        return moves
                    


def on_board(x,y):
    if x<0 or x>7 or y<0 or y>7:
        return False
    return True


def castle_sqrs(flag):
    if flag == 8:
        sqrs = [62, 61, 60]
    elif flag == 4:
        sqrs = [58, 59, 57, 60]
    elif flag == 2:
        sqrs = [6,5, 4]
    elif flag == 1:
        sqrs = [2, 1, 3, 4]
    else:
        sqrs = []
    return sqrs



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



