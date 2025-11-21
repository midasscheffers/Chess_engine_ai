
from dataclasses import dataclass

@dataclass 
class BitBoard:

    FULL = 18446744073709551615
    Empty = 0


    def bb_from_sq(sq:int) -> int:
        return 1<<sq
    

    def row_mask(r:int) -> int:
        return 72340172838076673 << r

class Board:

    def __init__(self) -> None:
        self.bitboards:list[int] = [0 for _ in range(12)]
        self.moves_counter:int = 1
        self.halfmoves_counter:int = 0
        self.castle_right:list[list[bool]] = [[True for _ in range(4)]]
        self.ep_square:list[int] = [-1]

    
    def set_piece(self, p, sq):


    def remove_piece(self, sq):
        for bb in self.bitboards:
            bb