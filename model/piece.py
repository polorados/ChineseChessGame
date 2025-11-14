from .rank import Rank
from .player import Player

class Position:
    row: int
    col: int

    def __init__(self,row,col):
        self.row = row
        self.col = col
class Piece:
    id: int
    name: str
    rank: Rank
    owner: Player
    position: Position
    is_alive: bool = True

    def __init__(self, name, rank: Rank, owner: Player, position: Position):
        self.id = id(self)
        self.name = name
        self.rank = rank
        self.owner = owner
        self.position = position
        self.symbol = owner.name[0] + name[0] + str(self.rank.value)
    
    def remove_piece(self):
        self.is_alive = False
        self.position = None