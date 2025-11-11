

class Piece():
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
        
        lines = state.split("/")
        for j,l in enumerate(lines):
            




b = Board()
print(b.squares)
b.set_piece(Piece.White|Piece.Bishop, 3)
print(b.squares)
print(Piece.piece_type(b.squares[3]))

