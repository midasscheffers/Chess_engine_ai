

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
        type_to_char_dict = {Piece.King:"k", Piece.Pawn:"p", Piece.Knight:"n", Piece.Bishop:"b", Piece.Rook:"r", Piece.Queen:"q", Piece.Empty:" "}
        p_str = type_to_char_dict[Piece.piece_type(p)]
        if Piece.piece_color(p) == Piece.White:
            p_str = p_str.upper()
        return p_str


class Board():

    def __init__(self):
        self.squares = [0 for _ in range(64)]
        self.castle_rights = 15
        self.moves = 1
        self.halfmoves = 0
        self.ep_square = -1
        self.is_white_turn = 1
        self.load_FEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")


    def set_piece(self, p:Piece, sqr:int):
        self.squares[sqr] = p


    def index_to_cord(i:int):
        pass


    def cord_to_index(cord:str):
        pass
    

    def load_FEN(self, FEN:str):
        state, turn, castle, ep_square, halfmoves, moves = FEN.split(" ")
        self.halfmoves = int(halfmoves)
        self.moves = int(moves)
        if ep_square == "-":
            self.ep_square = -1
        else:
            self.ep_square = self.cord_to_index(ep_square)
        
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




b = Board()
# print(b.squares)
b.print()
